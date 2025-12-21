import pandas as pd

def query_sample_data(df: pd.DataFrame, limit: int):
    sample_data = df.head(limit)
    return sample_data

def calculate_median_price(df: pd.DataFrame, column: str):
    df[column] = df[column].astype(float)
    result = df[column].median()
    return result

def calculate_average_price(df: pd.DataFrame, column: str):
    df[column] = df[column].astype(float)
    result = df[column].mean()
    return result

def calculate_min_price(df: pd.DataFrame, column: str):
    df[column] = df[column].astype(float)
    result = df[column].min()
    return result

def calculate_max_price(df: pd.DataFrame, column: str):
    df[column] = df[column].astype(float)
    result = df[column].max()
    return result

def calculate_last_n_month_mean_resale_prices(df: pd.DataFrame, month_offset: int, month_column: str):
    max_date = df[month_column].max()
    min_date = max_date - pd.DateOffset(months = month_offset)
    df = df[df[month_column] > min_date]
    result = (df.groupby(month_column)["resale_price"]
            .mean() 
            .reset_index())

    return result

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

