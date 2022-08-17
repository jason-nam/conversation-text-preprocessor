import os
from typing import Dict, List
import re
import json

from tqdm import tqdm
from soynlp.normalizer import *

term_size = os.get_terminal_size()
_dir = os.path.dirname(os.path.abspath(__file__))
source_data_path = os.path.join(_dir, "../data/multiturn_data/source_data") # Path of source data.
new_data_path = os.path.join(_dir, "../data/multiturn_data/filtered_data") # Path of filtered data.
single_letter_dict_path = os.path.join(_dir, "single_letter_terms.txt") # Single letter Dict path.
special_characters_dict_path = os.path.join(_dir, "special_characters.txt") # Special characters List path.


def get_dirnames(path):
    """Get all directory names within the designated directory path. Return a list of all directory names."""
    dirlist = []
    try:
        for dirname in os.listdir(path):
            if os.path.isdir(os.path.join(path, dirname)):
                dirlist.append(dirname)
    except:
        print(f"\"{path}\" does not exist")
        raise
    return dirlist


def get_filenames(path):
    """Get all file names within the designated directory path. Return a list of all file names."""
    flist = []
    try:
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                flist.append(filename)
    except:
        print(f"\"{path}\" does not exist")
        raise
    return flist


def read_json(path):
    """Read .json file in designated path. Return dataset."""
    try:
        with open(path, 'r', encoding='utf-8-sig') as file:
            data = json.load(file)
    except:
        print(f"\"{path}\" does not exist")
        raise
    return data


def write_json(data, dirname, filename):
    """Generate .json file in designated directory."""
    if not os.path.exists(os.path.join(new_data_path, dirname)):
        print(f"\"{os.path.join(new_data_path, dirname)}\" path does not exist")
    # Write conversation json file. 
    try:
        out_file = open(os.path.join(new_data_path, dirname, filename), "w", encoding = 'utf-8')
        json.dump(
            data, 
            out_file, 
            indent = 2, 
            sort_keys = False, 
            ensure_ascii=False
        )
        out_file.close()
    except: # Failed to write conversation json file.
        print(f"\"{dirname}\" failed to generate.")
        raise


def load_dictionary(path):
    """Read dictionary from .txt file. Return dictionary."""
    result = {}
    try:
        with open(path, 'r', encoding="utf8") as file:
            for line in file.readlines():
                try:
                    key = line.split()[0]
                    value = line.split()[1]
                    result[key] = str(value).strip()
                except Exception as e:
                    pass
    except:
        print(f"\"{path}\" does not exist")
        raise
    return result


def load_list(path):
    """Read list from .txt file. Return list."""
    result = []
    try:
        with open(path, 'r', encoding="utf8") as file:
            for line in file.readlines():
                try:
                    for c in line.strip().split(" "):
                        result.append(c)
                except Exception as e:
                    pass
    except:
        print(f"\"{path}\" does not exist")
        raise
    return result


# Dict containing single letter characters and their pre-determined allowed consecutive length.
SINGLE_LETTER_TERMS: Dict[str, str] = load_dictionary(single_letter_dict_path)
if SINGLE_LETTER_TERMS == {}: # Failed to load dictionary txt file that contains list of single letter characters.
    print(f"Failed to load \"{single_letter_dict_path}\"")
    raise

# List containing special characters to be removed within utterance.
SPECIAL_CHARACTERS: List[str] = load_list(special_characters_dict_path)
if SPECIAL_CHARACTERS == []: # Failed to load dictionary txt file that contains list of special characters.
    print(f"Failed to load \"{special_characters_dict_path}\"")
    raise


def adjust_character_length(utterance, target, repeat_max):
    """Function that adjusts lenght of single letter characters from the Korean Alphabet.
    Returns modified utterance that has single letter characters in pre-set consecutive lenghts."""
    count = 0
    del_ind = []
    for ind, c in enumerate(utterance):
        if c == target:
            count += 1
            # Append to delete index list to be processed later if certain single letter character has been repeated consecutively for more than repeat_max times.
            if count > repeat_max:
                del_ind.append(ind)
        elif c == ' ': # Ignore spaces between single letter characters. Repetition is not disturbed by spaces in sentence.
            continue
        else:
            count = 0
    for i in reversed(del_ind): # Modify sentence from last to first characters.
        utterance = utterance[0:i] + utterance[i+1:]
    return utterance


def remove_special_characters(utterance, illegal_characters):
    """Function that removes any special characters in utterance sentence.
    Returns filtered utterance that is stripped of all special characters."""
    for illegal_char in illegal_characters:
        utterance = utterance.replace(illegal_char, '')
    return utterance
    

def is_short_utterance(utterance, min_utterance_len):
    """Function that checks length of utterance sentence.
    Returns True if length of utterance is less than 5, else returns False."""
    if len(str(utterance)) <= min_utterance_len:
        return True
    return False


def is_long_utterance(utterance, max_utterance_len):
    """Function that checks length of utterance sentence.
    Returns True if length of utterance is greater than 150, else returns False."""
    if len(str(utterance)) >= max_utterance_len:
        return True
    return False


def main():
    # Iterate through root dir to get list of dir names.
    dirlist = get_dirnames(source_data_path)

    # Iterate over dir from root dir.
    for dirname in dirlist:
        flist = get_filenames(path=os.path.join(source_data_path, dirname)) # Load list of file names from dir.
        long_exception = "long_exceptions"
        eng_exception = "eng_exceptions"
        transformed_exception = "transformed_exceptions"
        deleted_data = "deleted_data"
        data_count = len(flist)
        remaining_data_count = 0
        long_data_count = 0

        if not os.path.exists(os.path.join(new_data_path, long_exception)):
            os.mkdir(os.path.join(new_data_path, long_exception)) # Make dir if target dir does not exist.
            print(f"Directory \"{os.path.join(new_data_path, long_exception)}\" generated.")

        if not os.path.exists(os.path.join(new_data_path, eng_exception)):
            os.mkdir(os.path.join(new_data_path, eng_exception)) # Make dir if target dir does not exist.
            print(f"Directory \"{os.path.join(new_data_path, eng_exception)}\" generated.")

        if not os.path.exists(os.path.join(new_data_path, transformed_exception)):
            os.mkdir(os.path.join(new_data_path, transformed_exception)) # Make dir if target dir does not exist.
            print(f"Directory \"{os.path.join(new_data_path, transformed_exception)}\" generated.")

        if not os.path.exists(os.path.join(new_data_path, deleted_data)):
            os.mkdir(os.path.join(new_data_path, deleted_data)) # Make dir if target dir does not exist.
            print(f"Directory \"{os.path.join(new_data_path, deleted_data)}\" generated.")

        if not os.path.exists(os.path.join(new_data_path, dirname)):
            os.mkdir(os.path.join(new_data_path, dirname)) # Make dir if target dir does not exist.
            print(f"Directory \"{os.path.join(new_data_path, dirname)}\" generated.")

        print(dirname)

        # Iterate over files in dir.
        for filename in tqdm(flist):
            short_utterance_count = 0
            remove_data = False
            is_eng = False
            contains_special_char = False
            is_long = False
            transformed = False

            # Load json conversation file.
            df = read_json(path=os.path.join(
                source_data_path, 
                dirname, 
                filename
            )) 

            for ind in range(len(df)):
                # Adjust lenght of single letter terms that represent emotions in Korean Language.
                for key in SINGLE_LETTER_TERMS:
                    df[ind]['utterance'] = adjust_character_length(
                        utterance=df[ind]['utterance'], 
                        target=key, 
                        repeat_max=int(SINGLE_LETTER_TERMS[key])
                    )

                # Replace all "OO님" sequence with "당신" if conversation is from AIHub.
                if df[ind]['id'].startswith("감성대화말뭉치"):
                    df[ind]['utterance'] = df[ind]['utterance'].replace("OO님", "당신")

                # Remove special characters from utterance.
                df[ind]['utterance'] = only_text(df[ind]['utterance'])

                # Identify if utterance contains english characters.
                if bool(re.search("[a-zA-Z]", df[ind]['utterance'])):
                    is_eng = True

                # Remove conversation if length of utterances in a conversation is less than 5 characters long for 3 consecutive utterances.
                if is_short_utterance(
                    utterance=df[ind]['utterance'], 
                    min_utterance_len=5
                ):
                    short_utterance_count += 1
                    if short_utterance_count == 3:
                        remove_data = True
                        break
                else:
                    short_utterance_count = 0

                if is_long_utterance(
                    utterance=df[ind]['utterance'],
                    max_utterance_len=150
                ):
                    is_long = True

            # Write conversation json files if remove_data is False.
            if not remove_data:
                remaining_data_count += 1
                #
                write_json(
                    data=df, 
                    dirname=dirname, 
                    filename=filename
                )
                #
                if is_long:
                    long_data_count += 1
                    #
                    write_json(
                        data=df, 
                        dirname=long_exception, 
                        filename=filename
                    )
            
                # Write conversation json file to english exceptions dir for further analysis if is_eng is True.
                if is_eng:
                    write_json(
                        data=df, 
                        dirname=eng_exception, 
                        filename=filename
                    )
                # Not implemented yet.
                if transformed:
                    #
                    write_json(
                        data=df, 
                        dirname=transformed_exception, 
                        filename=filename
                    )
            else:
                write_json(
                    data=df, 
                    dirname=deleted_data, 
                    filename=filename
                )

        # Print result of each dir conversation filters.
        print (
            f'DIRECTORY: {dirname}\n',
            f'TOTAL DATA: {data_count}\n', 
            f'FILTERED DATA: {data_count - remaining_data_count}\n', 
            f'REMAINING DATA: {remaining_data_count}\n', 
            f'LONG DATA: {long_data_count}\n', 
        )


if __name__ == "__main__":
    main()