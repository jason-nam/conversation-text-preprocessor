import data_util
from filter_logic import is_bad_conversation

import pathlib

def get_filenames(path):
    flist = []
    for p in pathlib.Path(path).iterdir():
        if p.is_file():
            flist.append(p.name)
    return flist

def main():
    flist = get_filenames('../data/unfiltered_file')
    # filtered_flist = get_filenames('../data/filtered_file')
    # flist = [x for x in flist if x not in filtered_flist]

    for file in flist:
        df = data_util.get_data(file)
        delete_rows = []

        for i, row in df.iterrows():
            if is_bad_conversation(row):
                delete_rows.append(i)

        df = data_util.drop_row(df, delete_rows)
        print(len(delete_rows), 'rows deleted.')

        data_util.write_data(df, file)
        print(file, 'generated')

if __name__ == "__main__":
    main()