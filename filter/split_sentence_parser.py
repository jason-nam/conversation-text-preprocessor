# -*- coding: utf-8 -*-

from typing import List, Tuple
from kss import split_sentences
import os

import util
import loader

_dir = os.path.dirname(os.path.abspath(__file__))
source_data_path = os.path.join(_dir, "../data/long_multiturn_data/source_data")
new_data_path = os.path.join(_dir, "../data/long_multiturn_data/filtered_data")

MAX_LEN = 150

def split_sentence(sentences: List) -> Tuple:
    
    if len(sentences) <= 1:
        return (None, None)

    first_sentence = sentences.pop(0)
    second_sentence = sentences.pop(-1)
        
    if len(first_sentence) > MAX_LEN and len(second_sentence) > MAX_LEN:
        return (None, None)
    
    while sentences:
        first_sentence_ok = False
        second_sentence_ok = False

        if len(first_sentence + sentences[0]) <= MAX_LEN:
            first_sentence_ok = True
        if len(second_sentence + sentences[-1]) <= MAX_LEN:
            second_sentence_ok = True

        if not first_sentence_ok and not second_sentence_ok:
            break
        elif first_sentence_ok and not second_sentence_ok:
            first_sentence = first_sentence + " " + sentences.pop(0)
            continue
        elif not first_sentence_ok and second_sentence_ok:
            second_sentence = sentences.pop(-1) + " " + second_sentence
            continue
        else:
            if len(first_sentence) <= len(second_sentence):
                first_sentence = first_sentence + " " + sentences.pop(0)
            else:
                second_sentence = sentences.pop(-1) + " " + second_sentence

    if len(first_sentence) > MAX_LEN:
        return (None, second_sentence)
    elif len(second_sentence) > MAX_LEN:
        return (first_sentence, None)
    else:
        return (first_sentence, second_sentence)

def is_long_utterance(utterance, max_utterance_len):
    if len(str(utterance)) >= max_utterance_len:
        return True
    return False

def organize_sentence():
    # dirlist = loader.get_dirnames(source_data_path)
    # for dirname in dirlist:
    flist = loader.get_filenames(source_data_path)

    data_count = len(flist)
    filtered_data_count = 0 
    progress = 0
    status = "IN PROGRESS"

    for filename in flist:
        remove_data = False
        short_utterance_count = 0

        df = loader.read_json(os.path.join(source_data_path, filename))

        for ind in range(len(df)):
            if is_long_utterance(df[ind]['utterance'], MAX_LEN):
                sentence = split_sentences(df[ind]["utterance"])
                two_split_sentences = split_sentence(sentence)
                if two_split_sentences == (None, None):
                    df[ind][df[ind]["id"]] = "NA"
                elif two_split_sentences[0] == None:
                    df[ind][df[ind]["id"]+".0"] = "NA"
                    df[ind][df[ind]["id"]+".1"] = two_split_sentences[1]
                elif two_split_sentences[1] == None:
                    df[ind][df[ind]["id"]+".0"] = two_split_sentences[0]   
                    df[ind][df[ind]["id"]+".1"] = "NA"
                else:
                    df[ind][df[ind]["id"]+".0"] = two_split_sentences[0]
                    df[ind][df[ind]["id"]+".1"] = two_split_sentences[1]                

        if not os.path.exists(new_data_path):
            os.mkdir(new_data_path)
                        
        try:
            loader.write_json(df, os.path.join(new_data_path, filename))
            # print("--> ", filename, "generated in", os.path.join(new_data_path, dirname, filename))
        except:
            print("failed to generate.")
            raise
        filtered_data_count += 1

        progress += 1
        print("\r[%-20s] %d%%" % ('='*int((progress/data_count)*20), int(100*(progress/data_count))), end = "")
    print("")

if __name__ == "__main__":
    items = [
        # "ㅋㅋㅋㅋㅋ 아침엔 좀 많이 내렸어 말했낲 오늘 어두워서 평소보다 3분 정도 늦게 나와서 걸어가는데 집 앞 카페 사장님 그 분 ㅇㅇ 이 창문 내리고 또! 또 얻어타기 미안해가지고 눈 마주치자마자 달리는데 따라와러 창문 내리고 비오자나여 이래서 걍 타고 감 아침엔 좀 왔어 ",
        # "잘살면 좋은거고 우월감이라는게 우월감을 느끼고자 남을 비난하는건 아닌데 어쨌든 상대방이 잘못한 상황이고 내가 거기에 대해서 뭐라고 하는거니까 어쨌든 내가 스트레스받는거는 적지 근데 이제 니가 나한ㅌ0 어떤 포지션을 취해라 손을 떼라 이러면은 이제 내가 반성을 해야하잖아 근데 니도 어제 그랬잖어 니가 잘못한거 없다고 생각한다고 나도 사실 잘못한거 없다고 생각하거든 걍 내가 찾아봐주느라 힘든건 있어도 얘가 어긋나는거는 막아주고 좀 바르게 살 수 있도록 해줘야한다고 생각하는데 그니까 니는 내가 이런걸 찾느라 시간과 에너지를 소모하는게 사실 나는 부모도 아니니까 내가 나서서 그렇게 할 필요는 없다 맞는말이긴함 ",
        # " 선결제 , 실상품제공, 리뷰 후 평일 3일이내 페이백  실상품 제공 후기 여성잠옷 or 남성잠옷 or 아동잠옷 여성속옷 중복 절대 불가 한가지만 가능 하며 4개월이내 참여자 불가  신청시 진행하려는 번호 꼭 답변 함께주세요 카카오톡 아이디:account 연락주세요 name1아 이거 톡 보내봐 폰번호랑 저거중에 머하고 싶은지 보내면돼 ",
        "돈이 부족해도? 잘산다고? 개네들 다 부모집안에서 도움 받은거 아냐? 아님 말고 근데 내가느끼기엔 결혼할려면 기본 다 부모집 도움을 받더라고 어쩔 수 없는거 같애 부모 도움없이는 당장에 집 사는것도 어려우니까 나 어제 남친이랑 이 근처에 아파트 생기는 거 보러갔거든 진짜 짱 좋은거야 근데 기본 45억 하더라고 이 지역에서 45억 그냥 연애만 해야될까봐 "
    ]

    for txt in items:
        txt_split = split_sentences(txt)
        # print(txt)
        print(txt_split)
        print(split_sentence(txt_split))
        print()
    # organize_sentence()