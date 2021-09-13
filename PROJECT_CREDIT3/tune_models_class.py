import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV
   
    
class tune_models:
    
    def __init__(self, file_obj, logger_obj):
        
        self.file_obj = file_obj
        self.logger_obj = logger_obj
        
        self.logger_obj.log(self.file_obj , "\n Entered tune_models class")
    def parameter_tuning(self,x,y):    
        
        self.logger_obj.log(self.file_obj, "\n Started parameter tuning")
        
#      
#           "logistic_Regression" : {"model" : LogisticRegression(),
#                                   "params": {'C': np.logspace(-4 , 5 , 50), 'penalty': ['l1', 'l2']}},
#
#        """    "Random_Forest" : {"model" : RandomForestClassifier(),
#                             "params" : {'bootstrap': [True, False],
#                         'criterion': ['gini','entropy'],
#                         'max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
#                         'max_features': ['auto', 'sqrt'],
#                         'min_samples_leaf': [1, 2, 4],
#                         'min_samples_split': [2, 5, 10],
#                         'n_estimators': [50,100,150,200]}},
#            "svc" : { 
#                "model": SVC(gamma="auto"),
#                "params" : { 
#                    "C" : [1, 10, 20],
#                    "kernel" : ["rbf", "poly"]
#                }
#            },
#            "Adaboost Classifier" : {
#                "model" : AdaBoostClassifier(base_estimator= DecisionTreeClassifier()),
#                "params":  {
#                    "n_estimators":[100,120,150]
#                }
#            },
#            "xgboost" : {
#                "model": XGBClassifier(objective='binary:logistic'),
#                "params": {
#                    "n_estimators":[100,120,150]
#               }
#            },"""

        self.params = {    
            "Gradient boost" : {
                "model" : GradientBoostingClassifier(),
                "params":{
                    "n_estimators":[100,120,150]
                }
            }

            }


        try:
            
            self.scores = []
            for model_name, mp in self.params.items():
                mdl = RandomizedSearchCV(mp["model"],mp["params"], cv=5, return_train_score=False)
                mdl.fit(x, y)
                self.scores.append([mp["model"],[mdl.best_params_],mdl.best_score_])
            self.logger_obj.log(self.file_obj, " \n parameter tuning done successfully")

            return self.scores
        except Exception as e:
            self.logger_obj.log(self.file_obj, " \n Exception occured while parameter tuning"+str(e))
            