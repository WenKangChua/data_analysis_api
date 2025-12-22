# To look at values/info in DF

import pandas as pd
from production.data import *

hdb_resale_data = load_hdb_resale_data()
# hdb_sort = hdb_resale_data.sort_values(by="month", ascending=True)
# print(hdb_sort.head())
# print(hdb_resale_data.info())
# print(len(hdb_resale_data))

result = hdb_resale_data.query("town == 'TAMPINES' and flat_type == '5 ROOM'")
print(result)
