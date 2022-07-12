import tokenizer as tc
from data_util import is_null

ROW_INDEX = ['dialogue_id', 'Q-3', 'Q-2', 'Q-1', 'A']
STIFF_DIALOGUE_ID = '감성대화말뭉치'
POTENTIAL_STIFF_DIALOGUE_ID = 'HuLiC'
STIFF_PHRASES = ('당신', '가요', '나요', '어요', '아요', '에요', '네요', '데요', '니다', '유감')
MIN_UTTERANCE_LENGTH = 5
MAX_UTTERANCE_LENGTH = 250
MAX_REPEATING_CHARACTERS = 7
MAX_STIFF_WORD = 2


def contains_repeating_tokens(row):
    for utterance in row[2:5]:
        if is_null(utterance):
            continue
        if repeating_characters(utterance):
            return True
        print(tc.get_token(utterance))
    return False

def contains_stiff_dialogue(row):
    if STIFF_DIALOGUE_ID in row[ROW_INDEX[0]]:
        return True
    if POTENTIAL_STIFF_DIALOGUE_ID in row[ROW_INDEX[0]] and contains_stiff_phrases(row[2:]):
        return True
    return False

def contains_illegal_characters(row):
    illegal_character = get_special_characters()
    for utterance in row[2:]:
        if any(c in str(utterance) for c in illegal_character):
            return True
    return False

def contains_short_utterance(row):
    for utterance in row[2:]:
        if len(str(utterance)) <= MIN_UTTERANCE_LENGTH:
            return True
    return False

def contains_long_utterance(row):
    for utterance in row[2:]:
        if len(str(utterance)) >= MAX_UTTERANCE_LENGTH:
            return True
    return False

def repeating_characters(phrase):
    count = 0
    prev_char = phrase[0]
    for c in phrase[1:]:
        if c == prev_char:
            count += 1
        else:
            count = 0
        prev_char = c
        if count >= MAX_REPEATING_CHARACTERS:
            return True
    return False

def contains_stiff_phrases(row):
    count = 0
    for utterance in row:
        if is_null(utterance):
            continue
        if any(c in utterance for c in STIFF_PHRASES):
            count += 1
        if count >= MAX_STIFF_WORD:
            return True
    return False

def get_special_characters():
    file = open('special_characters.txt', 'r', encoding='UTF-8')
    data = file.read().replace('\n', ' ').split(' ')
    file.close()
    return data

def is_bad_conversation(row):
    if contains_repeating_tokens(row):
        return True
    if contains_illegal_characters(row):
        return True
    if contains_stiff_dialogue(row):
        return True
    if contains_short_utterance(row) or contains_long_utterance(row):
        return True
    return False

if __name__ == "__main__":
    None