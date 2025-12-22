import pandas as pd
from production.data import *

hdb_resale_data = load_hdb_resale_data()
print(hdb_resale_data.head(5))
