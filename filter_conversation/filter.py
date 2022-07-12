import data_util
import pathlib
from filter_conditions import is_bad_conversation

def get_filenames(path):
    flist = []
    for p in pathlib.Path(path).iterdir():
        if p.is_file():
            flist.append(p.name)
    return flist

flist_ = ['7_dialogue_id_filter_double_turn.csv']

def main():
    flist = get_filenames('../data/unfiltered_file')
    # filtered_flist = get_filenames('../data/filtered_file')
    # flist = [x for x in flist if x not in filtered_flist]

    data_count = 0
    filtered_data_count = 0

    for file in flist_:
        df = data_util.get_data(file)
        delete_rows = []

        data_count += len(df)

        for i, row in df.iterrows():
            if is_bad_conversation(row):
                delete_rows.append(i)

        df = data_util.drop_row(df, delete_rows)
        print(len(delete_rows), 'rows deleted.')

        data_util.write_data(df, file)
        print(file, 'generated')

        
        filtered_data_count += len(delete_rows)
    
    print('Total data:', data_count)
    print('Filtered data:', filtered_data_count)
    print('Remaining data:', data_count - filtered_data_count)

if __name__ == "__main__":
    main()