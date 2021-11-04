import csv
from datetime import datetime
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

class PersonalQuestionaire:
    
    def __init__(self, main_py_path, questionaire_csv_path, result_csv_path):
        self.questionaire_csv_path = "/Users/okpn/WasedaKonishiShudoProject/questionaires/personal_info_questionaire.csv"
        self.result_csv_path = "/Users/okpn/WasedaKonishiShudoProject/results/personal_info.csv"
    
    def exec(self):
        questionaire_list = self._prepare_questionaire()
        Log.log("--------------new senario--------------")
        
        result = []
        datetime = self._get_time()
        self._make_participant_id(datetime)
        
        result.append(self.participant_id)
        result.append(datetime)
        
        for questionaire in questionaire_list:
            value = self._perse_questionaire(questionaire)
            result.append(value)
        
        print(self.participant_id)   
        print(result)
        
        self.save_result_to_csv(result)
    
    def _make_participant_id(self, datetime):
        self.participant_id = str(datetime) + "P"
        print(self.participant_id)
    
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
                return Question.question_coutinuous(questionaire.question_word, questionaire.min, questionaire.max, questionaire.min_label, questionaire.max_label)
    
    def _make_test_id(self, situation_index):
        return str(self.participant_id) + "_" + str(situation_index)
        
    def _get_time(self):
        return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    def save_result_to_csv(self,result):
        with open(self.result_csv_path, "a", encoding="utf-8")as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(result)