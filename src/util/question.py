
from util.log import Log

class Question:
    
    def question_short_text(message): #半角スペース等なしの単語，名前みたいなもの
        Log.log(message)
        value = input("Input Values :")
        return value

    def question_qualitative(message, choices): #質的データ
        Log.log(message + ":" + str(choices))
        value = input("Input Values :") 
        return value
    
    def question_int(message): #整数の質問
        Log.log(message)
        value = input("Input Values :") 
        return value
    
    def question_double(message): #実数ならなんでもいい質問
        Log.log(message)
        value = input("Input Values :") 
        return value
    
    def question_sentence(message): #長文でもいい質問
        Log.log(message)
        value = input("Input Values :") 
        return value
    
    def question_discrete(message, discrete): #離散値量的データの質問
        Log.log(message + ":", str(discrete))
        value = input("Input Values :") 
        return value
    
    def question_continuous(message, min, max, min_label, max_label): #連続値量的データの質問
        Log.log(message + ":" + min + "=" + min_label + " - " + max +  "=" + max_label)
        value = input("Input Values :") 
        return value