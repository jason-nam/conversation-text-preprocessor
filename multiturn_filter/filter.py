from soynlp.normalizer import *

def is_short_utterance(utterance, min_utterance_len):
    if len(str(utterance)) <= min_utterance_len:
        return True
    return False

def is_long_utterance(utterance, max_utterance_len):
    if len(str(utterance)) >= max_utterance_len:
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
    
def remove_special_characters(utterance, illegal_characters):
    for illegal_char in illegal_characters:
        utterance = utterance.replace(illegal_char, '')
    return utterance

if __name__ == "__main__":
    print(adjust_character_length('ㅋㅋㅋㅋㅋㅋㅋ 그래? ㅋㅋㅋㅋㅋㅋㅋㅋㅋ',"ㅋ", 5))
    print(remove_special_characters('그래서 나는 그 드라마를 봤어 %▒!?', [""]))