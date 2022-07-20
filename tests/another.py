import json
from re import I
import tempfile
from xml.etree.ElementTree import TreeBuilder
from eunjeon import Mecab
from numpy import True_

#이 함수로 한번에 다 필터링 걸치수있게끔 함수 만들기
#def최대한 많이 써서 마지막에 한번에 간단하게 돌려버리자
#step1
#step2 ㅋ없애는 프로젝트
M = Mecab()


#문자가 하나인 경우만 5개 미만으로 제거한다.
def removeKHU(ip):
    final = ""
    limit = 0
    for a in range(len(ip)):
        if is_single_letter(ip[a]) == False:
            if ip[a] == " ":
                final += ip[a]
            else:
                limit = 0
                final += ip[a]
        else:
            limit+=1
            if limit <=5:
                final += ip[a]
    return final

def unknown_pos(sentence):
    m = Mecab()
    unknownlist = []
    a = m.pos(sentence)
    for i in a:
        if i[1] == 'UNKNOWN':
            unknownlist.append(i[0])
    return unknownlist

def is_single_letter(ip):    
    one_list = ['ㄱ','ㄲ','ㅆ','ㄸ','ㅃ','ㅉ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ','ㅏ','ㅑ','ㅓ','ㅕ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅣ','ㅘ']
    for a in one_list:
        if ip == a:
            return True
    return False
    
def cut_unknown(sentence):
    noKHU = sentence
    #print(noKHU)
    #print(M.pos(noKHU))
    unknown = unknown_pos(noKHU)
    sen = ''
    copy = noKHU
    for a in unknown:
        loc = copy.index(a)
        sen += copy[0:loc]
        copy = copy[loc+len(a):]
        locKHU = len(sen)-1
        
        limit =0
        while is_single_letter(sen[locKHU]) == True:
            if sen[locKHU] != ' ':
                limit +=1
                if(limit>5):
                    limit = 5
            locKHU -= 1
        if(limit >=2):
            sen = sen[:len(sen)-3] + a[:2]
        else:
            sen += a[:5-limit]
        
    return sen +copy



#aaa= "월요일이네요. 난 아직 술이 안깼어요"
#print(aaa[aaa.index("난"):len(aaa)])        

#print(M.pos("어어ㅓ어 어땟어 "))

#print("a"+"  v")
#관계확인해서 띄워쓰기 ///단어다띄워쓰기해서 숫자가 맞는지 확인
#국회에서만 쓰이는 말투이니까 사전을 만들어서 국회가 나왔으니 제일을 제 일로 바꾸어 줄 수 도있다.


#주임님한테 물어볼거 ㅋㅋ사이에 띄워쓰기가 있으면 몇개까지 허용해도 되는가? ex> ㅋ     ㅋㅋㅋㅋ 이런경우 띄워쓰기를 없애야 하나요?
'''
def null1():
    n=4
    str1 = 'MDRW2100000005'
    with open("workplease.json",'r', encoding="UTF-8") as json_file:
        chat = json.load(json_file)
    b=chat["utterance"]
    list1 = []
    for a in b:
        list1.append(cut_unknown(a))
    toJSON = []
    for a in range(len(b)):
        toJSON[a]["id"]=chat[a]["id"]
        toJSON[a]["speaker_id"]=chat[a]["speaker_id"]
        toJSON[a]["filtered_utterance"] = list1[a]
    out_file = open('changed'+str(n+1), 'w', encoding = 'utf-8')
    json.dump(toJSON, out_file, indent = 4, sort_keys=False, ensure_ascii=False)
    out_file.close()
'''
#index를 쭉가면서 좌우에 한글자만 있는경우 인덱스 모음으로 묶고 인덱스를 돌려가면서 limit제한에 맞게끔 맞춰준다.
def between_one_word(sentence):
    index =[]
    for i in range(1,len(sentence)-1):
        if is_single_letter(sentence[i])==False:
            if is_single_letter(sentence[i-1]) == True & is_single_letter(sentence[i+1])==True:
                index.append(i)
    cut=0
    sentence1 = sentence
    for c in index:
        a = c-cut
        locA=a-1
        locB=a+1
        countA=0
        countB=0
        temp= 0
        while is_single_letter(sentence1[locA])==True:
            if is_single_letter(sentence1[locA]) == True:
                countA+=1
            locA = locA -1
            if(locA==-1):
                temp = -1
                locA=a
        c=0
        while is_single_letter(sentence1[locB])==True:
            if is_single_letter(sentence1[locB]) == True:
                countB+=1
            locB +=1
            if locB >=len(sentence1):
                c=locB
                locB=a
        if(countA+countB>5):
            if countA>4: 
                cut = cut + countA-4
                countA=4
            if countB>1:
                cut = cut + countB-1 
                countB=1
        if temp== -1:
            locA=0
        if c>0:
            locB=c
        if locA!=0:
            sentence1 = sentence1[:locA+1]+sentence1[a-countA:a+countB+1]+sentence1[locB:]
        else:
            sentence1 = sentence1[a-countA:a+1+countB]+sentence1[locB:]
    return sentence1
#"ㅋㅋㅋㅋㅋㅋㅋㅋㅋ ㄴㄴ"같은경우
#먼저 종류별로 나누어 주고 그렇게 한거를 두개만 존재해야 되는거는 그대로 있게한다. 5개로 추리는 과정
#있으면 나머지의 limit 은 3개로 좁힌다.
#ㅋ만 있는걸 가져온다. 그리고 정리
def two_word(a):
    list = ['ㄱ','ㄴ','ㄷ','ㅂ','ㅇ','ㅏ','ㅓ','ㅗ','ㅜ','ㅠ','ㅡ','ㅣ']
    if len(a) >=2 | len(a)==0:
        return False
    for i in list:
        if a[0]== i:
            return True
    return False

def two_is_fine(sentence):
    list = ['ㄱ','ㄴ','ㄷ','ㅂ','ㅇ','ㅏ','ㅓ','ㅗ','ㅜ','ㅠ','ㅡ','ㅣ']
    copy = sentence
    result=''
    Began = False
    one_word_list = []
    temp = ''
    #한글자만 가지고 있는애들
    index = []
    for i in range(len(sentence)):
        if sentence[i]!=' ':
            if is_single_letter(sentence[i]) == True:
                temp += sentence[i]
                if Began == False:
                    index.append(i)
                    Began = True
            else:
                Began = False
    #print(index)
    for a in index:
        t =a
        temp =''
        while is_single_letter(sentence[t]) == True:
            temp += sentence[t]
            if sentence[t+1] == ' ':
                temp += " "
                t+=2
                if t>=len(sentence)-1:
                    break
            else: 
                t +=1
                if t>=len(sentence)-1:
                    break
        #print(temp)
        one_word_list.append(temp)
    if is_single_letter(sentence[len(sentence)-1]) ==True:
        one_word_list[len(one_word_list)-1] +=sentence[len(sentence)-1]
    
    new_list = []
    for i in one_word_list:
        a = i.replace(" ",'')
        new = ''
        for letter in list:
            two = letter+letter
            check = a.find(two)
            if(check!=-1):
                new+=two
        new_list.append(new)
    loc=0
    #print(one_word_list)
    #print(new_list)
    for i in (one_word_list):
        if new_list[loc] != '':
            copy = copy.replace(i,new_list[loc])
        loc +=1

    return copy
    #print(one_word_list)
    """for line in one_word_list:
        for letter in range(len(line)):
            if line[letter] == ' ':
                temp += ' '
            else:
                if two_word[i] != True:
                    temp += letter
                else: None
    """
    #여기서 부터 변환해주는 코드 (below blank 에서 짤것)   

def work(sentence):
    return between_one_word(cut_unknown(removeKHU(two_is_fine(sentence))))

#예제
#a="ㅋㅋㅋㅋㅋ큭ㅋㅋㅋㅋ이러면서 됏다그래 이러고 끄시더라구옹 ㅋㅋㅋㅋㅋㅇㄴㅋㅋㅋ참ㅌㅌㅌㅌㅋㅋㅌ"
#print(M.pos("ㅋㅋㅋㅋㅋ큭ㅋㅋㅋㅋ이러면서 됏다그래 이러고 끄시더라구옹 ㅋㅋㅋㅋㅋ참ㅌㅌㅌㅌㅌ"))
print(work("ㅋㅋㅋㅋㅋ큭ㅋㅋㅋㅋ이러면서 됏다그래 이러고 끄시더라구옹 ㅋㅋㅋㅋㅋㅇㄴㅋㅋㅋ참ㅌㅌㅌㅌㅋㅋㅌ"))
#print(M.pos(a))
#print(removeKHU(cut_unknown("ㅋㅋㅋㅋ킄ㅋ킄ㅋㅋㅋ")))
#print(M.pos(work("아아아 ㅎㅎㅎㅎㅎㅎㅎ")))
print(work("ㅋㅋㅋㅋㅋ응ㅜㅜ 어쩔수읍지 ㅋㅋㅋㅋㅋㅋㅋㅋ응ㅋㅋㅋㅋ어떻게 하겠어 ㅋㅋㅋㅋㅋㅋㅋㅋ쿠ㅜㅠㅡㅣ"))
#print(between_one_word("어쩔수없지 ㅋㅋㅋㅋ응ㅋ어떻게"))
#print(len("어쩔수읍지 ㅋㅋㅋㅋㅋㅋㅋㅋ쿠ㅜㅜㅜㅜㅜ"))
#print(work("헉 맞아 ㅋ큐ㅠㅠㅠ 사실 거리두기가 제일 큰 이유네 남쪽지방에 살아서 서울 가는것도 엄청 큰 여행이더라 ㅎㅎ 여전히 서울이 제일 재밌는 거 같아 혹시 추천 해줄 관광지 있어?"))
#print(work("ㅋㅋㅋㅋㅋㅋ ㄴㄴ"))
print(work("하지마ㅌㅌㅋㅋ ㅌㅌ ㅌ랄니까 ㅋㅋㅋㅋㅋㅋㅋ어이가 없네 ㅁㅁㅁ"))



