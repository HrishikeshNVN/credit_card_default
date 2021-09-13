from db_operations import Db_Opeartions as db_op
from data_pre_process import Data_Pre_Process as dpre
from application_logging import logger
import pickle
import os
import pandas as pd
import numpy as np



"""
                Class Name: Predict_Class
                Description: This is the entry point to prediction. This class receives data to predict,
                after prediction the predicted value will be return and also insert the data to the database
                Output: Predicted value
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
"""





class Predict_Class:

    
    
    
    def __init__(self):
        self.file_obj = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.logger_obj = logger.App_Logger()
    def predict(self,data):
        
        self.logger_obj.log(self.file_obj,'Prediction started \n')
        try:
            data_frame = data.copy()
            #Preprocessing new data
            dat_pre = dpre(self.file_obj,self.logger_obj)
            #Cleaning spaces if any
            df = dat_pre.space_cleaning(data)
            #Removing irrelevant Columns
            df = dat_pre.nouse_columns_remove(df)
            #Splits data to dependent and independent 
            dfx = dat_pre.split_dependent_independent(df)
            #Checks for null values and if any columns which has nul value returns
            cols, null_col_df = dat_pre.checks_for_null(dfx)
            #Seperates data to categorical and numerical
            print("CHECKING COLUMNS")
            print(dfx)
            df_cat, df_num = dat_pre.seperate_cat_num(dfx)
            #cols = df_num.columns
            df_cat[cols] = df_num[cols].values
            #Cleaning categorical data
            df_cat = dat_pre.clean_cat_data(dfx)
            #Creates one hot encoding object-dictionary for encoding nominal values
            oh_dict = dat_pre.create_one_hot1()
            #Performs One hot encoding on nominal values
            df_enc = dat_pre.oh_encode1(oh_dict,df_cat)
            #Performs frequency encoding on nominal variables which has more unique values in number
            
            df_fr_enc = dat_pre.freq_encode(df_enc)
            
            #Missing numerical values imputation
            df_cat_num = dat_pre.impute_missing_num_data(df_fr_enc)
            
            #Scaling the data
            df_xcn = dat_pre.scales_data(df_cat_num)
            #Identifies the cluster in which the given data belongs to
            #Kmeans = open("models/Kmeans.pkl",'rb')
            #Kms = pickle.load(Kmeans)
            #Kmeans.close()
            #cluster = Kms.predict(df_xcn)
            #print("Cluster = ",cluster)
            #Finds the model to use based on the cluster
            file_list = os.listdir('models/')
            filename = self.get_fn(file_list)
            #Loading the model
            model_file = open("models/"+filename,'rb')
            model = pickle.load(model_file)
            model_file.close()
            #Predicting 
            print(filename)
            predicted_value = model.predict(df_xcn)
            print(predicted_value)
            data_frame["default_payment_next_month"] = predicted_value
            #Connects with the database
            
            db_ops = db_op(self.file_obj, self.logger_obj)
            session = db_ops.connect_db()
            print(session)
            #Inserting the whole data with prediction to database
            db_ops.db_input_predicted_data(data_frame,session)
            self.logger_obj.log(self.file_obj,' Predicted successfully..... \n')
            return predicted_value
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Error occured while started the prediction \n'+str(e))
            print('Error occured while started the prediction \n'+str(e))

    def get_fn(self,file_list):
        for i in file_list:
            if ".pkl" in i:
                return i


    ##Local function to find the model file to load
 #   def get_fn(self,file_list,cluster):
 #       for i in file_list:
 #           if str(cluster[0]) in i:
 #                return i