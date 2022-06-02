from asyncore import file_dispatcher
import csv
import random
import re
import pathlib
import os
import sys
import copy
import json
import pickle

from regex import P

file_info_path = "./results/apology_test.csv"
wav_dir_path = "results/wav/"
condition_csv_path = 'preprocessor/condition.csv'
output_overview = 'experiment_folder/overview.csv'
output_files_dir = 'experiment_folder/wavfile/'

if not os.path.exists(output_files_dir):
    os.makedirs(output_files_dir)
    
# app.pyからコピー
# 音声ファイルのIDを格納したdictを作る
with open(file_info_path) as f:
    header = next(csv.reader(f))
    reader = csv.reader(f)
    input_list = [row for row in reader]
subject_id_dict = dict()
apology_word_dict = dict()
for line in input_list:
    if line[1] not in subject_id_dict:
        subject_id_dict[line[1]] = list()
    if line[7] not in apology_word_dict:
        apology_word_dict[line[7]]= list()
    subject_id_dict[line[1]].append(line[0])
    apology_word_dict[line[7]].append(line[0])
subject_word_dict = dict()
# 2次元dict
for line in input_list:
    if line[1] not in subject_word_dict:
        subject_word_dict[line[1]] = dict()
    if len(line) > 7:
        if line[7] not in subject_word_dict[line[1]]:
            subject_word_dict[line[1]][line[7]] = list()
        subject_word_dict[line[1]][line[7]].append(line[0])


def main():
    # ファイル名のファイル置いておくフォルダなかったら作る
    if not os.path.exists(output_files_dir):
        os.mkdir(output_files_dir)
    participant_ids = []
    with open(file_info_path, mode='r') as f:
        header = next(csv.reader(f))
        reader = csv.reader(f)
        participant_ids = [row[1] for row in reader]
    # participant_ids_set = set(participant_ids)
    # 'list'という変数名をプログラム中で使うと、list()した時にunboundエラーが出る
    participant_ids = list(set(participant_ids))

    with open(condition_csv_path, mode='r') as f:
        condition_header = next(csv.reader(f))
        reader = csv.reader(f)
        condition_list = [row for row in reader]
        pattern = condition_list[0][0]
       
    # 正規表現で指定したパターンから当てはまるidを取り出していく
    specified_id_list = list()
    for id in participant_ids:
        matchOB = re.search(pattern, id)
        if matchOB != None:
            # print(matchOB.group())
            specified_id_list.append(matchOB.group())
    
    specified_word_list = list()
    acquisitions = 10
    id_mix = False
    word_mix = False
    chunk = None
    # 取り出す単語をheaderからリストに入れる
    # csvに書き込んだ設定情報からflagを立てる
    for i, value in enumerate(condition_list[0]):
        if i > 0 and i < 9 and value == '1':
            specified_word_list.append(condition_header[i])
        elif i == 9:
            acquisitions = int(value)
        elif i == 10 and value == '1':
            id_mix = True
        elif i == 11 and value == '1':
            word_mix = True
        elif i == 12 and value == '1':
            chunk = 'id'
        elif i == 12 and value == '2':
            chunk = 'word'


    list_for_experiment = list()
    dict_for_experiment_id = dict()
    dict_for_experiment_word = dict()

    # 追加
    dict_for_experiment_id_word = dict()
    dict_for_experiment_word_id = dict()

    if specified_id_list != []:
        for id in specified_id_list:
            if id not in dict_for_experiment_id:
                dict_for_experiment_id[id] = list()
                dict_for_experiment_id_word[id] = dict()
            if specified_word_list != []:
                for word in specified_word_list:
                    if word not in dict_for_experiment_word:
                        dict_for_experiment_word[word] = list()
                        dict_for_experiment_word_id[word] = dict()
                    if id not in dict_for_experiment_word_id[word]:
                        dict_for_experiment_word_id[word][id] = list()
                    if word not in dict_for_experiment_id_word[id]:
                        dict_for_experiment_id_word[id][word] = list()

                    if word in subject_word_dict[id]:
                        if acquisitions > len(subject_word_dict[id][word]):
                            # taken: 実際にlistに格納する（できる）数
                            # acquisitionを直接編集すると後々まで響く
                            taken = len(subject_word_dict[id][word])
                        else:
                            taken = acquisitions
                        # 指定した数(<=あった数)を、最初に作った辞書からランダムに抽出してくる
                        # 辞書はフォルダ作りの制限の掛け方により使い分ける
                        sampled = random.sample(subject_word_dict[id][word], taken)
                        list_for_experiment.extend(sampled)
                        dict_for_experiment_id[id].extend(sampled)
                        dict_for_experiment_word[word].extend(sampled)
                        dict_for_experiment_id_word[id][word] = sampled
                        dict_for_experiment_word_id[word][id] = sampled
            else:
                if acquisitions > len(subject_id_dict[id]):
                    taken = len(subject_id_dict[id])
                else:
                    taken = acquisitions
                list_for_experiment.extend(random.sample(subject_id_dict[id], taken))
                
    elif specified_word_list != []:
        for word in specified_word_list:
            if acquisitions > len(apology_word_dict[word]):
                taken = len(apology_word_dict[word])
            else:
                taken = acquisitions
            list_for_experiment.extend(random.sample(apology_word_dict[word], taken))
    
   

    # 作ったdict_for_experimentを展開してlistにする手法
    # temp_output_list = []
    # if not id_mix and not word_mix and chunk == 'id':
    #     for key in dict_for_experiment_id:
    #         temp_output_list.extend(dict_for_experiment_id[key])
    # elif not id_mix and word_mix and chunk == 'id':
    #     for key in dict_for_experiment_id:
    #         # dict_for_experiment_id[key] = random.shuffle(dict_for_experiment_id[key])
    #         # temp_output_list.extend(dict_for_experiment_id[key])
    #         # random.shuffle(dict_for_experiment_id[key])
    #         # print(dict_for_experiment_id[key])
    #         random.shuffle(dict_for_experiment_id[key])
    #         # print(dict_for_experiment_id[key])
    #         # print(type(temp))
    #         temp_output_list.extend(dict_for_experiment_id[key])
    # elif not id_mix and not word_mix and chunk == 'word':
    #     for key in dict_for_experiment_word:
    #         temp_output_list.extend()
    # elif id_mix and not word_mix and chunk == 'word':
    #     for key in dict_for_experiment_word:
    #         temp_output_list.extend(random.shuffle(dict_for_experiment_word[key]))
    # elif id_mix and word_mix:
    #     random.shuffle(list_for_experiment)
    #     temp_output_list = list_for_experiment      
    # else:
    #     sys.exit("条件設定が間違っています。条件を確認してやり直してください。")

    # 作ったdict_for_experimentをdict形式を保持したままapp.pyに渡す
    # temp_output_dict = dict()
    # temp_output_dict→temp_output
    if not id_mix and not word_mix and chunk == 'id':
        # この方式は全部id→謝罪語で順番通り：使われないかもしれない
        temp_output = copy.copy(dict_for_experiment_id_word)
    elif not id_mix and word_mix and chunk == 'id':
        for key in dict_for_experiment_id:
            random.shuffle(dict_for_experiment_id[key])
        temp_output = copy.copy(dict_for_experiment_id)
    elif not id_mix and not word_mix and chunk == 'word':
        # この方式は全部謝罪語→idで順番通り：使われないかもしれない
        temp_output = copy.copy(dict_for_experiment_word_id)
    elif id_mix and not word_mix and chunk == 'word':
        for key in dict_for_experiment_word:
            random.shuffle(dict_for_experiment_word[key])
        temp_output = copy.copy(dict_for_experiment_word)
    elif id_mix and word_mix:
        # この方式は完全ランダム→使われないかも
        random.shuffle(list_for_experiment)
        temp_output = list_for_experiment
    else:
        sys.exit("条件設定が間違っています。条件を確認してやり直してください。")

    # outputフォルダの中身のファイル名を見て、インクリメントのようにファイル名を付けられるようにする
    p_output = pathlib.Path('experiment_folder/wavfile')
    # outputフォルダの中のファイル名を取得
    inside_output_list = list(p_output.iterdir())
    if inside_output_list != []:
        # basenameだけ取得してintに直し、sort
        # sortした中で一番大きい数+1を作成するファイルの名前とする
        inside_output_list_int = [int(str(name.stem)) for name in inside_output_list]
        inside_output_list_int.sort()
        current_file_name = inside_output_list_int[-1] + 1
    else:
        current_file_name = 1

    # 格納ファイル数の確認
    files_num = 0
    if type(temp_output) == dict:
        dict_for_experiment = copy.copy(temp_output)
        for i in dict_for_experiment:
            if type(dict_for_experiment[i]) == dict:
                for j in dict_for_experiment[i]:
                    files_num += len(dict_for_experiment[i][j])
            elif type(dict_for_experiment[i]) == list:
                files_num += len(dict_for_experiment[i])
    elif type(temp_output) == list:
        list_for_experiment = copy.copy(temp_output)
        files_num = len(list_for_experiment) 
    files_num = str(files_num)
    print("格納ファイル数：" + files_num)
    
    with open(str(p_output) + '/' + str(current_file_name) + '.json', 'a') as OUTPUT:
        json.dump(temp_output, OUTPUT, indent=2, ensure_ascii=False)
    # with open(str(p_output) + '/' + str(current_file_name) + '.csv', 'a') as OUTPUT:
    #     writer = csv.writer(OUTPUT)
    #     writer.writerow(list_for_experiment)
    with open(output_overview, 'a') as OVERVIEW:
        writer = csv.writer(OVERVIEW)
        condition_list[0].insert(0, str(len(list_for_experiment)))
        condition_list[0].insert(0, current_file_name)
        if current_file_name == 1:
            condition_header.insert(0, '格納ファイル数')
            condition_header.insert(0, 'ファイル名')
            writer.writerow(condition_header)
        writer.writerow(condition_list[0])

if __name__ == "__main__":
    main()
