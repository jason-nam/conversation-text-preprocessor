import data_util
import util
import pathlib
from filter_conditions import is_bad_conversation

PATH = '../data/unfiltered_file'
flist_ = ['7_dialogue_id_filter_double_turn.csv']

def get_filenames(path):
    flist = []
    for p in pathlib.Path(path).iterdir():
        if p.is_file():
            flist.append(p.name)
    return flist

def get_delete_rows(df):
    delete_rows = []
    for i, row in df.iterrows():
        if is_bad_conversation(row):
            delete_rows.append(i)
    return delete_rows

def main():
    flist = get_filenames(PATH)

    data_count = 0
    filtered_data_count = 0

    for file in flist:
        df = data_util.get_data(file)
        delete_rows = get_delete_rows(df)
        data_count += len(df)
        filtered_data_count += len(delete_rows)
        df = data_util.drop_row(df, delete_rows)
        data_util.write_data(df, file)
        util.print_progress(file, len(delete_rows))
    util.print_result(data_count, filtered_data_count)

if __name__ == "__main__":
    main()