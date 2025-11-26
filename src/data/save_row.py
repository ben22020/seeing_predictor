import pandas as pd
import os

file_path = "src/data/seeing_weather_data.csv"

def save_row(df: pd.DataFrame):
    if not os.path.isfile(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)