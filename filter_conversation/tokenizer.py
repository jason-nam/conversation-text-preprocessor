from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("klue/bert-base")
tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")

def get_token(text):
    return tokenizer.tokenize(text)

def is_repeat(tokens):
    count = 0
    if len(tokens) == 0:
        return False

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