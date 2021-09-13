import pandas as pd
from Get_Data import Get_Data as get_data_frame ## CLASS USE To get the file to train
from Data_Pre_Process import Data_Pre_Process as pre_process ## mODULE TO DO ALL PRE PROCESSING


class data_to_train:
    
    def __init__(self,file_obj,logger_obj):
        
        self.file_obj = file_obj
        self.logger_obj = logger_obj
        self.get_df = get_data_frame(self.file_obj,self.logger_obj)
        
            
    
    def final_data_to_train(self):
        
        self.logger_obj.log(self.file_obj, "\\\\\\\\\\\\\\\\\\\\\\\STARTED TO PREPARE DATA FOR TRAINING ///////////////////////")               
        data = self.get_df.get_file_to_train()
        data_pre_pro = pre_process(self.file_obj,self.logger_obj)
        
        dataf = data_pre_pro.nouse_columns_remove(data)
        
        dfx, dfy = data_pre_pro.split_dependent_independent(dataf)
        
        cols, null_col_df = data_pre_pro.checks_for_null(dfx)
        
        df_cat, df_num = data_pre_pro.seperate_cat_num(dfx)
        
        df_cat = data_pre_pro.clean_cat_data(df_cat)
        
        df_cat_enc = data_pre_pro.categorical_data_encode(df_cat)
        
        df_cat_fren = data_pre_pro.freq_encode(df_cat_enc)
        
        df_num = data_pre_pro.impute_missing_num_data(df_num)
        
        df_to_scale  = pd.concat([df_cat_fren,df_num], axis=1)

        df_scaled = data_pre_pro.scales_data(df_to_scale)
        
        dfy = pd.DataFrame(dfy)
        
        dfy_cp = dfy.copy()
        
        #x, y = data_pre_pro.balance_data(df_scaled, dfy)
        
        return x, y
        