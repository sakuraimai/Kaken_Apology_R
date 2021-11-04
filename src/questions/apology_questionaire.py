import csv
from datetime import datetime
import time

from data.situation import Situation
from data.questionaire import(
    QuestionContinuous,
    QuestionSentence,
    QuestionQualitative,
    QuestionDescrete,
    QuestionDouble,
    QuestionInt,
    QuestionShortText    
)

from util.question import Question
from util.log import Log

from audio_recorder.audio_recorder import AudioRecorder



class ApologyQuestionaire:
    
    def __init__(self, participant_id, main_py_path, situation_csv_path, questionaire_csv_path, result_csv_path):
        self.situation_csv_path ="/Users/okpn/WasedaKonishiShudoProject/questionaires/Stimuli_Production_2021_01.csv"
        self.participant_id = participant_id
        self.questionaire_csv_path = "/Users/okpn/WasedaKonishiShudoProject/questionaires/apology_feeling_info_questionaire.csv"
        self.result_csv_path = "/Users/okpn/WasedaKonishiShudoProject/results/apology_test.csv"
    
    def exec(self):
        situation_list = self._prepare_situation()
        questionaire_list = self._prepare_questionaire()

        for situation in situation_list:
            
            Log.log("--------------new senario--------------")
            Log.log(f"シチュエーション番号: {situation.index}")
            Log.log(f"場所: {situation.place}")
            Log.log(f"謝罪の対象: {situation.target}")
            Log.log(f"理由: {situation.reason}")
            
            result = []
            test_id = self._make_test_id(situation_index= situation.index)
            datetime = self._get_time()
            
            result.append(test_id)
            result.append(self.participant_id)
            result.append(datetime)
            for questionaire in questionaire_list:
                value = self._perse_questionaire(questionaire)
                result.append(value)
            
            self.wait(3000)
            Log.log("これから，録音を開始します。カウントがされたら，実際に謝罪をしてください。")
            audio_recorder = AudioRecorder(test_id)
            self.wait(3000)
            Log.log("それでははじめます。")
            self.wait(3000)
            Log.log(3)
            self.wait(2000)
            Log.log(2)
            audio_recorder.start()
            self.wait(2000)
            Log.log(1)
            self.wait(2000)
            Log.log("謝罪してください。録音中です。")
            self.wait(5000)
            get_enter = input("エンターキーを押してください。次へいきます。")
            audio_recorder.finish()
            
            print(result)

            self.save_result_to_csv(result)
            
    def _prepare_situation(self):
        with open(self.situation_csv_path, "r", encoding="utf-8") as situation_csv:
            header = next(csv.reader(situation_csv))
            reader = csv.reader(situation_csv)
            situation_list = self._load_situation(reader)
        return situation_list
    
    def _prepare_questionaire(self):
        with open(self.questionaire_csv_path, "r", encoding="utf-8") as questionaire_csv:
            reader = csv.reader(questionaire_csv)
            questionaire_list = self._load_questionaire(reader)
        return questionaire_list
    
    def _load_situation(self, reader):
        situation_list = []
        for situation_row in reader:
            situation =  Situation(index= situation_row[0],
                            place= situation_row[1],
                            target= situation_row[2],
                            reason= situation_row[3]
                            )
            situation_list.append(situation)
        return situation_list
    
    def _load_questionaire(self, reader):
        questionaire_list = []
        for questionaire_row in reader:
            questionaire = None
            if(questionaire_row[2] == "short_text"):
                questionaire = QuestionShortText(question_name= questionaire_row[0],
                                        question_word= questionaire_row[1],
                                        question_type= questionaire_row[2])
            if(questionaire_row[2] == "qualitative"):
                qualitative_list = []
                for qualitative in questionaire_row[3:]:
                    qualitative_list.append(qualitative)
                questionaire = QuestionQualitative(question_name= questionaire_row[0],
                                            question_word= questionaire_row[1],
                                            question_type= questionaire_row[2],
                                            choices= qualitative_list)
                
            if(questionaire_row[2] == "int"):
                questionaire = QuestionInt(question_name= questionaire_row[0],
                                    question_word= questionaire_row[1],
                                    question_type= questionaire_row[2])
                
            if(questionaire_row[2] == "double"):
                questionaire = QuestionDouble(question_name= questionaire_row[0],
                                    question_word= questionaire_row[1],
                                    question_type= questionaire_row[2])
                
            if(questionaire_row[2] == "sentence"):
                questionaire =  QuestionSentence(question_name= questionaire_row[0],
                                    question_word= questionaire_row[1],
                                    question_type= questionaire_row[2])
                
            if(questionaire_row[2] == "continuous"):
                questionaire =  QuestionContinuous(question_name= questionaire_row[0],
                                    question_word= questionaire_row[1],
                                    question_type= questionaire_row[2],
                                    min= questionaire_row[3],
                                    max= questionaire_row[4],
                                    min_label= questionaire_row[5],
                                    max_label= questionaire_row[6])
                
            questionaire_list.append(questionaire)
            
        return questionaire_list
    
    def _perse_questionaire(self, questionaire):
            questionaire_type = questionaire.question_type
            if(questionaire_type == "short_text"):
                return Question.question_short_text(questionaire.question_word)
            if(questionaire_type == "qualitative"):
                return Question.question_qualitative(questionaire.question_word, questionaire.choices)
            if(questionaire_type == "int"):
                return Question.question_int(questionaire.question_word)
            if(questionaire_type == "double"):
                return Question.question_double(questionaire.question_word)
            if(questionaire_type == "sentence"):
                return Question.question_sentence(questionaire.question_word)
            if(questionaire_type == "continuous"):
                return Question.question_continuous(questionaire.question_word, questionaire.min, questionaire.max, questionaire.min_label, questionaire.max_label)
    
    def _make_test_id(self, situation_index):
        return str(self.participant_id) + "_" + str(situation_index)
        
    def _get_time(self):
        return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    def save_result_to_csv(self,result):
        with open(self.result_csv_path, "a", encoding="utf-8")as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(result)
            
    def wait(self, milisec):
        time.sleep(milisec/1000)