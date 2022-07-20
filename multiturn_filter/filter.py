import data_util

SPECIAL_CHARACTERS = 'special_characters.txt'
MIN_UTTERANCE_LENGTH = 5
MAX_UTTERANCE_LENGTH = 150

file = open(SPECIAL_CHARACTERS, 'r', encoding='UTF-8')
illegal_characters = file.read().replace('\n', ' ').split(' ')
file.close()

def is_short_utterance(utterance):
    if len(str(utterance)) <= MIN_UTTERANCE_LENGTH:
        return True
    return False

def is_long_utterance(utterance):
    if len(str(utterance)) >= MAX_UTTERANCE_LENGTH:
        return True
    return False

def adjust_character_length(utterance, target, repeat_max):
    count = 0
    del_ind = []
    for ind, c in enumerate(utterance):
        if c == target:
            count += 1
            if count > repeat_max:
                del_ind.append(ind)
        elif c == ' ':
            continue
        else:
            count = 0
    for i in reversed(del_ind):
        utterance = utterance[0:i] + utterance[i+1:]
    return utterance

def remove_special_characters(utterance):
    for illegal_char in illegal_characters:
        utterance = utterance.replace(illegal_char, '')
    return utterance

if __name__ == "__main__":
    print(adjust_character_length('ㅋㅋㅋㅋㅋㅋㅋ 그래? ㅋㅋㅋㅋㅋㅋㅋㅋㅋ', 5))
    print(remove_special_characters('그래서 나는 그 드라마를 봤어 %▒!?'))