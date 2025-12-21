import requests
import pandas as pd

hdb_resale_data: pd.DataFrame | None = None

def generate_months(year):
    return [f'{{"month": "{year}-{m:02d}"}}' for m in range(1, 13)]

def calculate_storey_upper(storey: int):
    # HDB resale data contains storey ranges in multiples of 3, etc 01 TO 03, 04 TO 06.
    # This function will calculate the upper range of the storey.
    # For eg, user input 4, return 6.

    # mod == 1, lower range. mod == 2, mid range. mod == 3, upper range
    mod = storey % 3
    if mod == 0:
        storey_upper = storey
    else:
        storey_upper = 3 - mod + storey

    return storey_upper

def load_hdb_resale_data():
    #hdb resales flat prices dataset
    url = "https://data.gov.sg/api/action/datastore_search"
    all_records = []

    limit = 500

    # years = [2023,2024,2025]
    years = [2025]
    months = []
    for y in years:
        months.extend(generate_months(y))

    for month in months:
        offset = 0
        while True:
            records = []
            params = {
                "resource_id": "d_8b84c4ee58e3cfc0ece0d773c8ca6abc",
                "limit": limit,
                "offset": offset,
                "filters": month
            }

            response = requests.get(url, params=params).json()
            records = response["result"]["records"]

            if not records:
                break
            
            all_records.extend(records)
            offset += limit


    df = pd.DataFrame(all_records)
    
    # convert resale_price to numeric
    df["resale_price"] = pd.to_numeric(df["resale_price"])

    # extract years from remaining lease
    df["remaining_lease_years"] = (df["remaining_lease"].str.extract(r'(\d+) years')
                                   .fillna(0).astype(int))
    
    # extract months from remaining lease
    df["remaining_lease_months"] = (df["remaining_lease"].str.extract(r'(\d+) months')
                                    .fillna(0).astype(int)) / 12
    
    # add lease years(months) into lease months
    df["remaining_lease_years"] = (df["remaining_lease_months"] + df["remaining_lease_years"]).round(2)
    
    # extract upper range from storey_range
    df["storey"] = df['storey_range'].str.extract(r' TO (\d+)').astype(int)
                       
    
    # convert floor area sqm to float
    df["floor_area_sqm"] = df["floor_area_sqm"].astype(float)

    # extract month and year
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m")
    df["year"] = df["month"].dt.year
    df["month_num"] = df["month"].dt.month
    
    df = df.drop(columns=["_id","remaining_lease","storey_range","remaining_lease_months"])

    return df
