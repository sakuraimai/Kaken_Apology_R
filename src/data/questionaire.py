from dataclasses import dataclass

@dataclass
class BaseQuestionaire:
    question_name: str
    question_word: str
    question_type: str

@dataclass
class QuestionShortText(BaseQuestionaire):
    pass

@dataclass
class QuestionQualitative(BaseQuestionaire):
    choices: object
    
@dataclass
class QuestionInt(BaseQuestionaire):
    pass

@dataclass
class QuestionDouble(BaseQuestionaire):
    pass

@dataclass
class QuestionSentence(BaseQuestionaire):
    pass

@dataclass
class QuestionDescrete(BaseQuestionaire):
    discrete: object
    
@dataclass
class QuestionContinuous(BaseQuestionaire):
    min: float
    max: float
    min_label: str
    max_label: str    