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
    [GET]  /analysis/summary_stats -> Summary statistics with filters
    [GET]  /analysis/trend -> Shows last 12 month resale prices
    [POST] /analysis/predict -> Predict resale prices using Random Forest

## analysis/sample
Method: [GET] <br>
Description: Return a row-by-row sample of the dataset.<br>

Optional filters:
`LIMIT` : int
- Default: 1
- Min: 1
- Max: 10


Example Output: 

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
                "storey": 2,
                "year": 2023,
                "month_num": 1
            }
        ]

## analysis/summary_stats

Method: [GET] <br>
Description: Shows summary statistic of HDB resale prices.<br>


Optional filters:

- `town` : str
- `flat_type` : str
- `flat_model` : str
- `floor_area_sqm` : float
- `remaining_lease_years` : int
- `storey` : int
- `year` : int
- `month_num` : int


Example Output:

    {
        "average_resale_price": "$ 657,143.85",
        "median_resale_price": "$ 645,000.00",
        "max_resale_price": "$ 1,208,000.00",
        "min_resale_price": "$ 150,000.00"
    }

## analysis/trend

Mehod: [GET] <br>
Description: Shows last 12 months average resale prices.<br>

Optional filters:

- `town` : str
- `flat_type` : str
- `flat_model` : str
- `floor_area_sqm` : float
- `remaining_lease_years` : int
- `storey` : int

Example Output:

        [
            {
                "month": "2025-01-01",
                "resale_price": "44,911,664.00"
            },
            {
                "month": "2025-02-01",
                "resale_price": "37,951,768.00"
            },
            {
            .
            .
            .    
            },
            {
                "month": "2025-11-01",
                "resale_price": "28,248,776.00"
            },
            {
                "month": "2025-12-01",
                "resale_price": "26,904,328.00"
            }
        ]

## analysis/predict

Method: [POST] <br>
Description: Predicts resale prices using a Random Forest model.<br>

Payload required:
- `town` : str
- `flat_type` : str
- `flat_model` : str
- `floor_area_sqm` : float
- `remaining_lease_years` : int
- `storey` : int
- `year` : int
- `month_num` : int


Example Output:

    {
        "Predicted Price": "$807,174.79",
        "Mean Absolute Error": "$29,362.30",
        "R Squared": "0.95"
    }
