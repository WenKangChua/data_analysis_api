from fastapi import FastAPI
from contextlib import asynccontextmanager
from api_analysis import router as analysis_router
import data
import prediction_model as pm

# startup #
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Type of hdb_resale_data:", type(data.hdb_resale_data))
    data.hdb_resale_data = data.load_hdb_resale_data()
    pm.trained_model, pm.x_test, pm.y_test = pm.train_model(data.hdb_resale_data)
    print("Data loaded into DataFrame at startup!")
    print("Type of hdb_resale_data:", type(data.hdb_resale_data))
    yield
    print("app shutting down")

# Create the FastAPI app
app = FastAPI(lifespan=lifespan)

# Include routes from api.py
app.include_router(analysis_router)

@app.get("/")
def root():
    return {"message": "Welcome to the wenkang's API"}

