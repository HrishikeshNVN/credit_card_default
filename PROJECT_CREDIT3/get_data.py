import os
import pandas as pd

class Get_Data:
    
    """
    This class shall  be used for obtaining the data from the source for training.

    Written By: Hrishikesh Namboothiri.V.N

    """
    
    
    def __init__(self,file_object,logger_object):
        
#       self.path1 = "YET_TO_TRAIN.csv"
#        self.path2 = "TRAINED.csv"
    
        self.logger_object = logger_object
        self.file_object = file_object

    def get_file(self,file_name):
        
        """
         Method Name: get_file_to_train
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

         Written By: Hrishikesh Namboothiri.V.N
        """
        self.logger_object.log(self.file_object,"Entered get_file_to_train of Get_Data")
        
        try:
            if os.path.isfile(file_name):
                self.logger_object.log(self.file_object,"Found new file to train")
                self.df = pd.read_csv(file_name)
                self.logger_object.log(self.file_object,"Collected data from TRAIN and Exit Get_Data")
 #               self.df = self.df[['ID', 'AGE', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3',
  #     'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'EDUCATION', 'LIMIT_BAL',
  #     'MARRIAGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
  #     'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6',
  #     'SEX', 'default_payment_next_month']]
                
                return self.df
                          
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in get_file_to_train method of the Get_Data class. Exception message: '+str(e))
            self.logger_object.log(self.file_object,'Data Load Unsuccessful.Exited the get_file_to_train method of the Get_Data class')
            raise Exception()