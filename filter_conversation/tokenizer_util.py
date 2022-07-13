import pathlib
from transformers import AutoTokenizer

UNK = '[UNK]'

path = pathlib.Path('../tokenizer')
tokenizer = AutoTokenizer.from_pretrained(path)

def get_token(text):
    return tokenizer.tokenize(text)

def contains_unk(tokenized_text):
    if UNK in tokenized_text:
        return True
    return False

def is_repeat(tokens):
    if len(tokens) == 0:
        return False
    count = 0
    prev_token = tokens[0]
    for t in tokens[1:]:
        if t == prev_token:
            count += 1
        else:
            count = 0
        prev_token = t
        if count >= 4:
            return True
    return False

if __name__ == "__main__":
    None