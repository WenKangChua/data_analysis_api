from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd

trained_model: None
x_test: None
y_test: None

def percentage_train_test_split(df: pd.DataFrame, percentage_train: float):
     df = df.sort_values(by="month", ascending=False)
     split_df_cutoff = int(len(df) * percentage_train)

     train = df.iloc[:split_df_cutoff]
     test = df.iloc[split_df_cutoff:]

     x_train = train.drop(columns="resale_price")
     y_train = train["resale_price"]

     x_test = test.drop(columns="resale_price")
     y_test = test["resale_price"]

     return x_train, x_test, y_train, y_test

def train_model(df_model: pd.DataFrame):

    x_train, x_test, y_train, y_test = percentage_train_test_split(
         df_model, percentage_train=0.8
    )

    categorical = ["town", "flat_type", "flat_model"]
    numeric = ["floor_area_sqm", "remaining_lease_years", "storey", "year", "month_num"]

    preprocess = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", "passthrough", numeric)
    ])

    # Random Forest model
    rf_model = RandomForestRegressor(
        n_estimators=600,       # number of trees
        max_depth=None,         # let trees grow fully
        min_samples_split=10,   # control overfitting
        random_state=42,
        n_jobs=-1               # use all CPU cores
    )

    pipeline = Pipeline([("prep", preprocess), ("model", rf_model)])
    trained_model = pipeline.fit(x_train, y_train)
    
    return trained_model, x_test, y_test

def predict_future_price(town: str, flat_type: str, flat_model: str, 
                         floor_area_sqm: float, remaining_lease_years: int,
                         storey: int, year: int, month_num: int):
     
     # Evaluate
     preds = trained_model.predict(x_test)
     mae = mean_absolute_error(y_test, preds)
     r_square = r2_score(y_test, preds)

     parameters = pd.DataFrame([{
        "town": town,
        "flat_type": flat_type,
        "flat_model": flat_model,
        "floor_area_sqm": floor_area_sqm,
        "remaining_lease_years": remaining_lease_years,
        "storey": storey,
        "year": year,
        "month_num": month_num
     }])

     result = trained_model.predict(parameters)[0]

     return result, mae, r_square
