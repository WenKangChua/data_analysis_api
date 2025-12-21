import requests
import json
import pandas as pd

url = "http://127.0.0.1:8000/"

# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
end_point_1 = "/analysis/sample"
params_1 = {
    "limit": 2
}
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
end_point_2 = "/analysis/summary_stats"
params_2 = {
    # "town": "TAMPINES",
    # "flat_type": "5 ROOM",
    # "flat_model": "Improved",
    # "floor_area_sqm": 105.0,
    # "remaining_lease_years": 720,
    # "storey": 12,
    "year": 2025,
    "month_num": 11
}
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
end_point_3 = "/analysis/trend"
params_3 = {
    "town": "TAMPINES",
    "flat_type": "5 ROOM",
    # "flat_model": "Improved",
    # "floor_area_sqm": 105.0,
    # "remaining_lease_years": 720,
    # "storey": 34
}
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 
end_point_4 = "/analysis/predict"
payload_4 = {
    "town": "TAMPINES",
    "flat_type": "5 ROOM",
    "flat_model": "Model A",
    "floor_area_sqm": 110.0,
    "remaining_lease_years": 90,
    "storey": 10,
    "year": 2026,
    "month_num": 3
}
# ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- 

# /analysis/sample
sample = requests.get(url + end_point_1, params=params_1).json()
print("sample:")
print(json.dumps(sample, indent=4))
print("\n")

# /analysis/summary_stats
summary_stats = requests.get(url + end_point_2, params=params_2).json()
print("summary_stats:")
print(json.dumps(summary_stats, indent=4))
print("\n")

# /analysis/trend
trend = requests.get(url + end_point_3, params=params_3).json()
print("trend:")
print(json.dumps(trend, indent=4))
print("\n")

# /analysis/predict
predict = requests.post(url + end_point_4, json=payload_4).json()
print("predict:")
print(json.dumps(predict, indent=4))