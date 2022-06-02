#-*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import csv
import random
import sys
# import wave
# from playsound import playsound
# import simpleaudio
import copy
import json
import numpy as np
import _tkinter
from tkinter import N
from flask import Flask, render_template, request, redirect
from flask import send_file, send_from_directory, abort

sys.path.append('./src')

audio_input_channel = 0

app = Flask(__name__)
global_particilant_id = ""
next_link = ""
global_pure_next_link = ""
global_pure_past_link = ""
### 追加 ###
questions_file_path = "./questionaires/example_question.csv"
questionaire_csv_path = "./questionaires/Stimuli_Production.csv"
wav_dir_path = "./results/wav/"
input_csv_path = "./results/apology_test.csv"
new_result_csv_path = "./results/apology_test_r.csv"
personal_info_path = "./results/personal_info.csv"
filenames_folders_dir = 'experiment_folder/wavfile/'
shuffled_folders_dir = 'experiment_folder/shuffled_wavfile/'

global_audio_recorder = None



### 追加 ###
# 質問をcsvから追加するためのpath
with open(questions_file_path, "r", newline='') as eq:
    header = next(csv.reader(eq))
    reader = csv.reader(eq)
    eq_list = [row[1] for row in reader]

l = []

# wavファイル名になる部分のみを抜き出す->l
with open(input_csv_path, "r", newline='') as f:
    header = next(csv.reader(f))
    reader = csv.reader(f)
    l = [row[0] for row in reader]
random.shuffle(l)

# 前実験のresultのファイルから切り分けてdict保存する
with open(input_csv_path) as f:
    header = next(csv.reader(f))
    reader = csv.reader(f)
    input_list = [row for row in reader]
subject_id_dict = dict()
apology_word_dict = dict()
for line in input_list:
    if line[1] not in subject_id_dict:
        subject_id_dict[line[1]] = list()
    # if len(line) > 7: # ここでエラー出る（不明）-> resultファイルの要素不足
    if line[7] not in apology_word_dict:
        apology_word_dict[line[7]]= list()
    subject_id_dict[line[1]].append(line[0])
    apology_word_dict[line[7]].append(line[0])
subject_word_dict = dict()
# 2次元dict
for line in input_list:
    if line[1] not in subject_word_dict:
        subject_word_dict[line[1]] = dict()
    if len(line) > 7: #同様
        if line[7] not in subject_word_dict[line[1]]:
            subject_word_dict[line[1]][line[7]] = list()
        subject_word_dict[line[1]][line[7]].append(line[0])

subject_condition = "None"
apology_word_condition = "None"
num_of_questions = 80

@app.route("/", methods=["GET","POST"])
def setExperimentalConditions():

    global subject_condition
    global apology_word_condition
    global l
    global subject_id_dict
    global apology_word_dict
    global subject_word_dict
    global num_of_questions
    global folder_name

    subject_condition = "None"
    apology_word_condition = "None"

    if request.method == "POST":
       
        # 全部listからやる時
        # folder_name = request.form["folder_name"] + '.csv'
        # print(folder_name)
        # with open(filenames_folders_dir + folder_name) as f:
        #     reader = csv.reader(f)
        #     file_list = [row for row in reader]
        #     l = copy.copy(file_list[0])

        folder_name = request.form["folder_name"] + '.json'
        print(folder_name)
        with open(filenames_folders_dir + folder_name) as f:
            temp = json.load(f)
            # 完全ランダムの時のみ
            if type(temp) == list:
                print("list")
                # file_list = [row for row in reader]
                l = copy.copy(temp)
                random.shuffle(l)
            elif type(temp) == dict:
                temp_list = list()
                print("dict")
                for i in temp:
                    if type(temp[i]) == dict:
                        for j in temp[i]:
                            random.shuffle(temp[i][j])
                            temp_list.extend(temp[i][j])
                    elif type(temp[i]) == list:
                        # for key in temp:
                        random.shuffle(temp[i])
                        temp_list.extend(temp[i])
                l = copy.copy(temp_list)

        # with open(result_csv_path, "a", encoding="utf-8", newline="")as file:
        #     writer = csv.writer(file)
        #     writer.writerow([subject_condition, apology_word_condition])
        
        return redirect("/setpersonalinformation")

    return render_template("setExperimentalConditions.html")

# 実験条件のid、謝罪語などを画面から設定するタイプ
# def setExperimentalConditions_sub():

#     global subject_condition
#     global apology_word_condition
#     global l
#     global subject_id_dict
#     global apology_word_dict
#     global subject_word_dict
#     global num_of_questions

#     subject_condition = "None"
#     apology_word_condition = "None"

#     if request.method == "POST":
#         if (request.form.get('subject') != None):
#             subject_condition = request.form["subject_id"]
#         if (request.form.get('word') != None):
#             apology_word_condition = request.form["selected_word"]
#         num_of_questions = int(request.form["num_of_questions"])
#         # with open(result_csv_path, "a", encoding="utf-8", newline="")as file:
#         #     writer = csv.writer(file)
#         #     writer.writerow([subject_condition, apology_word_condition])
        
#         if subject_condition == "None":
#             if apology_word_condition != "None":
#                 l = copy.copy(apology_word_dict[apology_word_condition])
#         elif apology_word_condition == "None":
#             l = copy.copy(subject_id_dict[subject_condition])
#         else:
#             l = copy.copy(subject_word_dict[subject_condition][apology_word_condition])
#         random.shuffle(l)
#         l = copy.copy(l[0:num_of_questions])
#         ### test ###
#         print("condition: " + subject_condition + "," + apology_word_condition + "," + str(num_of_questions))
#         print("l_len(setcondition): ")
#         print(len(l))
#         print(l)

#         return redirect("/setpersonalinformation")

#     return render_template("setExperimentalConditions.html")


@app.route("/setpersonalinformation", methods=["GET","POST"])
def setPersonalInformation():
    global global_particilant_id
    global global_audio_recorder
    global audio_input_channel

    # result_csv_path = "./results/personal_info.csv"
    # test
    print("l_len(setpersonalinformation): ")
    print(len(l))
    if len(l) < 10:
        print(l)

    datetime_now = datetime.datetime.now()
    datetime_str = str(datetime_now)
    participant_id = f"R{str(datetime_now.year).zfill(4)}{str(datetime_now.month).zfill(2)}{str(datetime_now.day).zfill(2)}_{str(datetime_now.hour).zfill(2)}_{str(datetime_now.minute).zfill(2)}"
    global_particilant_id = participant_id

    print("書き込み")
    with open(shuffled_folders_dir + global_particilant_id + '_F' + folder_name, 'w') as OUTPUT:
        json.dump(l, OUTPUT, indent=2, ensure_ascii=False)
       

    name = "unknown"
    email = "unknown"
    age = "0"
    gender = "unknown"

    if(request.method == "POST"):
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        gender = request.form["gender"]
        
        with open(personal_info_path, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([participant_id, subject_condition, apology_word_condition, num_of_questions, datetime_str, name, email, age, gender])
        return redirect("/experimentquestionaireintroduction")

    return render_template("setPersonalInformation.html")

@app.route("/experimentquestionaireintroduction")
def experimentQuestionaireIntroduction():
    global l
    print("l_len(introduction): ")
    print(len(l))
    return render_template("experimentQuestionaireInduction.html")


@app.route("/listeningexperiment/<int:id>", methods=["GET","POST"])
def listeningExperiment(id):

    global next_link
    global global_pure_next_link
    global global_pure_past_link
    global subject_condition
    global apology_word_condition
    global l
    if len(l) < id+1:
        return redirect("/finishallsession")

    question1 = eq_list[0]
    question2 = eq_list[1]
    question3 = eq_list[2]
    question4 = eq_list[3]
   
    wav_file_id = l[id]
    index = id + 1
    l_len = len(l)
    if id > 0:
        progress = str(100*id/l_len)
    else:
        progress = "0"
    
    print("wav_file_id")  
    print(wav_file_id)
    print("l_len(experiment): ")
    print(len(l))
    execute_datetime = datetime.datetime.now()
    
    test_id = f"{global_particilant_id}_W{wav_file_id}_T{str(execute_datetime.hour).zfill(2)}_{str(execute_datetime.minute).zfill(2)}_{str(execute_datetime.second).zfill(2)}"
    # test_id = f"{global_particilant_id}_{wav_file_id}_{str(execute_datetime.hour).zfill(2)}_{str(execute_datetime.minute).zfill(2)}_{str(execute_datetime.second).zfill(2)}"

    # global_audio_recorder = AudioRecorder(test_id, audio_input_channel)
    # wav_file_path = wav_dir_path + wav_file_id + ".wav"
    # playsound(wav_file_path)
    # wav_obj = simpleaudio.WaveObject.from_wave_file(wav_file_path)
    # play_obj = wav_obj.play()
    # play_obj.wait_done()

    if(request.method == "POST"):
        datetime_str = str(datetime.datetime.now())
        q1 = request.form["q1"]
        q2 = request.form["q2"]
        q3 = request.form["q3"]
        q4 = request.form["q4"]

        with open(new_result_csv_path, "a", encoding="utf-8", newline="")as file:
            writer = csv.writer(file)
            writer.writerow([test_id, global_particilant_id, wav_file_id, datetime_str, q1, q2, q3, q4])
        # return redirect("/startrecord")
        return redirect(global_pure_next_link)

    global_pure_next_link = f"/listeningexperiment/{index}"
    if index > 2:
        global_pure_past_link = f"/listeningexperiment/{index - 2}"
    else:
        global_pure_past_link = f"/listeningexperiment/{index - 1}"

    next_link = f"location.href='/listeningexperiment/{index}'"

    return render_template("listeningExperiment.html",
                           next_link= next_link,
                           question1= question1,
                           question2 = question2,
                           question3 = question3,
                           question4 = question4,
                           wav_file_id = wav_file_id,
                        #    wav_file_path = wav_file_path,
                           progress = progress
                           )

@app.route('/listeningexperiment/<wav_file_id>')
def returnAudioFile(wav_file_id):
    # path_to_audio_file = "/Audios/yourFolderPath" + audio_file_name
    wav_file_path = wav_dir_path + wav_file_id + ".wav"

    return send_file(
        wav_file_path, 
        mimetype="audio/wav", 
        as_attachment=True,
        download_name="test.wav")
        #  attachment_filename="test.wav")
       

@app.route("/reversepastquestipnaire")
def get_back_to_the_past_questionaire():
    return redirect(global_pure_past_link)

@app.route("/finishallsession")
def finish_all_session():
    return render_template("finishAllSession.html")


if __name__ == "__main__":
    print('on hello')
    app.run(host="127.0.0.1", port=5000, debug=True)
