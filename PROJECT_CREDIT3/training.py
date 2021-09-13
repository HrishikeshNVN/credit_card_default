import pandas as pd
import numpy as np
from get_data import Get_Data as get_df  ## CLASS USE To get the file to train
from data_pre_process import Data_Pre_Process as dpre ## MODULE TO DO ALL PRE PROCESSING
from application_logging import logger as logger  # For logging
from find_model_for_clusters import Find_Model_Cluster as fi_mo_cl ##To find and create suitable model for each cluster
from clustering_data_class import Clusterning_Data as cluster_data #For clustering data
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
from db_operations import Db_Opeartions as db_ops
import os, shutil

class TrainModel:
    
    def __init__(self):
    
        self.file_obj = open("trainModel_logs.txt" , "a+")
        self.logger_obj = logger.App_Logger()
    
    def model_training(self):
        
        self.logger_obj.log(self.file_obj, '\n Training Started \n')
        
        try:
            #db_op = db_ops(self.file_obj,self.logger_obj)
            #session = db_op.connect_db()
            #file_name = db_op.db_data_to_train(session)
            
            file_name = "Data/TRAIN_DATA.csv"
            gdf = get_df(self.file_obj,self.logger_obj) 
            df = gdf.get_file(file_name)
            dat_pre = dpre(self.file_obj,self.logger_obj)
            df = dat_pre.space_cleaning(df)
            df = dat_pre.nouse_columns_remove(df)
            dfx, dfy = dat_pre.split_dependent_independent(df)
            cols, null_col_df = dat_pre.checks_for_null(dfx)
            df_cat, df_num = dat_pre.seperate_cat_num(dfx)
            cols = df_num.columns
            df_cat[cols] = df_num[cols].values
            df_cat = dat_pre.clean_cat_data(df_cat)
            oh_dict = dat_pre.create_one_hot1()
            df_enc = dat_pre.oh_encode1(oh_dict,df_cat)
            print(df_enc.columns)
            #df_cat_enc = dat_pre.categorical_data_encode(df_cat)
            df_cat_fr_en = dat_pre.freq_encode(df_enc)
            df_xcn = dat_pre.impute_missing_num_data(df_cat_fr_en)
            #df_xcn = pd.concat([df_cat_fr_en,df_num], axis=1)
            df_xcn = dat_pre.scales_data(df_xcn)
            df_x , df_y = dat_pre.balance_data(df_xcn,dfy)
            #df_xcn = pd.concat([df_x,df_y], axis=1)
            #print(df_xcn)
            ##Clustering the pre processed data
            #cluster_d = cluster_data(self.file_obj,self.logger_obj)
            #df_x, no_of_cluster = cluster_d.clustering(df_x)
            #df_x["Y"] = df_y

            ##For each cluster finds best algorith and creates best model respectively.
            #for i in range(no_of_cluster):


             #   clustered_data = df_x[df_x["cluster"]==i]
             #   clustered_x = clustered_data.drop(labels = ["cluster","Y"], axis = 1)
             #   clustered_y = clustered_data["Y"]
             #   x_tr, x_ts, y_tr, y_ts = train_test_split(clustered_x, clustered_y, test_size=0.3, random_state=0)
            x_tr, x_ts, y_tr, y_ts = train_test_split(df_x, df_y, test_size=0.3, random_state=0)

            fmc = fi_mo_cl(self.file_obj,self.logger_obj)

            model, model_name = fmc.best_model(x_tr, x_ts, y_tr, y_ts)


            file = open("models/"+model_name+".pkl" , "wb")
            pickle.dump(model,file)
            file.close
            self.remove_old_models() 
            self.logger_obj.log(self.file_obj, '\n Training Completed Successfully \n')    
        except Exception as e:
            self.logger_obj.log(self.file_obj, '\n Exception occured while training'+str(e)+'\n')
            raise Exception()
            


    def remove_old_models(self):        
            folder = 'models/'
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                self.logger_obj.log(self.file_obj, '\n Started to remove old files \n')
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    self.logger_obj.log(self.file_obj,'Failed to delete %s. Reason: %s' % (file_path, e))
                        