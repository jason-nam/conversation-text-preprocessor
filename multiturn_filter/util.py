def print_progress(file_name, deteleted_rows_len):
    file_name = '[' + file_name + ']'
    print(
            file_name, 'FILTERED: ',
    )

def print_result(dir, data, filtered_data):
    # print_label()
    print(  
            '\nDIRECTORY:', dir,
            '\nTOTAL DATA:', data,
            '\nFILTERED DATA:', data - filtered_data,
            '\nREMAINING DATA:', filtered_data
    )

if __name__ == "__main__":
    None
