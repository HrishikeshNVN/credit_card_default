from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np


  

        
     
       
class Find_Model_Cluster:
    
    def __init__(self,file_obj, logger_obj):
        
        self.file_obj = file_obj
        self.logger_obj = logger_obj
        
        self.logger_obj.log(self.file_obj, "\n Entered in to Find Model Cluster class \n")
        
    def best_model(self, x_tr, x_ts, y_tr, y_ts):
        
        
        try:
            
            
            
            self.accuracy_list = []   
            self.model_list = []
            
            
             ##LOGISTIC REGRESSION HYPER PARAMETER TUNING
                                
            self.accuracy_list = []   
            self.model_list = []

            self.logger_obj.log(self.file_obj, "\n Started tuning Logistic regression \n")

            self.lr_params = {'C': np.logspace(-4 , 5 , 50), 'penalty': ['l1', 'l2']}

            self.cv_model = GridSearchCV(LogisticRegression(), self.lr_params, cv=3, n_jobs=-1, verbose=3, return_train_score=False)

            self.cv_model.fit(x_tr, y_tr)

            self.C = self.cv_model.best_params_['C']

            self.penalty = self.cv_model.best_params_['penalty']

            self.lr_model = LogisticRegression(penalty= self.penalty, C=self.C)

            self.lr_model.fit(x_tr, y_tr)


            self.lr_pred = self.lr_model.predict(x_ts)

            self.lr_accuracy = accuracy_score(y_ts, self.lr_pred)  

            self.model_list.append([self.lr_model,"LogisticRegression"])                               
            self.accuracy_list.append(self.lr_accuracy)                              

            self.logger_obj.log(self.file_obj, "\n Logistic regression tuned Success fully with accuracy_score:{} \n".format(self.accuracy_list[0]))
            
            ##RANDOM FOREST HYPER PARAMETER TUNING
            

            self.logger_obj.log(self.file_obj, "\n Started tuning Random_Forest_Classifier \n")
            self.rf_params = {'criterion': ['gini','entropy'],'max_depth': [10,20,40,50],'max_features': ['auto', 'sqrt'],'n_estimators': [50,100,130]}


            self.rf_cv = GridSearchCV(RandomForestClassifier(), param_grid=self.rf_params, cv=3, n_jobs=-1, verbose=3, return_train_score=False )


            self.rf_cv.fit(x_tr, y_tr)                             

            

            self.criterion = self.rf_cv.best_params_['criterion']

            self.max_depth = self.rf_cv.best_params_['max_depth']

            self.max_features = self.rf_cv.best_params_['max_features']


            self.n_estimators = self.rf_cv.best_params_['n_estimators']

            self.rf_model = RandomForestClassifier(  n_estimators=self.n_estimators,criterion= self.criterion, max_depth=self.max_depth,
            max_features=self.max_features)

            self.rf_model.fit(x_tr, y_tr)

            self.rf_pred = self.rf_model.predict(x_ts)

            self.rf_accuracy = accuracy_score(y_ts, self.rf_pred)

            self.model_list.append([self.rf_model,"Random_ForestClassifier"])                               
            self.accuracy_list.append(self.rf_accuracy)                                
            self.logger_obj.log(self.file_obj, "\n RandomForestClassifier  tuned Successfully with accuracy_score:{} \n".format(self.accuracy_list[1]))
            
            
            
            
            ##GRADIENT BOOSTING HYPER PARAMETER TUNING
            
            self.logger_obj.log(self.file_obj,"\n Started tuning GradientBoostingClassifier \n")
            self.gb_params = {'max_depth': [10,20,40,50],'n_estimators': [50,100,130]}
            
            
            self.gb_cv = GridSearchCV(GradientBoostingClassifier(), param_grid=self.gb_params, cv=3, n_jobs=-1, verbose=3, return_train_score=False )
            
            

            self.gb_cv.fit(x_tr, y_tr)

            self.max_depth = self.gb_cv.best_params_['max_depth']

            self.n_estimators = self.gb_cv.best_params_['n_estimators']

            self.gb_model = GradientBoostingClassifier(n_estimators=self.n_estimators, max_depth=self.max_depth)
            
            self.gb_model.fit(x_tr, y_tr)
            
            
            
            self.gb_pred = self.gb_model.predict(x_ts)

            self.gb_accuracy = accuracy_score(y_ts, self.gb_pred)
            
            print("Going to append to lists")

            self.model_list.append([self.gb_model, "GradientBoostingClassifier"])                               
            self.accuracy_list.append(self.gb_accuracy) 

            self.logger_obj.log(self.file_obj, "\n GradientBoostingClassifier  tuned Successfully with accuracy_score:{} \n".format(self.accuracy_list[2])) 
        
               
        
            
            self.max_accuracy = max(self.accuracy_list)
            self.pos = self.accuracy_list.index(self.max_accuracy)
            

            return self.model_list[self.pos][0], self.model_list[self.pos][1]
            
            
    
        except Exception as e:
            
            self.logger_obj.log(self.file_obj, "\n Exception occured while finding the best model"+str(e))
            
            raise Exception()
            
            
            