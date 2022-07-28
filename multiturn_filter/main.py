import os
from soynlp.normalizer import *
import sys
from typing import Dict, List

import loader 
import util
import filter

term_size = os.get_terminal_size()
_dir = os.path.dirname(os.path.abspath(__file__))
single_letter_dict_path = os.path.join(_dir, "single_letter_terms.txt")
special_characters_dict_path = os.path.join(_dir, "special_characters.txt")
SINGLE_LETTER_TERMS: Dict[str, str] = loader.load_dictionary(single_letter_dict_path)
SPECIAL_CHARACTERS: List[str] = loader.load_list(special_characters_dict_path)

# print(SINGLE_LETTER_TERMS)
# print(SPECIAL_CHARACTERS)

source_data_path = os.path.join(_dir, "../data/multiturn_data/source_data")
new_data_path = os.path.join(_dir, "../data/multiturn_data/filtered_data")

flist_ = ['MDRW2100000001.json_2.json']

def get_dirnames(path):
    dirlist = []
    try:
        for dirname in os.listdir(path):
            if os.path.isdir(os.path.join(path, dirname)):
                dirlist.append(dirname)
    except:
        print(path, "does not exist")
        raise
    return dirlist

def get_filenames(path):
    flist = []
    try:
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                flist.append(filename)
    except:
        print(path, "does not exist")
        raise
    return flist

def main():
    dirlist = get_dirnames(source_data_path)
    for dirname in dirlist:
        flist = get_filenames(os.path.join(source_data_path, dirname))

        data_count = len(flist)
        filtered_data_count = 0
        progress = 0
        status = "IN PROGRESS"

        for filename in flist:
            remove_data = False
            df = loader.read_json(os.path.join(source_data_path, dirname, filename))
            for ind in range(len(df)):
                # df[ind]["utterance"] = repeat_normalize()
                # None
                for key in SINGLE_LETTER_TERMS:
                    # print(key)
                    # print(int(SINGLE_LETTER_TERMS[key]))
                    df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], key, int(SINGLE_LETTER_TERMS[key]))

                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅋ', 5)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅂ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅃ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㄴ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅜ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅠ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅡ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅗ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅣ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅇ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅎ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㄷ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅅ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㄱ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㄲ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅉ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅁ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅍ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], 'ㅌ', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], ':', 1)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], '\'', 1)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], '!', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], '?', 2)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], '"', 1)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], ',', 3)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], '.', 3)
                # df[ind]['utterance'] = filter.adjust_character_length(df[ind]['utterance'], ';', 1)

                df[ind]['utterance'] = only_text(df[ind]['utterance'])

                # df[ind]['utterance'] = filter.remove_special_characters(df[ind]['utterance'], SPECIAL_CHARACTERS)

                # if filter.is_long_utterance(df[ind]['utterance'], 150) or filter.is_short_utterance(df[ind]['utterance'], 5):
                #     remove_data = not remove_data
                #     break

            if not remove_data:
                if not os.path.exists(os.path.join(new_data_path, dirname)):
                    os.mkdir(os.path.join(new_data_path, dirname))
                    print(dirname, "generated in", os.path.join(new_data_path, dirname))
                    print('=' * term_size.columns)
                try:
                    loader.write_json(df, os.path.join(new_data_path, dirname, filename))
                    # print("--> ", filename, "generated in", os.path.join(new_data_path, dirname, filename))
                except:
                    print(dirname, "failed to generate.")
                    raise
                filtered_data_count += 1

            progress += 1
            print("\r[%-20s] %d%%" % ('='*int((progress/data_count)*20), int(100*(progress/data_count))), end = "")
            sys.stdout.flush()

        util.print_result(filename, data_count, filtered_data_count)

if __name__ == "__main__":
    main()
    None