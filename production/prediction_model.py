from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import data

trained_model: None
X_test: None
y_test: None

def train_model(df_model: pd.DataFrame):

    X = df_model.drop(columns=["resale_price"])
    y = df_model["resale_price"]

    # Train-test split (random; for forecasting you may prefer time-based split)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
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
    trained_model = pipeline.fit(X_train, y_train)
    
    return trained_model, X_test, y_test

def predict_future_price(town: str, flat_type: str, flat_model: str, 
                         floor_area_sqm: float, remaining_lease_years: int,
                         storey: int, year: int, month_num: int):
     
     # Evaluate
     preds = trained_model.predict(X_test)
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
