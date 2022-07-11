import tokenizer as tc
from data_util import is_null

ROW_INDEX = ['dialogue_id', 'Q-3', 'Q-2', 'Q-1', 'A']
STIFF_DIALOGUE_ID = '감성대화말뭉치'
POTENTIAL_STIFF_DIALOGUE_ID = 'HuLiC'
ILLEGAL_PHRASES = ('당신', '가요', '나요', '어요', '아요', '에요', '네요', '데요', '니다', '유감')
ILLEGAL_CHARACTERS = ('$', '@', 'ㅅㅋ', '⫬', 'ㅜㅡ', '가̆̈', 'ㅅㅂ')
UTTERANCE_MIN_LENGTH = 5
UTTERANCE_MAX_LENGTH = 250

def contains_repeating_tokens(row):
    for utterance in row[2:5]:
        if is_null(utterance):
            continue
        if repeating_characters(utterance):
            return True
        if tc.is_repeat(tc.get_token(utterance)):
            return True
    return False

def contains_system_dialogue(row):
    if STIFF_DIALOGUE_ID in row[ROW_INDEX[0]]:
        return True
    if POTENTIAL_STIFF_DIALOGUE_ID in row[ROW_INDEX[0]] and contains_illegal_phrases(row[2:]):
        return True
    return False

def contains_illegal_characters(row):
    for utterance in row[2:]:
        if any(c in str(utterance) for c in ILLEGAL_CHARACTERS):
            return True
    return False

def contains_short_utterance(row):
    for utterance in row[2:]:
        if len(str(utterance)) <= UTTERANCE_MIN_LENGTH:
            return True
    return False

def contains_long_utterance(row):
    for utterance in row[2:]:
        if len(str(utterance)) >= UTTERANCE_MAX_LENGTH:
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
        if count >= 3:
            return True
    return False

def contains_illegal_phrases(row):
    count = 0
    for utterance in row:
        if is_null(utterance):
            continue
        if any(c in utterance for c in ILLEGAL_PHRASES):
            count += 1
        if count >= 2:
            return True
    return False

def is_bad_conversation(row):
    if contains_repeating_tokens(row):
        return True
    if contains_illegal_characters(row):
        return True
    if contains_system_dialogue(row):
        return True
    if contains_short_utterance(row) or contains_long_utterance(row):
        return True
    return False

if __name__ == "__main__":
    None