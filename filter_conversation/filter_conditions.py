import tokenizer_util as tc
import itertools
from data_util import is_null

STIFF_DIALOGUE_ID = '감성대화말뭉치'
POTENTIAL_STIFF_DIALOGUE_ID = 'HuLiC'
SPECIAL_CHARACTERS = 'special_characters.txt'
STIFF_PHRASES = ('당신', '가요', '나요', '어요', '아요', '에요', '네요', '데요', '니다', '유감')
ROW_INDEX = ['dialogue_id', 'Q-3', 'Q-2', 'Q-1', 'A']
INTERNET_TERMS = ['ㅋ', 'ㅎ', 'ㅇ', 'ㄷ']
MIN_UTTERANCE_LENGTH = 5
MAX_UTTERANCE_LENGTH = 150
MAX_REPEATING_CHARACTERS = 10
MAX_STIFF_WORD = 2
INTERNET_TERMS_TO_LENGTH_RATIO = 0.5

file = open(SPECIAL_CHARACTERS, 'r', encoding='UTF-8')
illegal_characters = file.read().replace('\n', ' ').split(' ')
file.close()

def contains_repeating_tokens(row):
    count = 0
    # prev_utterance = []
    for utterance in row[2:]:
        if is_null(utterance):
            continue

        # if prev_utterance and tc.get_token(prev_utterance) and sublist(get_sublist(tc.get_token(prev_utterance)), tc.get_token(utterance)):
        #     print('!!! utterances repeat phrases !!!\n',
        #             tc.get_token(prev_utterance), '\n',
        #             tc.get_token(utterance), '\n')
        #     return True
        # prev_utterance = utterance
        # print(get_sublist(tc.get_token(prev_utterance)))

        if tc.contains_unk(tc.get_token(utterance)):
            return True
        if get_char_ratio(utterance) > INTERNET_TERMS_TO_LENGTH_RATIO:
            return True
        if repeating_characters(utterance, MAX_REPEATING_CHARACTERS):
            return True
        if repeating_characters(utterance, 5):
            if count == 2:
                return True
            count += 1
        else:
            count = 0
    return False



# def contains_sublist(lst, sublst):
#     n = len(sublst)
#     return any((sublst == lst[i:i+n]) for i in range(len(lst)-n+1))

# def get_sublist(mylist):
#     return [i for i in itertools.combinations(mylist,3) if contains_sublist(mylist, list(i))]

# def sublist(ls1, ls2):
#     def sublist1(lst1, lst2):
#         ls1 = [element for element in lst1 if element in lst2]
#         ls2 = [element for element in lst2 if element in lst1]
#         return ls1 == ls2


#     def sublist2(lst1, lst2):
#         def get_all_in(one, another):
#             for element in one:
#                 if element in another:
#                     yield element
#         for x1, x2 in zip(get_all_in(lst1, lst2), get_all_in(lst2, lst1)):
#             if x1 != x2:
#                 return True
#         return False


#     def sublist3(lst1, lst2):
#         from collections import Counter
#         c1 = Counter(lst1)
#         c2 = Counter(lst2)
#         for item, count in c1.items():
#             if count > c2[item]:
#                 return False
#         return True

#     for lst in ls1:
#         if sublist2(lst, ls2):
#             print(lst, '\n',
#                   ls2, '\n')
#             return True
#     return False



def get_char_ratio(utterance):
    internet_term_count = 0
    for c in utterance:
        if any(t == c for t in INTERNET_TERMS):
            internet_term_count += 1
    return internet_term_count / len(utterance)

def contains_stiff_dialogue(row):
    if STIFF_DIALOGUE_ID in row[ROW_INDEX[0]]:
        return True
    if POTENTIAL_STIFF_DIALOGUE_ID in row[ROW_INDEX[0]] and contains_stiff_phrases(row[2:]):
        return True
    return False

def contains_illegal_characters(row):
    # illegal_character = get_special_characters()
    for utterance in row[2:]:
        if any(c in str(utterance) for c in illegal_characters):
            return True
    return False

def contains_short_utterance(row):
    for utterance in row[2:]:
        if is_null(utterance):
            continue
        if len(str(utterance)) <= MIN_UTTERANCE_LENGTH:
            return True
    return False

def contains_long_utterance(row):
    for utterance in row[2:]:
        if len(str(utterance)) >= MAX_UTTERANCE_LENGTH:
            return True
    return False

def repeating_characters(phrase, repeat_max):
    count = 1
    prev_char = phrase[0]
    for c in phrase[1:]:
        if c == prev_char:
            count += 1
        else:
            count = 1
        prev_char = c
        if count >= repeat_max:
            return True
    return False

def contains_stiff_phrases(row):
    count = 1
    for utterance in row:
        if is_null(utterance):
            continue
        if any(c in utterance for c in STIFF_PHRASES):
            count += 1
        if count > MAX_STIFF_WORD:
            return True
    return False

# def get_special_characters():
#     file = open(SPECIAL_CHARACTERS, 'r', encoding='UTF-8')
#     data = file.read().replace('\n', ' ').split(' ')
#     file.close()
#     return data

def is_bad_conversation(row):
    if contains_short_utterance(row) or contains_long_utterance(row):
        return True
    if contains_illegal_characters(row):
        return True
    if contains_stiff_dialogue(row):
        return True
    if contains_repeating_tokens(row):
        return True
    return False

if __name__ == "__main__":
    None