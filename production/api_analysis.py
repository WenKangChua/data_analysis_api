from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel, field_validator
import calculations as cal
import data
import prediction_model as predict

router = APIRouter(prefix="/analysis", tags=["analysis"])

class Parameters(BaseModel):
    town: str | None
    flat_type: str | None
    flat_model: str | None
    floor_area_sqm: float | None
    remaining_lease_years: int | None
    storey: int | None
    year: int | None
    month_num: int | None

    @field_validator("storey", mode="before") 
    def transform_storey(cls, v): 
        if v is None: 
            return v 
        return cal.calculate_storey_upper(v)


@router.get("/sample")
def get_sample (
    limit: int = Query(1, ge=1, le=10, description="Show sample data. Maximum 10 rows")
):
    sample_data = cal.query_sample_data(data.hdb_resale_data,limit)
    return sample_data.to_dict(orient="records")


@router.get("/summary_stats")
def get_basic_stats(params: Parameters = Depends()):
    df = data.hdb_resale_data

    for column, value in params.model_dump().items():
        if value:
            df = df[df[column]==value]
    
    median_price = cal.calculate_median_price(df, "resale_price")
    avg_price = cal.calculate_average_price(df, "resale_price")
    max_price = cal.calculate_max_price(df, "resale_price")
    min_price = cal.calculate_min_price(df, "resale_price")

    return {
        "average_resale_price": "$ {:,.2f}".format(avg_price),
        "median_resale_price": "$ {:,.2f}".format(median_price),
        "max_resale_price": "$ {:,.2f}".format(max_price),
        "min_resale_price": "$ {:,.2f}".format(min_price)
    }


@router.get("/trend")
def resale_price_over_12_month(params: Parameters = Depends()):
    df = data.hdb_resale_data

    for column, value in params.model_dump().items():
        if value:
            df = df[df[column]==value]

    df = cal.calculate_last_n_month_mean_resale_prices(df, 12, "month")
    df["resale_price"] = df["resale_price"].map("{:,.2f}".format)
    df["month"] = df["month"].dt.date

    return df.to_dict(orient="records")


@router.post("/predict")
def predict_resale_price(params: Parameters):

    town = params.town
    flat_type = params.flat_type
    flat_model = params.flat_model
    floor_area_sqm = params.floor_area_sqm
    remaining_lease_years = params.remaining_lease_years
    storey = data.calculate_storey_upper(params.storey)
    year = params.year
    month_num = params.month_num

    result,mae,r_square = predict.predict_future_price(town, flat_type, flat_model, floor_area_sqm, 
                                     remaining_lease_years,storey,
                                     year, month_num)
    return {
        "Predicted Price": "${:,.2f}".format(result),
        "Mean Absolute Error": "${:,.2f}".format(mae),
        "R Squared" : "{:.2f}".format(r_square)
    }
