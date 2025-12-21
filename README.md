# HDB Resales Prices Data Analytics Through Server Side API

This project provides a server-side API built with FastAPI that enables users to perform data analytics on Singapore’s HDB resale transactions. By leveraging official datasets from [data.gov.sg](https://data.gov.sg/datasets?query=hdb+resale&resultId=d_8b84c4ee58e3cfc0ece0d773c8ca6abc), the API offers endpoints for exploring raw samples, generating statistical summaries, and predicting resale prices using machine learning.

Key highlights:

1) FastAPI-powered REST API for efficient and scalable analytics.

2) Data analytics with Pandas & Scikit-learn, providing both descriptive statistics and predictive modeling.

3) Random Forest model trained on historical resale data to estimate property prices.

4) Customizable queries: filter results by town, flat type, floor area, lease years, and more.

5) Interactive API docs available via SwaggerUI at `http://127.0.0.1:8000/docs`.

# How to use
## Packages
Make sure you have Python 3.9+ installed. Then install the required packages:

    pip install -r requirements.txt


## Quick Start 

1) Clone the repository
2) Locate `main.py` directory
3) Start the API server by runing `python3 -m uvicorn main:app`.
   - The default server will be http://127.0.0.1:8000. 
   - To host other than localhost, `python3 -m uvicorn main:app --host <insert ip> --port <insert port>`
5) You can now explore the API. 
   - A sample code for API calls can be found in `test/test_api.py`


# API Reference

Below documents the API endpoints. The API docs can also be accessed using FastAPI - SwaggerUI `http://127.0.0.1:8000/docs`.

**Available endpoints**

    [GET]  /analysis/sample -> View dataset samples
    [GET]  /analysis/basic_stats -> Summary statistics with filters
    [POST] /analysis/predict -> Predict resale prices using Random Forest

### /Sample 
Shows you a row by row sample of the dataset in a column:value format.  
- Accepts parameter of limit.  
    - Default value 1, minimum value 1, maximum value 10 


Result Example:

        [
            {
                "town": "ANG MO KIO",
                "flat_type": "2 ROOM",
                "block": "406",
                "street_name": "ANG MO KIO AVE 10",
                "floor_area_sqm": 44,
                "flat_model": "Improved",
                "lease_commence_date": "1979",
                "resale_price": "267000",
                "remaining_lease_years": 55.42,
                "storey_mid": 2,
                "year": 2023,
                "month_num": 1
            }
        ]

### /basic_stats

Shows basic summary statistic of the HDB resale prices.

Accepts a parameter of:
- town: str | None = Field(None, description="Filter by town")
- flat_type: str | None = Field(None, description="Filter by flat type")
- flat_model: str | None = Field(None, description="Type of flat model")
- floor_area_sqm: float | None = Field(None, description="Floor area in square meters")
- remaining_lease_years: int | None = Field(None, description="Remaining lease in years")
- storey_mid: int | None = Field(None, description="Mid storey level")
- year: int | None = Field(None, description="Year of transaction")
- month_num: int | None = Field(None, description="Month of transaction (numeric)")


Result Example:

    {
        "average_resale_price": "$ 657,143.85",
        "median_resale_price": "$ 645,000.00",
        "max_resale_price": "$ 1,208,000.00",
        "min_resale_price": "$ 150,000.00"
    }

### /predict

Uses a random forest prediction model to predict resale prices

Accepts a payload of:
- town: str = Field(None, description="Filter by town")
- flat_type: str = Field(None, description="Filter by flat type")
- flat_model: str = Field(None, description="Type of flat model")
- floor_area_sqm: float = Field(None, description="Floor area in square meters")
- remaining_lease_years: int = Field(None, description="Remaining lease in years")
- storey_mid: int = Field(None, description="Mid storey level")
- year: int = Field(None, description="Year of transaction")
- month_num: int = Field(None, description="Month of transaction (numeric)")

Result Example:

    [
        "Mean Absolute Error: 27285.42",
        "R Squared: 0.96",
        "Predicted Price: $763,679.80"
    ]
