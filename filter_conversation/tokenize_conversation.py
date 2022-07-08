from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("klue/bert-base")
tokenizer = AutoTokenizer.from_pretrained("klue/bert-base")

def get_token(text):
    return tokenizer.tokenize(text)

def is_repeat(tokens):
    
    return True

if __name__ == "__main__":
    None