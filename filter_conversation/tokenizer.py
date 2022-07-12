import os
import pathlib
from transformers import AutoModel, AutoTokenizer

# cwd_path = os.getcwd()
path = pathlib.Path('../tokenizer')

# model = AutoModel.from_pretrained("klue/bert-base")
# tokenizer = AutoTokenizer.from_pretrained(cwd_path)
tokenizer = AutoTokenizer.from_pretrained(path)

def get_token(text):
    return tokenizer.tokenize(text)

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