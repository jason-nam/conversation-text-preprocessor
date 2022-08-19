import os
from typing import Dict, List, Optional
import re
import json

from tqdm import tqdm
from soynlp.normalizer import *
from kss import split_sentences
from multiprocessing import freeze_support


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


def split_sent_kss(sentence):
    """Split all sentences in utterance using kss library. 
    
    Return list of String type sentences."""

    freeze_support()
    return split_sentences(sentence)


def split_sent_connective(utterance):
    """Split sentences in utterance if sentences are connected 
    with common connective korean adverbs. 
    
    Return list of String type split sentences."""

    connective_adverbs = ["그럼", "그리고", "그래서"]

    # Find index locations.
    cut_ind = []
    for c_adv in connective_adverbs:
        for utterance_ind in range(0, len(utterance) - len(c_adv) + 1):
            if (
                utterance[
                    utterance_ind
                    :utterance_ind + len(c_adv)
                ] == c_adv
            ):
                cut_ind.append(utterance_ind)
    cut_ind.sort()

    if len(cut_ind) == 0:
        return [utterance]
    elif len(cut_ind) == 1:
        return [utterance[:cut_ind[0]], utterance[cut_ind[0]:]]
    else:
        split_utterance = [utterance[:cut_ind[0]]]
        for ind in range(len(cut_ind) - 1):
            split_utterance.append(
                utterance[
                    cut_ind[ind]
                    :cut_ind[ind+1]
                ]
            )
        split_utterance.append(utterance[cut_ind[-1]:])

        return split_utterance[1:] if split_utterance[0] == "" else split_utterance


def split_sent_onomatopoeia(utterance):
    """Split sentences in utterance if sentences are connected 
    with single letter Korean internet terminology in the form of onomatopoeia. 
    Terminology that are considered include 'ㅋ' that mimics natural laughter 
    and 'ㅎ' that mimics soft laughter. 
    
    Return list of String type split sentences."""

    split_utterance = split_sent_kss(utterance)
    split_sent = []

    for sent in split_utterance:
        onomatopoeia_beg = False
        cut_ind = 0
        for sent_ind in range(len(sent)):
            if (
                sent[sent_ind] == 'ㅋ' 
                or sent[sent_ind] == 'ㅎ'
            ):
                onomatopoeia_beg = True
            elif sent[sent_ind] == " ":
                continue
            else:
                if onomatopoeia_beg == True:
                    split_sent.append(sent[cut_ind:sent_ind])
                    cut_ind = sent_ind
                onomatopoeia_beg = False
        split_sent.append(sent[cut_ind:])
    return split_sent


def bisect_utterance_step_one(utterance):
    """Split utterance into two sentences. 
    
    Return two String utterances and boolean value indicating 
    success of split. If splitting utterance not applicable, 
    return back input utterance and boolean value 
    indicating failure of spit."""

    split_utterance = split_sent_kss(utterance)

    if len(split_utterance) == 1:
        return (False, utterance, utterance)

    top_utterance: str = ""
    bot_utterance: str = ""
    top_filled = False
    bot_filled = False

    while top_filled == False or bot_filled == False:
        if (
            not top_filled 
            and len(top_utterance + split_utterance[0]) >= 150
        ):
            top_filled = True
        else:
            top_utterance += split_utterance[0]
            del split_utterance[0]

        if len(split_utterance) <= 0:
            break

        if (
            not bot_filled 
            and len(bot_utterance + split_utterance[-1]) >= 150
        ):
            bot_filled = True
        else:
            bot_utterance += split_utterance[-1]
            del split_utterance[-1]
            if len(split_utterance) <= 0:
                break

    return (False, utterance, utterance) if (top_utterance == "" or bot_utterance == "") else (True, top_utterance, bot_utterance)


def bisect_utterance_step_two(utterance):
    """Split utterance into two sentences. 
    
    Return two String utterances and boolean value indicating success of split. 
    If splitting utterance not applicable, return back input utterance 
    and boolean value indicating failure of spit.
    
    Note: This function is only applicable when applying second step. 
    Refer to bisect_utterance_step_one function when applying first step."""

    split_utterance = split_sent_kss(utterance)

    first_split = []
    for sent in split_utterance:
        first_split += split_sent_connective(sent)

    sec_split = []
    for sent in first_split:
        sec_split += split_sent_onomatopoeia(sent)

    split_utterance = sec_split

    if len(split_utterance) == 1:
        return (False, utterance, utterance)

    top_utterance: str = ""
    bot_utterance: str = ""
    top_filled = False
    bot_filled = False

    while top_filled == False or bot_filled == False:
        if (
            not top_filled 
            and len(top_utterance + split_utterance[0]) >= 150
        ):
            top_filled = True
        else:
            top_utterance += split_utterance[0]
            del split_utterance[0]

        if len(split_utterance) <= 0:
            break

        if (
            not bot_filled 
            and len(bot_utterance + split_utterance[-1]) >= 150
        ):
            bot_filled = True
        else:
            bot_utterance += split_utterance[-1]
            del split_utterance[-1]
            if len(split_utterance) <= 0:
                break

    return (False, utterance, utterance) if (top_utterance == "" or bot_utterance == "") else (True, top_utterance, bot_utterance)


def bisect_conv_step_one(conv) -> Optional[list]:
    """Split conversation into groups by cutting conversation when an 
    utterance with char length greater than 150 is divisible. 
    Organize groups and apply appropriate identifications. 

    Return list that has utterances that have char length greater 
    han 150 bisected. If split not applicable, then return None."""

    split_conv = []

    for utterance in conv:
        if len(utterance["utterance"]) >= 150:
            is_split, top, bot = bisect_utterance_step_one(utterance["utterance"])
            # result = bisect_utterance_step_one(utterance["utterance"])
            if is_split == False:
                # return -1
                return None
                
            top_conv = {}
            top_conv["id"] = utterance["id"] + ".1"
            top_conv["speaker_id"] = utterance["speaker_id"]
            top_conv["utterance"] = top
            split_conv.append(top_conv)

            bot_conv = {}
            bot_conv["id"] = utterance["id"] + ".2"
            bot_conv["speaker_id"] = utterance["speaker_id"]
            bot_conv["utterance"] = bot
            split_conv.append(bot_conv)
    
        else:   
            split_conv.append(utterance)

    return split_conv


def bisect_conv_step_two(conv):
    """Split conversation into groups by cutting conversation 
    when an utterance with char length greater than 150 is divisible.
    Organize groups and apply appropriate identifications. 
    
    Return list that has utterances that have char length greater 
    than 150 bisected. If split not applicable, then return None.
    
    Note: This bisection is only applicable when applying second step. 
    Refer to bisect_conv_step_one function when applying first step."""

    split_conv =[]

    for utterance in conv:
        if len(utterance["utterance"]) >= 150:
            is_split, top, bot = bisect_utterance_step_two(utterance["utterance"])
            if is_split == False:
                # return -1
                return None

            top_conv = {}
            top_conv["id"] = utterance["id"] + ".1"
            top_conv["speaker_id"] = utterance["speaker_id"]
            top_conv["utterance"] = top
            split_conv.append(top_conv)

            bot_conv = {}
            bot_conv["id"] = utterance["id"] + ".2"
            bot_conv["speaker_id"] = utterance["speaker_id"]
            bot_conv["utterance"] = bot
            split_conv.append(bot_conv)
    
        else:   
            split_conv.append(utterance)

    return split_conv


def bisect_conv_step_three(conv):
    """Split conversation into groups by cutting conversation 
    when an utterance with char length greater than 150 is divisible. 
    Organize groups and apply appropriate identifications. 

    Return list that has utterances that have char length 
    greater than 150 bisected. If split not applicable, 
    then return None.
    
    Note: This bisection is only applicable when applying third step. 
    Refer to bisect_conv_step_one function when applying first step 
    or bisect_conv_step_two function when applying second step."""

    cut_ind = []
    copy_json_file = []
    split_conv = []
    null_info = {}

    for i, utterance in enumerate(conv):

        if len(utterance["utterance"]) >= 150:
            null_info = {}
            copy_json_file.append(null_info)
            cut_ind.append(i)
        else:
            copy_json_file.append(utterance)

    while copy_json_file[0] == null_info:  
        copy_json_file = copy_json_file[1:]

    while copy_json_file[-1] == null_info:
        copy_json_file = copy_json_file[:-1]
        
    temp = []
    copy_json_file = conv

    while len(copy_json_file) > 0:

        if len(copy_json_file) == 1:
            if copy_json_file[0] == {}:
                split_conv.append(temp)
                break
            else:
                temp.append(copy_json_file[0])
                split_conv.append(temp)
                break

        if copy_json_file[0] != {}:
            temp.append(copy_json_file[0])
            del copy_json_file[0]
            continue
        else:
            split_conv.append(temp)
            temp = []
            del copy_json_file[0]
            continue

    return split_conv


def split_file(conv):
    """Split data into top and bottom datasets. Cut along utterances
    that have been split previously. 
    
    Return list that contains nested dataset lists for each json file 
    to be generated."""

    split_files = []
    cut_file_ind = []
    hold = False

    for ind, utterance in enumerate(conv):
        if hold:
            hold = False
            continue
        if utterance["id"].count(".") == 3:
            cut_file_ind.append(ind + 1)
            hold = True

    split_files.append(conv[:cut_file_ind[0]])
    for i in range(len(cut_file_ind) - 1):
        split_files.append(conv[cut_file_ind[i]:cut_file_ind[i + 1]])    
    split_files.append(conv[cut_file_ind[-1]:])

    return split_files


def filter_long_sent(conv_data):
    
    # First step
    split_conv_one = bisect_conv_step_one(conv_data)
    if split_conv_one != None:
        split_conv_data = split_file(split_conv_one)
        return 1, split_conv_data

    # Second step
    split_conv_two = bisect_conv_step_two(conv_data)
    if split_conv_two != None:
        split_conv_data = split_file(split_conv_two)
        return 2, split_conv_data

    # Third step
    split_conv_three = bisect_conv_step_three(conv_data)
    return 3, split_conv_three


def main():
    # Iterate through root dir to get list of dir names.
    dirlist = get_dirnames(source_data_path)

    # Iterate over dir from root dir.
    for dirname in dirlist:
        flist = get_filenames(path=os.path.join(source_data_path, dirname)) # Load list of file names from dir.
        long_exception = "long_data"
        eng_exception = "eng_data"
        transformed_exception = "transformed_data"
        deleted_data = "deleted_data"
        single_utterance_data = "single_utterance_data"
        data_count = len(flist)
        remaining_data_count = 0
        destroyed_data_count = 0
        long_data_count = 0

        if not os.path.exists(os.path.join(new_data_path, long_exception)):
            os.mkdir(os.path.join(new_data_path, long_exception)) # Make dir if target dir does not exist.
            print(f"Directory \"{os.path.join(new_data_path, long_exception)}\" generated.")

        # if not os.path.exists(os.path.join(new_data_path, eng_exception)):
        #     os.mkdir(os.path.join(new_data_path, eng_exception)) # Make dir if target dir does not exist.
        #     print(f"Directory \"{os.path.join(new_data_path, eng_exception)}\" generated.")

        # if not os.path.exists(os.path.join(new_data_path, transformed_exception)):
        #     os.mkdir(os.path.join(new_data_path, transformed_exception)) # Make dir if target dir does not exist.
        #     print(f"Directory \"{os.path.join(new_data_path, transformed_exception)}\" generated.")

        if not os.path.exists(os.path.join(new_data_path, deleted_data)):
            os.mkdir(os.path.join(new_data_path, deleted_data)) # Make dir if target dir does not exist.
            print(f"Directory \"{os.path.join(new_data_path, deleted_data)}\" generated.")

        if not os.path.exists(os.path.join(new_data_path, single_utterance_data)):
            os.mkdir(os.path.join(new_data_path, single_utterance_data)) # Make dir if target dir does not exist.
            print(f"Directory \"{os.path.join(new_data_path, single_utterance_data)}\" generated.")

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

                if is_long:
                    step, split_df = filter_long_sent(conv_data=df)
                    for ind, df_iter in enumerate(split_df):
                        if len(df_iter) < 2:
                            write_json(
                                data=df_iter, 
                                dirname=single_utterance_data, 
                                filename=filename[:-5]+"_"+repr(ind)+".json"
                            )
                        else:
                            write_json(
                                data=df_iter, 
                                dirname=dirname, 
                                filename=filename[:-5]+"_"+repr(ind)+".json"
                            )
                            remaining_data_count += 1

                            write_json(
                                data=df_iter, 
                                dirname=long_exception, 
                                filename=filename[:-5]+"_"+repr(ind)+".json"
                            )
                            long_data_count += 1
                else:
                    #
                    write_json(
                        data=df, 
                        dirname=dirname, 
                        filename=filename
                    )
                    remaining_data_count += 1
            
                # # Write conversation json file to english exceptions dir for further analysis if is_eng is True.
                # if is_eng:
                #     write_json(
                #         data=df, 
                #         dirname=eng_exception, 
                #         filename=filename
                #     )
                # # Not implemented yet.
                # if transformed:
                #     #
                #     write_json(
                #         data=df, 
                #         dirname=transformed_exception, 
                #         filename=filename
                #     )
            else:
                write_json(
                    data=df, 
                    dirname=deleted_data, 
                    filename=filename
                )
                destroyed_data_count += 1

        # Print result of each dir conversation filters.
        print (
            f'DIRECTORY: {dirname}\n'
            f'TOTAL DATA: {data_count}\n'
            f'FILTERED DATA: {destroyed_data_count}\n'
            f'REMAINING AND SPLIT DATA: {remaining_data_count}\n'
            f'LONG DATA: {long_data_count}\n'
        )


if __name__ == "__main__":
    main()