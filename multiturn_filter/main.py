import data_util
import util
import pathlib
import filter

PATH = [
            [
                '../data/multiturn_data/source_data/AIHUB-미디어젠-감성대화말뭉치_mid',
                pathlib.Path('AIHUB-미디어젠-감성대화말뭉치_mid')
            ],
            [
                '../data/multiturn_data/source_data/AlterEgo_dialog_mid',
                pathlib.Path('AlterEgo_dialog_mid')
            ],
            [
                '../data/multiturn_data/source_data/chat_dialog_2006_mid',
                pathlib.Path('chat_dialog_2006_mid')
            ],
            [
                '../data/multiturn_data/source_data/HuLiC_benchmark_mid',
                pathlib.Path('HuLiC_benchmark_mid')
            ],
            [
                '../data/multiturn_data/source_data/modu_online_corpus_2021_mid',
                pathlib.Path('modu_online_corpus_2021_mid')
            ]
]

CHAR = [(),]

flist_ = ['MDRW2100000001.json_2.json']

def get_filenames(path):
    flist = []
    for p in pathlib.Path(path).iterdir():
        if p.is_file():
            flist.append(p.name)
    return flist

def main():
    for path in PATH:
        flist = get_filenames(path[0])

        data_count = 0
        filtered_data_count = 0

        for file in flist:
            data_count += 1
            remove_data = False
            df = data_util.read_json(path[1]/file)
            for ind, utterance_data in enumerate(df):
                
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

                # df[ind]['utterance'] = filter.remove_special_characters(df[ind]['utterance'])

                if filter.is_long_utterance(df[ind]['utterance']) or filter.is_short_utterance(df[ind]['utterance']):
                    remove_data = not remove_data
                    # print('REMOVE', file)
                    break

            if not remove_data:
                data_util.write_json(df, path[1]/file)
                filtered_data_count += 1

        data_count += len(df)
        # util.print_progress(file)
        util.print_result(str(path[1]), data_count, filtered_data_count)

if __name__ == "__main__":
    main()