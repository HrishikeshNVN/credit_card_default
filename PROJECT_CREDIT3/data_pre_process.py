import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import OneHotEncoder

"""
   All data cleaning and data transformation performs from here.

   Written By: Hrishikesh Namboothiri V.N


"""


class Data_Pre_Process:

    
    def __init__(self,file_obj,logger_obj):

        self.file_obj = file_obj
        self.logger_obj = logger_obj
        self.logger_obj.log(self.file_obj,"Entered to Data_Preprocessing Class")
    
    """
      Method Name: space_cleaning
      Description: This method removes the unwanted spaces from given dataframe.
      Output: A pandas DataFrame after removing the spaces.
      On Failure: Raise Exception
      Written By: Hrishikesh Namboothiri V.N

    """

    def space_cleaning(self, dataf):
         
        self.logger_obj.log(self.file_obj," Started cleaning spaces in each cells in data frame ,whose dtype is 'object'")
        try:
            self.spaceless_data = dataf.apply(lambda x: x.strip() if x.dtype == "object" else x)
            self.logger_obj.log(self.file_obj,"Done space removal, Exits the space_cleaning method")
            return self.spaceless_data
        except Exception as e:
            self.logger_obj.log(self.file_obj,"Raised Exception in space_cleaning method"+str(e))
            self.logger_obj.log(self.file_obj,"Failed attempt to remove extra spcaes beacause of"+str(e))
            raise Exception()



    def nouse_columns_remove(self,dataf):
    
    
        """
                Method Name: nouse_columns_remove
                Description: This method removes the given unwanted columns from a pandas dataframe.
                Output: A pandas DataFrame after removing the specified columns.
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
        """
        
        self.logger_obj.log(self.file_obj,"Started to remove irrelevnt columns from dataframe")
        self.column = "ID"
        try:
            if self.column in dataf.columns:
                self.column_removed_df = dataf.drop(labels=self.column, axis = 1)
                self.logger_obj.log(self.file_obj,"Unwanted columns removed, Exit nouse_columns_remove method of Data_Pre_Process class")
                return self.column_removed_df
            else:
                self.logger_obj.log(self.file_obj,"Unwanted columns removed, Exit nouse_columns_remove method of Data_Pre_Process class")
                return dataf
        except Exception as e:
            self.logger_obj.log(self.file_obj,"Exception occured while removing unwanted columns, "+str(e))
            raise Exception()
        
        
    def split_dependent_independent(self,dataf):
    
      
        """
                Method Name: nouse_columns_remove
                Description: This method seperates the given dataframe into two pandas dataframes.
                Output: Two datafram. Dataframe of independent features and other with dependent feature.
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
        """
        
        dependent_column = "default_payment_next_month"
        self.logger_obj.log(self.file_obj, "Started to split_dependent_independent ")
        try:
            if dependent_column in dataf.columns:
                self.dependent = dataf[dependent_column]
                self.independent = dataf.drop(labels=dependent_column, axis=1)
                self.logger_obj.log(self.file_obj, "Seperated given dataframe to independent and dependent successfully, Exit split_dependent_independent method of class Data_Pre_Process")
                return self.independent, self.dependent
            else:
                return dataf
        except Exception as e:
            self.logger_obj.log(self.file_obj, "Exception occured while splitting data to independent and dependent"+str(e))
            raise Exception()
            
            
            
    def checks_for_null(self,data_independent):
    
      
        """
                Method Name: nouse_columns_remove
                Description: This method chceks for null values in given dataframe.
                Output: list of column name in the dataframe with null values and dataframe with column names and null value counts
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
        """
    
    
        self.logger_obj.log(self.file_obj, "Started to check for null values ")
        try:
            x = data_independent.isnull().sum()
            self.cols_with_null = list(x.index[x.values > 0])
            self.null_count_data = pd.DataFrame(data_independent.isnull().sum() , columns=["count of null"]).transpose()
            if len(self.cols_with_null) > 0:
                self.logger_obj.log(self.file_obj,"Found null values and corresponding columns, Exit from checks_for_null method from class Dta_Pre_Process")
            return self.cols_with_null, self.null_count_data
        except Exception as e:

            self.logger_obj.log(self.file_obj, "Exception occured while checking for null values"+str(e))
            raise Exception()
            
            
            
    def seperate_cat_num(self,dataf):
        
        """
        Method Name: balance_data
        Description: This method handles the imbalanced dataset to make it a balanced one.
        Output: new balanced feature and target columns
        On Failure: Raise Exception

        Written By: Hrishikesh Namboothiri V.N
        """
        
        self.logger_obj.log(self.file_obj,"Entered to seperate_cat_num for seperating to categorical and numerical dataset")
        try:   
            self.dataf_cat = dataf[['SEX', 'EDUCATION', 'MARRIAGE','PAY_0','PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']]
            self.dataf_num = dataf[['LIMIT_BAL','AGE','BILL_AMT1', 'BILL_AMT2','BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1','PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']]
            self.logger_obj.log(self.file_obj,"categorical and numerical data seperation success")
            return self.dataf_cat, self.dataf_num
        except Exception as e:
            self.logger_obj.log(self.file_obj,"Exception occured while seperating categorical and numerical data"+str(e))
            raise Exception() 
        
        
        
        


    def clean_cat_data(self,dataf):
        
        """
        Input: X_categorical dataframe and pre-defined clean_dict
        Action: Except AGE , replaceing each values (which are not belong to clean_dict) in X_categorical of each column
        with appropriate values
        Output: X_categorical with appropriate values
        """
        self.logger_obj.log(self.file_obj,"started cleaning categorical data")
        try:       
            self.clean_dict = {'SEX': [1,2,3], "EDUCATION":[1,2,3,4], "MARRIAGE": [1,2,3], "PAY_0": [-2,-1,0,1,2,3,4,5,6,7,8,9],
                    "PAY_2": [-2,-1,0,1,2,3,4,5,6,7,8,9],"PAY_3": [-2,-1,0,1,2,3,4,5,6,7,8,9],"PAY_4": [-2,-1,0,1,2,3,4,5,6,7,8,9],
                    "PAY_5": [-2,-1,0,1,2,3,4,5,6,7,8,9],"PAY_6": [-2,-1,0,1,2,3,4,5,6,7,8,9]}

            self.Xcp = dataf.copy()
            for i,j in self.clean_dict.items():
                self.Xcp[i] = self.Xcp[i].apply(lambda x: max(j) if x not in j else x)
                self.logger_obj.log(self.file_obj,"cleaned categorical data successfully.")
            return self.Xcp
        except Exception as e:
            self.logger_obj.log(self.file_obj,"Exception occured while cleaning categorical data"+str(e))
            raise Exception() 

                                   
                                   
                                   
                                   
                                   
                                   
    def categorical_data_encode(self,dataf):
        """
                Method Name: categorical_data_encode
                Description: This method encodes categorical values to numerical
                Output: Dataframe with encoded categorical values
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
                
        """
        cols = ['SEX', 'EDUCATION', 'MARRIAGE']
        try:
            self.logger_obj.log(self.file_obj,'Entered the categorical_data_encode method of Data_Pre_Process class')
            self.cat_enc_dataf = pd.get_dummies(dataf, columns=cols, prefix=cols, drop_first=True)
            self.logger_obj.log(self.file_obj,'Done categorical encoding successfuly, Exit categorical_data_encode method of Data_Pre_Process class')
            return self.cat_enc_dataf
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured encoding categorical data'+str(e))
            raise Exception()
                                   
                                   
        
                                   
  
    def freq_encode(self,dataf):
                                   
        """
        Input: X_categorical_trained_cleaned_nominal_encoded dataframe(X_categorical) and Frequncy dictionary from create_freq_dict.
        Action: Frequncy encode columns in predefined "cols" in X_categorical
        Output: X_categorical with frequency encoded
        
        """                            
                                   
                                   
        freq_dict ={'PAY_0': {0: 0.4904,
  -1: 0.1879,
  1: 0.1217,
  -2: 0.0932,
  2: 0.091,
  3: 0.0106,
  4: 0.003,
  5: 0.001,
  8: 0.0006,
  6: 0.0003,
  7: 0.0003},
 'PAY_2': {0: 0.5221,
  -1: 0.2019,
  2: 0.133,
  -2: 0.1257,
  3: 0.0109,
  4: 0.0035,
  1: 0.001,
  5: 0.0008,
  7: 0.0006,
  6: 0.0004,
  8: 0.0},
 'PAY_3': {0: 0.5249,
  -1: 0.1969,
  -2: 0.1358,
  2: 0.1291,
  3: 0.0084,
  4: 0.0024,
  5: 0.0008,
  6: 0.0008,
  7: 0.0007,
  1: 0.0002,
  8: 0.0001},
 'PAY_4': {0: 0.5458,
  -1: 0.1906,
  -2: 0.1449,
  2: 0.107,
  3: 0.0062,
  4: 0.0023,
  7: 0.0018,
  5: 0.0011,
  6: 0.0002,
  1: 0.0001,
  8: 0.0001},
 'PAY_5': {0: 0.5623,
  -1: 0.1867,
  -2: 0.1506,
  2: 0.0885,
  3: 0.0065,
  4: 0.0027,
  7: 0.0019,
  5: 0.0007,
  6: 0.0001,
  8: 0.0},
 'PAY_6': {0: 0.5392,
  -1: 0.1929,
  -2: 0.163,
  2: 0.0942,
  3: 0.0066,
  4: 0.0016,
  7: 0.0014,
  6: 0.0007,
  5: 0.0003,
  8: 0.0}}
        
        self.logger_obj.log(self.file_obj,'Started frequency encoding nominal data')
        
        try:
            cols = ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']
            for var in cols:
                dataf[var] = dataf[var].map(freq_dict[var])
            self.logger_obj.log(self.file_obj,'Successful frequency encoding nominal data')
            return dataf                
        except Exception as e:

            self.logger_obj.log(self.file_object,'Exception occured while frequency encoding nominal data'+str(e))

            raise Exception()


   
                                   
                                   
                                   

    def impute_missing_num_data(self,dataf):
        
        """
        Input: X_numerical dataframe
        Action: If any value missing in X_numerical , using most_frequent strategy Simple imputer imputes the missing values. 
        Output: X_numerical with appropriate values
        
    
        """
        columns = ['LIMIT_BAL','AGE','BILL_AMT1', 'BILL_AMT2','BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1','PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']
        self.logger_obj.log(self.file_obj,'Started imputing_missing_numerical_data ')
        try:
            self.logger_obj.log(self.file_obj,'Started imputing numerical data')                         
            self.Xcp = dataf.copy()
            self.si = SimpleImputer(strategy="most_frequent")
            for i in columns:
                self.si.fit(self.Xcp[[i]])
                if i == "default.payment.next.month":
                    break
                self.Xcp[[i]] = self.si.transform(self.Xcp[[i]])
                if i == "AGE":
                    self.Xcp[i] = self.Xcp[i].apply(int)
            self.logger_obj.log(self.file_obj,'Successfully imputed_missing_numerical_data ')
            return self.Xcp                    
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured while scaling numeric data'+str(e))
            raise Exception()
                                   
                                   
                                   
    
    def balance_data(self,x,y):
    
    
        """
        Method Name: balance_data
        Description: This method handles the imbalanced dataset to make it a balanced one.
        Output: new balanced feature and target columns
        On Failure: Raise Exception

        Written By: Hrishikesh Namboothiri V.N
        """
        
        self.x = x
        self.y = y
        self.logger_obj.log(self.file_obj,"Entered to balance_data method for balancing dataset")

        try:
            self.ros = RandomOverSampler()
            self.x_sampled , self.y_sampled = self.ros.fit_resample(self.x, self.y)
            self.logger_obj.log(self.file_obj,"Dataset balanced by balance_data method in class Data_Pre_Process ")
            self.x_sampled.replace(np.nan,0, inplace = True)
            self.x_sampled.replace(np.inf,1, inplace = True)
            self.x_sampled.replace(-np.inf,-1, inplace = True)
            self.logger_obj.log(self.file_obj,'Successfully balanced_data, method of Data_Pre_Process class')
            return self.x_sampled , self.y_sampled
        except Exception as e:
            self.logger_obj.log(self.file_obj,"Exception occured while balancing data"+str(e))
            raise Exception() 
                                   
                                   
                                   
    
    def scales_data(self,dataf):

        """
        Method Name: scale_numerica_data
        Description: This method scales the numerical values using the Standard scaler.
        Output: A dataframe with scaled values
        On Failure: Raise Exception
        Written By: Hrishikesh Namboothiri V.N
        """
        try: 
            self.logger_obj.log(self.file_obj,'Entered the scale_numerical_data method of Data_Pre_Process class')


            self.dataf = dataf
            self.dataf_numeric = self.dataf.select_dtypes(include=["int64","float64"]).copy()
            self.dataf_categoric = self.dataf.select_dtypes(exclude=["int64","float64"]).copy()
            self.scalar = StandardScaler()
            self.scaled_dataf = pd.DataFrame(data=self.scalar.fit_transform(self.dataf_numeric) , columns=self.dataf_numeric.columns)
            self.logger_obj.log(self.file_obj,'Done Numeric data scaling, Exit scales_numeric_data method in Data_Pre_Process class')
            data = pd.concat([self.dataf_categoric,self.dataf_numeric], axis=1)
            data.replace(np.nan,0, inplace = True)
            data.replace(np.inf,1, inplace = True)
            data.replace(-np.inf,-1, inplace = True)
            self.logger_obj.log(self.file_obj,'Successfully scaled_numerical_data, method of Data_Pre_Process class')
            return data
        except Exception as e:

            self.logger_obj.log(self.file_obj,'Exception occured while scaling numeric data'+str(e))

            raise Exception()
            
            
    
    def create_one_hot(self,X):
        
        oh_dict = {}

        cols = ["SEX","EDUCATION","MARRIAGE"]

        try:
            for i in cols:
                if i == "SEX":
                    oh = OneHotEncoder(drop="if_binary") 
                    oh.fit(X[[i]])
                    oh_dict[i] = oh
                else:
                    oh = OneHotEncoder(drop="first")
                    oh.fit(X[[i]])
                    oh_dict[i] = oh
            self.logger_obj.log(self.file_obj,'')
            return oh_dict
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured at create_one_hot method data'+str(e))

    
    
    
    
    def create_one_hot1(self):  


        columns = ["SEX","EDUCATION","MARRIAGE"]
        oh_dict = {}
        SEX = pd.DataFrame([1,2],columns=["SEX"])
        MARRIAGE = pd.DataFrame([1,2,3], columns=["MARRIAGE"])
        EDUCATION = pd.DataFrame([1,2,3,4], columns=["EDUCATION"])
        df_list = [SEX,MARRIAGE,EDUCATION]

        self.logger_obj.log(self.file_obj,'Started to execute create_one_hot1 method data \n ')

        try:
            for i in df_list:

                if(i.columns[0] == 'SEX'):
                    oh = OneHotEncoder(drop="if_binary") 
                    oh.fit(i)
                    oh_dict[i.columns[0]] = oh
                else:
                    oh = OneHotEncoder(drop="first")
                    oh.fit(i)
                    oh_dict[i.columns[0]] = oh

            self.logger_obj.log(self.file_obj,'Successfully executed create_one_hot1 method data \n ')
            return oh_dict

        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured at create_one_hot1 method data'+str(e))

        
    
    
    
    def oh_encode1(self,oh_dict,x):
        
        c = ["SEX","MARRIAGE","EDUCATION"]
        try:
            for i in c:

                oh = oh_dict[i]
                x_tra = pd.DataFrame(oh.transform(x[[i]]).toarray())
                #print(x_tra.axes[1])


                col_x_tra = list(x_tra.axes[1])
                fn = lambda a : i+"_"+str(a+1) 
                columns1 = list(map(fn,col_x_tra))
                x[columns1] = x_tra[col_x_tra].values
                x.drop(labels=[i], axis=1, inplace=True)
                    #df_new = x_tra.reset_index(drop=True)
                    #x_n = x.reset_index(drop=True)
                    #h = pd.concat([x,df_new],axis=0)
                    #result = pd.concat([x, x_tra], axis=1, ignore_index=True)
                    #if "SEX_1" in df1.columns:
                    #x.rename(columns = {'SEX_1':'SEX_2'}, inplace = True)
            self.logger_obj.log(self.file_obj,'Data Successfully one hot encoded, oh_encode1 data')
            return x
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured at oh_encode1 data'+str(e))

        
    
    

    def oh_encode(self,oh_dict,x):

        cols = ['SEX','EDUCATION','MARRIAGE']
        
        try:
            for i in cols:

                oh = oh_dict[i]
                x_tra = pd.DataFrame(oh.transform(x[[i]]).toarray())
                
                col_x_tra = list(x_tra.axes[1])
                fn = lambda a : i+"_"+str(a+1) 
                columns1 = list(map(fn,col_x_tra))
                        #x_tra
                x[columns1] = x_tra[col_x_tra].values
                x.drop(labels=[i], axis=1, inplace=True)
                    #df_new = x_tra.reset_index(drop=True)
                    #x_n = x.reset_index(drop=True)
                    #h = pd.concat([x,df_new],axis=0)
                    #result = pd.concat([x, x_tra], axis=1, ignore_index=True)

            if "SEX_1" in x.columns:
                x.rename(columns = {'SEX_1':'SEX_2'}, inplace = True)
        except Exception as e:
            self.logger_obj.log(self.file_obj,'Exception occured at oh_encode data'+str(e))
 

        return x