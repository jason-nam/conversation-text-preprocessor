import pandas as pd
from pathlib import Path
import json

FROM_PATH = Path('../data/multiturn_data/source_data')
TO_PATH = Path('../data/multiturn_data/filtered_data')
COLUMN_NAMES = ['index', 'dialogue_id', 'Q-3', 'Q-2', 'Q-1', 'A']

def read_json(filename):
    with open(FROM_PATH/filename, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    out_file = open(TO_PATH/filename, "w", encoding = 'utf-8')
    json.dump(data, out_file, indent = 2, sort_keys = False, ensure_ascii=False)
    # print('Generated', filename)
    out_file.close()

if __name__ == "__main__":
    None