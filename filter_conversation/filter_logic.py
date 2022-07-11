import tokenizer as tc
from csv_handler import is_null

A_MINIMUM_LENGTH = 5
ROW_INDEX = ['dialogue_id', 'Q-3', 'Q-2', 'Q-1', 'A']
STIFF_DIALOGUE_ID = '감성대화말뭉치'
POTENTIAL_STIFF_DIALOGUE_ID = 'HuLiC'
ILLEGAL_PHRASES = ('당신', '가요', '나요', '어요', '아요', '에요', '네요', '데요', '니다', '유감')
ILLEGAL_CHARACTERS = ('$', '@')
UTTERANCE_MIN_LENGTH = 10

# def is_short_answer(row):
#     return True if len(row['A']) < A_MINIMUM_LENGTH else False

def is_repeating_tokens(row):
    for utterance in row[2:5]:
        if is_null(utterance):
            continue
        if repeating_characters(utterance):
            return True
        if tc.is_repeat(tc.get_token(utterance)):
            return True
    return False

def is_system_dialogue(row):
    if STIFF_DIALOGUE_ID in row[ROW_INDEX[0]]:
        return True
    count = 0
    if POTENTIAL_STIFF_DIALOGUE_ID in row[ROW_INDEX[0]]:
        for utterance in row[2:]:
            if is_null(utterance):
                continue
            if any(c in utterance for c in ILLEGAL_PHRASES):
                count += 1
            if count >= 2:
                return True
    return False

def is_undefined(row):
    for utterance in row[2:]:
        if any(c in str(utterance) for c in ILLEGAL_CHARACTERS):
            return True
    return False

def is_short_utterance(row):
    for utterance in row[2:]:
        if len(str(utterance)) < UTTERANCE_MIN_LENGTH:
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
        if count >= 4:
            return True
    return False

def is_bad_conversation(row):
    # if is_short_answer(row):
    #     return True
    if is_repeating_tokens(row):
        return True
    if is_undefined(row):
        return True
    if is_system_dialogue(row):
        return True
    if is_short_utterance(row):
        return True
    return False

if __name__ == "__main__":
    None