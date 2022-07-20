def print_progress(file_name, deteleted_rows_len):
    file_name = '[' + file_name + ']'
    print(
            file_name, 'filtered :',
            deteleted_rows_len, 'rows deleted',
    )

def print_result(data, filtered_data):
    # print_label()
    print(
            '\nTotal data:', data,
            '\nFiltered data:', filtered_data,
            '\nRemaining data:', data - filtered_data
    )

def print_label():
    print(r"""\ 

            """                 
    )