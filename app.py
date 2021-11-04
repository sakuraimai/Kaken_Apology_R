from __future__ import print_function
import datetime
import csv

from flask import Flask, render_template, request, redirect

from src.audio_recorder.audio_recorder import AudioRecorder

app = Flask(__name__)
global_particilant_id = ""
next_link = ""
global_pure_next_link = ""


@app.route("/")
def title():
    experiment_date = datetime.datetime.now().strftime("%Y-%m-%d")
    experimenter = "小西先生"
    organization = "早稲田大学"
    experiment_name = "実験名"
    return render_template("title.html", 
                           experiment_date= experiment_date,
                           experimenter= experimenter,
                           organization= organization,
                           experiment_name= experiment_name)


@app.route("/introduction")
def introduction():
    return render_template("introduction.html")

@app.route("/setpersonalinformation", methods=["GET","POST"])
def setPersonalInformation():
    global global_particilant_id
    global global_audio_recorder
    result_csv_path = "./results/personal_info.csv"
    
    datetime_str = str(datetime.datetime.now())
    participant_id = datetime_str + "P"
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
    questionaire_csv_path = "./questionaires/Stimuli_Production_2021_01.csv"
    result_csv_path = "./results/apology_test.csv"
    l = []
    global next_link
    global global_pure_next_link
    global global_audio_recorder
    
    with open(questionaire_csv_path, "r", newline='') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
    
    if len(l) < id:
        return redirect("/finishallsession")
    
    questionaire = l[id]
    questionaire_id = questionaire[0]
    place = questionaire[1]
    target = questionaire[2]
    reason = questionaire[3]
    word1 = questionaire[4]
    word2 = questionaire[5]
    word3 = questionaire[6]
    word4 = questionaire[7]
    index = id + 1
    
    test_id = global_particilant_id + questionaire_id
        
    global_audio_recorder = AudioRecorder(test_id)
    
    if(request.method == "POST"):
        datetime_str = str(datetime.datetime.now())
        q1 = request.form["q1"]
        q2 = request.form["q2"]
        q3 = request.form["q3"]
        q4 = request.form["q4"]
        word = request.form["word"]

        with open(result_csv_path, "a", encoding="utf-8", newline="")as file:
            writer = csv.writer(file)
            writer.writerow([test_id, global_particilant_id, datetime_str, q1, q2, q3, q4, word])
        return redirect("/startrecord")
            
    global_pure_next_link = f"/experimentquestionaire/{index}"
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


@app.route("/finishallsession")
def finish_all_session():
    return render_template("finishAllSession.html")
    
    
if __name__ == "__main__":
    print('on hello')
    app.run(host="127.0.0.1", port=5000, debug=True)
