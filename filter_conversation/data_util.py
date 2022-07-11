import pandas as pd
from pathlib import Path

FROM_PATH = Path('../data/unfiltered_file')
TO_PATH = Path('../data/filtered_file')
COLUMN_NAMES = ['index', 'dialogue_id', 'Q-3', 'Q-2', 'Q-1', 'A']

def get_data(file_name):
    path = FROM_PATH/file_name
    df = pd.read_csv(path)
    return df

def drop_row(df, ind):
    df = df.drop(df.index[ind])
    return df

def write_data(df, file_name):
    path = TO_PATH/file_name
    df.to_csv(path, index=False, header=COLUMN_NAMES)

def is_null(var):
    return pd.isnull(var)

if __name__ == "__main__":
    None