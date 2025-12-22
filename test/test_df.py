import pandas as pd
from production.data import *

hdb_resale_data = load_hdb_resale_data()
print(hdb_resale_data.sample(5))
print(hdb_resale_data.info())
