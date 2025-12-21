import requests
import json
import pandas as pd

url = "http://127.0.0.1:8000/"

end_point_1 = "/analysis/trend"

params = {
    "town": "TAMPINES",
    "flat_type": "5 ROOM",
    # "flat_model": "Improved",
    # "floor_area_sqm": 105.0,
    # "remaining_lease_years": 720,
    # "storey": 34,
    # "year": 2025,
    # "month_num": 5
}

# test_1 = requests.get(url + end_point_1, params=params).json()
# print(json.dumps(test_1, indent=4))

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 

end_point_2 = "/analysis/predict"
payload = {
    "town": "TAMPINES",
    "flat_type": "5 ROOM",
    "flat_model": "Model A",
    "floor_area_sqm": 110.0,
    "remaining_lease_years": 90,
    "storey": 10,
    "year": 2026,
    "month_num": 1
}

test_2 = requests.post(url + end_point_2, json=payload).json()
print(json.dumps(test_2, indent=4))