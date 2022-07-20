#filter 2 (대화정제)
import json
import re
def input(sentence):
    a= '[ㄱ-ㅎ기-힣a-zA-Zㅏ-ㅣ\s]+'
    regex = re.compile(a)
    final =''
    candidate = []
    if regex.search(sentence):
        result = regex.findall(sentence)
        for i in result:
            final+= i
            AA = i.replace(" ",'')
            if (AA != ''):
                c =sentence.index(i)+len(i)
                if c>=len(sentence):
                    break
                list111 = ['.','!','?']
                for i in list111:
                    if sentence[c] == i:
                        final += sentence[c]
                candidate.append(sentence[c])
    return final

print(input("나 안그래도 요즘 동숲 친구들 많이 만들었거든 다 포도 팔더라고 포도 매물 넘쳐요~~^^"))

print(input("없는줄 알앗자너~ 나 오늘 뭐하기 해산물 먹으러가기루햇어!!!!!!!! 타파스 바같은 넊낌이던데"))

