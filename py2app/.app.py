from __future__ import print_function
import datetime
import csv
import random
import sys
from flask import Flask, render_template, request, redirect

sys.path.append('./src')
from src.audio_recorder.audio_recorder import AudioRecorder

audio_input_channel = 0

app = Flask(__name__)
global_particilant_id = ""
next_link = ""
global_pure_next_link = ""
global_pure_past_link = ""
### 追加 ###
example_question_path = "./questionaires/example_question.csv"
questionaire_csv_path = "./questionaires/Stimuli_Production.csv"
wav_path = "./results/wav"
result_csv_path = "./results/apology_test.csv"
global_audio_recorder = None

l = []

with open(questionaire_csv_path, "r", newline='') as f:
    header = next(csv.reader(f))
    reader = csv.reader(f)
    l = [row for row in reader]
random.shuffle(l)

### 追加 ###
# 質問をcsvから追加するためのpath
with open(example_question_path, "r", newline='') as eq:
    header = next(csv.reader(eq))
    reader = csv.reader(eq)
    eq_list = [row for row in reader]


@app.route("/", methods=["GET","POST"])
def setPersonalInformation():
    global global_particilant_id
    global global_audio_recorder
    global audio_input_channel

    result_csv_path = "./results/personal_info.csv"

    datetime_now = datetime.datetime.now()
    datetime_str = str(datetime_now)
    participant_id = f"P{str(datetime_now.year).zfill(4)}{str(datetime_now.month).zfill(2)}{str(datetime_now.day).zfill(2)}_{str(datetime_now.hour).zfill(2)}_{str(datetime_now.minute).zfill(2)}"
    global_particilant_id = participant_id


    name = "unknown"
    email = "unknown"
    age = "0"
    gender = "unknown"

    if(request.method == "POST"):
        name = request.form["name"]
        email = request.form["email"]
        age = request.form["age"]
        gender = request.form["gender"]
        audio_input_channel = int(request.form["audio_input_channel"])

        with open(result_csv_path, "a", encoding="utf-8", newline="")as file:
            writer = csv.writer(file)
            writer.writerow([participant_id, datetime_str, name, email, age, gender])
        return redirect("/experimentquestionaireintroduction")

    return render_template("setPersonalInformation.html")

@app.route("/experimentquestionaireintroduction")
def experimentQuestionaireIntroduction():
    return render_template("experimentQuestionaireInduction.html")


@app.route("/experimentquestionaire/<int:id>", methods=["GET","POST"])
def experimentQuestionaire(id):

    global next_link
    global global_pure_next_link
    global global_pure_past_link
    global global_audio_recorder


    if len(l) < id+1:
        return redirect("/finishallsession")

    questionaire = l[id]
    questionaire_id = str(questionaire[0]).zfill(3)
    place = questionaire[1]
    target = questionaire[2]
    reason = questionaire[3]
    word1 = questionaire[4]
    word2 = questionaire[5]
    word3 = questionaire[6]
    word4 = questionaire[7]
    index = id + 1

    execute_datetime = datetime.datetime.now()
    test_id = f"{global_particilant_id}_Q{questionaire_id}_T{str(execute_datetime.hour).zfill(2)}_{str(execute_datetime.minute).zfill(2)}_{str(execute_datetime.second).zfill(2)}"

    global_audio_recorder = AudioRecorder(test_id, audio_input_channel)

    if(request.method == "POST"):
        datetime_str = str(datetime.datetime.now())
        q1 = request.form["q1"]
        q2 = request.form["q2"]
        q3 = request.form["q3"]
        q4 = request.form["q4"]
        word = questionaire[3+ int(request.form["word"])]


        with open(result_csv_path, "a", encoding="utf-8", newline="")as file:
            writer = csv.writer(file)
            writer.writerow([test_id, global_particilant_id, datetime_str, q1, q2, q3, q4, word])
        return redirect("/startrecord")

    global_pure_next_link = f"/experimentquestionaire/{index}"
    if index > 2:
        global_pure_past_link = f"/experimentquestionaire/{index - 2}"
    else:
        global_pure_past_link = f"/experimentquestionaire/{index - 1}"

    next_link = f"location.href='/experimentquestionaire/{index}'"

    return render_template("experimentQuestionaire.html",
                           next_link= next_link,
                           questionaire_id= questionaire_id,
                           place= place,
                           target= target,
                           reason= reason,
                           word1 = word1,
                           word2 = word2,
                           word3 = word3,
                           word4 = word4)

@app.route("/startrecord")
def get_start_record():
    global_audio_recorder.start()
    return redirect("/recordexecuting")

@app.route("/recordexecuting")
def record_executing():
    return render_template("recordingExecuting.html",
                           next_link= next_link)

@app.route("/rerecord")
def get_re_record():
    global_audio_recorder.reset()
    global_audio_recorder.start()
    return redirect("/recordexecuting")

@app.route("/finishrecord")
def get_finish_record():
    global_audio_recorder.finish()
    return redirect(global_pure_next_link)

@app.route("/reversepastquestipnaire")
def get_back_to_the_past_questionaire():
    return redirect(global_pure_past_link)

@app.route("/finishallsession")
def finish_all_session():
    return render_template("finishAllSession.html")


if __name__ == "__main__":
    print('on hello')
    app.run(host="127.0.0.1", port=5000, debug=False)
