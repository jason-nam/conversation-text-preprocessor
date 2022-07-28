import os
import json

def read_json(path):
    with open(path, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    return data

def write_json(data, path):
    out_file = open(path, "w", encoding = 'utf-8')
    json.dump(data, out_file, indent = 2, sort_keys = False, ensure_ascii=False)
    # print('Generated', filename)
    out_file.close()

def load_dictionary(path):
    result = {}
    with open(path, 'r', encoding="utf8") as file:
        for line in file.readlines():
            try:
                key = line.split()[0]
                value = line.split()[1]
                result[key] = str(value).strip()
            except Exception as e:
                pass
    return result

def load_list(path):
    result = []
    with open(path, 'r', encoding="utf8") as file:
        for line in file.readlines():
            try:
                for c in line.strip().split(" "):
                    result.append(c)
            except Exception as e:
                pass
    return result

if __name__ == "__main__":
    None