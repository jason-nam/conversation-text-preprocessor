import csv_handler
from filter_logic import is_bad_conversation

FILE_NAME = '7_dialogue_id_filter_double_turn.csv'

def main():
    df = csv_handler.get_data(FILE_NAME)
    delete_rows = []

    for i, row in df.iterrows():
        if is_bad_conversation(row):
            delete_rows.append(i)

    df = csv_handler.drop_row(df, delete_rows)
    print(len(delete_rows), 'rows deleted.')

    csv_handler.write_data(df, FILE_NAME)

if __name__ == "__main__":
    main()