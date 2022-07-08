import filter_conversation.tokenize_conversation as tc
from csv_handler import is_null

A_MINIMUM_LENGTH = 5
ROW_INDEX = ['dialogue_id', 'Q-3', 'Q-2', 'Q-1', 'A']
DEFECTIVE_DIALOGUE_ID = '감성대화말뭉치'

def is_short_answer(row):
    return True if len(row['A']) < A_MINIMUM_LENGTH else False

def is_repeating_tokens(row):
    for col in row[2:5]:
        if is_null(col):
            continue
        if 'ㅋㅋㅋㅋ' in col or '....' in col:
            return True
        # if tc.is_repeat(tc.get_token(col)):
        #     return True
    return False

def is_system_voice(row):
    if DEFECTIVE_DIALOGUE_ID in row[ROW_INDEX[0]]:
        return True
    # if 'HuLiC' in row[ROW_INDEX[0]]:

    return False

def is_undefined(row):
    for i in row[2:]:
        if i != None and '$' in str(i):
            return True
    return False

def is_long_utterance(row):
    return True

def is_bad_conversation(row):
    if is_short_answer(row):
        return True
    if is_repeating_tokens(row):
        return True
    if is_undefined(row):
        return True
    if is_system_voice(row):
        return True
    return False

if __name__ == "__main__":
    None