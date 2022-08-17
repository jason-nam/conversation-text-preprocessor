from pathlib import Path
import json
import re
#import filter2_final as f2f
#import filterJM as jm
from concurrent import futures
#from soynlp.normalizer import *
from kss import split_sentences
from multiprocessing import freeze_support
from tqdm import tqdm
from threading import Thread
from typing import Optional, str

def split_sent(sentence):
    """Split all sentences in utterance using kss library. Return list of String type sentences."""
    freeze_support()
    return split_sentences(sentence)


def split_sent_connective(utterance):
    """Split sentences in utterance if sentences are connected with common connective korean adverbs. Return list of String type split sentences."""
    connective_adverbs = ["그럼", "그리고", "그래서"]

    # Find index locations.
    cut_ind = []
    for c_adv in connective_adverbs:
        for utterance_ind in range(0, len(utterance) - len(c_adv) + 1):
            if (
                utterance[
                    utterance_ind
                    :utterance_ind + len(c_adv)
                ] == c_adv
            ):
                cut_ind.append(utterance_ind)
    cut_ind.sort()

    if len(cut_ind) == 0:
        return [utterance]
    elif len(cut_ind) == 1:
        return [utterance[:cut_ind[0]], utterance[cut_ind[0]:]]
    else:
        split_utterance = [utterance[:cut_ind[0]]]
        for ind in range(len(cut_ind) - 1):
            split_utterance.append(
                utterance[
                    cut_ind[ind]
                    :cut_ind[ind+1]
                ]
            )
        split_utterance.append(utterance[cut_ind[-1]:])

        return split_utterance[1:] if split_utterance[0] == "" else split_utterance


def split_sent_onomatopoeia(utterance):
    """Split sentences in utterance if sentences are connected with single letter Korean internet terminology in the form of onomatopoeia. Terminology that are considered include 'ㅋ' that mimics natural laughter and 'ㅎ' that mimics soft laughter. Return list of String type split sentences."""
    split_utterance = split_sent(utterance)
    split_sent = []

    for sent in split_utterance:
        onomatopoeia_beg = False
        cut_ind = 0
        for sent_ind in range(len(sent)):
            if (
                sent[sent_ind] == 'ㅋ' 
                or sent[sent_ind] == 'ㅎ'
            ):
                onomatopoeia_beg = True
            elif sent[sent_ind] == " ":
                continue
            else:
                if onomatopoeia_beg == True:
                    split_sent.append(sent[cut_ind:sent_ind])
                    cut_ind = sent_ind
                onomatopoeia_beg = False
        split_sent.append(sent[cut_ind:])
    return split_sent


def bisect_utterance_step_one(utterance):
    """Split utterance into two sentences. Return two String utterances and boolean value indicating success of split. If splitting utterance not applicable, return back input utterance and boolean value indicating failure of spit."""
    split_utterance = split_sent(utterance)

    if len(split_utterance) == 1:
        return False, utterance, None

    top_utterance: str = ""
    bot_utterance: str = ""
    top_filled = False
    bot_filled = False

    while top_filled == False or bot_filled == False:
        if (
            not top_filled 
            and len(top_utterance + split_utterance[0]) >= 150
        ):
            top_filled = True
        else:
            top_utterance += split_utterance[0]
            del split_utterance[0]

        if len(split_utterance) <= 0:
            break

        if (
            not bot_filled 
            and len(bot_utterance + split_utterance[-1]) >= 150
        ):
            bot_filled = True
        else:
            bot_utterance += split_utterance[-1]
            del split_utterance[-1]
            if len(split_utterance) <= 0:
                break

    return False, utterance, None if (top_utterance == "" or bot_utterance == "") else True, top_utterance, bot_utterance


def bisect_utterance_step_two(utterance):
    """Split utterance into two sentences. Return two String utterances and boolean value indicating success of split. If splitting utterance not applicable, return back input utterance and boolean value indicating failure of spit.
    
    Note: This function is only applicable when applying second step. Refer to bisect_utterance_step_one function when applying first step."""
    split_utterance = split_sent(utterance)

    first_split = []
    for sent in split_utterance:
        first_split += split_sent_connective(sent)

    sec_split = []
    for sent in first_split:
        sec_split += split_sent_onomatopoeia(sent)

    split_utterance = sec_split

    if len(split_utterance) == 1:
        return False, utterance, None

    top_utterance: str = ""
    bot_utterance: str = ""
    top_filled = False
    bot_filled = False

    while top_filled == False or bot_filled == False:
        if (
            not top_filled 
            and len(top_utterance + split_utterance[0]) >= 150
        ):
            top_filled = True
        else:
            top_utterance += split_utterance[0]
            del split_utterance[0]

        if len(split_utterance) <= 0:
            break

        if (
            not bot_filled 
            and len(bot_utterance + split_utterance[-1]) >= 150
        ):
            bot_filled = True
        else:
            bot_utterance += split_utterance[-1]
            del split_utterance[-1]
            if len(split_utterance) <= 0:
                break

    return False, utterance, None if (top_utterance == "" or bot_utterance == "") else True, top_utterance, bot_utterance


def bisect_file_step_one(conv) -> Optional[list]:
    """Split input json file conversation into two group bundles. Organize bundles and apply appropriate identifications. Return list with two group bundles. If split not applicable, then return None."""
    split_conv = []

    for utterance in conv:
        if len(utterance["utterance"]) >= 150:
            is_split, top, bot = bisect_utterance_step_one(utterance["utterance"])
            # result = bisect_utterance_step_one(utterance["utterance"])
            if is_split == False:
                # return -1
                return None
                
            top_conv = {}
            top_conv["id"] = utterance["id"] + ".1"
            top_conv["speaker_id"] = utterance["speaker_id"]
            top_conv["utterance"] = top
            split_conv.append(top_conv)

            bot_conv = {}
            bot_conv["id"] = utterance["id"] + ".2"
            bot_conv["utterance"] = bot
            split_conv.append(bot_conv)
    
        else:   
            split_conv.append(utterance)

    return split_conv


def bisect_file_step_two(conv):
    """Split input json file into two group bundles. Organize bundles and apply appropriate identifications. Return list with two group bundles. If split not applicable, then return None.
    
    Note: This bisection is only applicable when applying second step. Refer to bisect_file_step_one function when applying first step."""
    split_conv =[]

    for utterance in conv:
        if len(utterance["utterance"]) >= 150:
            is_split, top, bot = bisect_utterance_step_two(utterance["utterance"])
            if is_split == False:
                # return -1
                return None

            top_conv = {}
            top_conv["id"] = utterance["id"] + ".1"
            top_conv["speaker_id"] = utterance["speaker_id"]
            top_conv["utterance"] = top
            split_conv.append(top_conv)

            bot_conv = {}
            bot_conv["id"] = utterance["id"] + ".2"
            bot_conv["utterance"] = bot
            split_conv.append(bot_conv)
    
        else:   
            split_conv.append(utterance)

    return split_conv


def bisect_file_step_three(json_file):
    """Split input json file into two group bundles. Organize bundles and apply appropriate identifications. Return list with two group bundles. If split not applicable, then return None.
    
    Note: This bisection is only applicable when applying third step. Refer to bisect_file_step_one function when applying first step or bisect_file_step_two function when applying second step."""
    list_cut_ind =[]
    copy_json_file =[]
    list_json_files =[]
    null_info={}
    for i,bundle in enumerate(json_file):
        if len( bundle["utterance"])>=150:
            null_info = {}
            copy_json_file.append(null_info)
            list_cut_ind.append(i)
        else:
            copy_json_file.append(bundle)
    while copy_json_file[0]==null_info:  
        copy_json_file = copy_json_file[1:]
    while copy_json_file[-1] == null_info:
        copy_json_file= copy_json_file[:-1]
    temp =[]
    copy_json_file = json_file
    while len(copy_json_file)>0:
        if len(copy_json_file)==1:
            if copy_json_file[0]==null_info:
                list_json_files.append(temp)
                break
            else:
                temp.append(copy_json_file[0])
                list_json_files.append(temp)
                break
        if copy_json_file[0]!={}:
            temp.append(copy_json_file[0])
            del copy_json_file[0]
            continue
        else:
            list_json_files.append(temp)
            temp = []
            del copy_json_file[0]
            continue
    return list_json_files





def CutJsonFile(json_file):
    list_json_file=[]
    splie_ind_list=[]
    continue_once=False
    for ind,bundle in enumerate(json_file):
        if continue_once:
            continue_once=False
            continue
        if bundle["id"].count(".")==3:
            # temp_list.append(bundle)
            splie_ind_list.append(ind+1)
            continue_once=True
    list_json_file.append(json_file[:splie_ind_list[0]])
    for i in range(len(splie_ind_list)-1):
        list_json_file.append(json_file[splie_ind_list[i]:splie_ind_list[i+1]])    
    list_json_file.append(json_file[splie_ind_list[-1]:])
    #print(splie_ind_list)
    return list_json_file


def MakeData(data_into_list,a):
    path_data="C:\\Users\\박준하\\Documents\\카카오톡 받은 파일\\filter_only_ALL6\\from_윤재님\\filtered_data\\long_exceptions\\"
    new_folder_name = path_data+"filtered_long_exceptions\\"
    for iii, each_json_file in enumerate(tqdm(data_into_list)):
        #print(order_data)
        if iii<-1107:
            continue
        with open(path_data+each_json_file.name,'r', encoding="UTF-8-sig") as json_file:
            json_to_python = json.load(json_file)

        filtered_json = bisect_file_step_one(json_to_python)
        if filtered_json!=None:
            list_json_in_piece = CutJsonFile(filtered_json)
            for ind,json_piece in enumerate(list_json_in_piece,1):
                if len(json_piece)>=2:
                    out_file3 = open(new_folder_name+each_json_file.name[:-5]+"_"+repr(ind)+".json", 'w', encoding = 'utf-8')
                    json.dump(json_piece, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
                    out_file3.close()
                else:
                    out_file3 = open(new_folder_name+"short_1st_filter\\"+each_json_file.name[:-5]+"_"+repr(ind)+".json", 'w', encoding = 'utf-8')
                    json.dump(json_piece, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
                    out_file3.close()
            return
        
        filtered_json_2nd=bisect_file_step_two(json_to_python)
        if filtered_json_2nd != None:
            list_json_in_piece_2 = CutJsonFile(filtered_json_2nd)
            for ii,json_piece_2 in enumerate(list_json_in_piece_2):
                if len(json_piece_2)>=2:
                    out_file3 = open(new_folder_name+each_json_file.name[:-5]+"_"+repr(ii+1)+".json", 'w', encoding = 'utf-8')
                    json.dump(json_piece_2, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
                    out_file3.close()
                else:
                    out_file3 = open(new_folder_name+"short_2nd_filter\\"+each_json_file.name[:-5]+"_"+repr(ii+1)+".json", 'w', encoding = 'utf-8')
                    json.dump(json_piece_2, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
                    out_file3.close()
            return

        json_in_piece=bisect_file_step_three(json_to_python)
        for i,json_piece_3 in enumerate(json_in_piece):
            out_file3 = open(new_folder_name+each_json_file.name[:-5]+"_"+repr(i+1)+".json", 'w', encoding = 'utf-8')
            json.dump(json_piece_3, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
            out_file3.close()
            
        
def main():
    data_into_list = []
    # path_data = "C:\\Users\\박준하\\Documents\\카카오톡 받은 파일\\filter_only_ALL6\\filter_only_ALL9\\"
    # path_data ="C:\\Users\\박준하\\Documents\\카카오톡 받은 파일\\chat_dialog_2006_mid\\chat_dialog_2006_mid\\"
    path_data="C:\\Users\\박준하\\Documents\\카카오톡 받은 파일\\filter_only_ALL6\\from_윤재님\\filtered_data\\long_exceptions\\"
    
    for json_file_name in Path(path_data).glob("*.json"):
        data_into_list.append(json_file_name)
        #print(json_file_name.name)
    print(len(data_into_list))

    new_folder_name = path_data+"fixed\\filtered_long_exceptions\\"
    Path(path_data+"fixed\\").mkdir(exist_ok=True)
    Path(new_folder_name).mkdir(exist_ok=True)
    Path(new_folder_name+"short_1st_filter\\").mkdir(exist_ok=True)
    Path(new_folder_name+"short_2nd_filter\\").mkdir(exist_ok=True)
    len1 = len(data_into_list)//2
    count =0
    for iii, each_json_file in enumerate(tqdm(data_into_list)):        
        #print(order_data)
        if iii<-1107:
            continue
        with open(path_data+each_json_file.name,'r', encoding="UTF-8-sig") as json_file:
            json_to_python = json.load(json_file)
        count+= len(json_to_python)
        
        filtered_json = bisect_file_step_one(json_to_python)
        if filtered_json!=None:
            list_json_in_piece = CutJsonFile(filtered_json)
            for ind,json_piece in enumerate(list_json_in_piece,1):
                if len(json_piece)>=2:
                    out_file3 = open(new_folder_name+each_json_file.name[:-5]+"_"+repr(ind)+".json", 'w', encoding = 'utf-8')
                    json.dump(json_piece, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
                    out_file3.close()
                else:
                    out_file3 = open(new_folder_name+"short_1st_filter\\"+each_json_file.name[:-5]+"_"+repr(ind)+".json", 'w', encoding = 'utf-8')
                    json.dump(json_piece, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
                    out_file3.close()
        else:
            filtered_json_2nd=bisect_file_step_two(json_to_python)
            if filtered_json_2nd != None:
                list_json_in_piece_2 = CutJsonFile(filtered_json_2nd)
                for ii,json_piece_2 in enumerate(list_json_in_piece_2):
                    if len(json_piece_2)>=2:
                        out_file3 = open(new_folder_name+each_json_file.name[:-5]+"_"+repr(ii+1)+".json", 'w', encoding = 'utf-8')
                        json.dump(json_piece_2, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
                        out_file3.close()
                    else:
                        out_file3 = open(new_folder_name+"short_2nd_filter\\"+each_json_file.name[:-5]+"_"+repr(ii+1)+".json", 'w', encoding = 'utf-8')
                        json.dump(json_piece_2, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
                        out_file3.close()
            else:
                ########################THIRD FILTER##########################
                json_in_piece=bisect_file_step_three(json_to_python)
                for i,json_piece_3 in enumerate(json_in_piece):
                    out_file3 = open(new_folder_name+each_json_file.name[:-5]+"_"+repr(i+1)+".json", 'w', encoding = 'utf-8')
                    json.dump(json_piece_3, out_file3, indent = 4, sort_keys=False, ensure_ascii=False)
                    out_file3.close()
    print(count)


if __name__ =="__main__":
    main()
