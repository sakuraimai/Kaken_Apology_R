import os
import os, sys
sys.path.append(os.getcwd())

from questions.apology_questionaire import ApologyQuestionaire
from questions.personal_questionaire import PersonalQuestionaire

print('getcwd:      ', os.getcwd())
print('__file__:    ', __file__)

main_py_path = str(os.getcwd() ) + "/" + str(__file__)

personal_questionaire = PersonalQuestionaire(main_py_path, "personal_info_questionaire.csv", "personal_info.csv")
personal_questionaire.exec()

apology_questionaire = ApologyQuestionaire(personal_questionaire.participant_id, main_py_path, "Stimuli_Production_2021_01.csv", "apology_feeling_info_questionaire.csv", "apology_test.csv")
apology_questionaire.exec()