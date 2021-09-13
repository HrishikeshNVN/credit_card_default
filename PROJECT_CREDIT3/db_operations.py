from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import PreparedStatement
from cassandra.query import SimpleStatement, BatchStatement
from numpy import dtype
import pandas as pd
import os


"""
                Class Name: Db_Operations
                Description: This class performs all the database related functions.
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
"""


class Db_Opeartions:
    
    def __init__(self,file_obj,logger_obj):
        
        self.file_obj = file_obj
        self.logger_obj = logger_obj
        
        
    def connect_db(self):


        """
                Method Name: connect_db
                Description: This method establishe connection with cassandra database.
                Output: Connector object to connect with database for all database operations..
                On Failure: Raise Exception

                Written By: Hrishikesh Namboothiri V.N
        """

        
        self.logger_obj.log(self.file_obj,"Started to Connect Database \n")
        try:
            cloud_config= {
                    'secure_connect_bundle': 'database_folder/secure-connect-credit-card-default.zip'
            }
            auth_provider = PlainTextAuthProvider(
                username=os.environ['CASSANDRA_USERNAME'], 
                password=os.environ['CASSANDRA_PASSWORD']
            )
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()
            row = session.execute("select release_version from system.local").one()
            if row:
                print(row[0])
                connection_status = 1
            else:
                print("An error occurred.")
                connection_status = 0  
            self.logger_obj.log(self.file_obj,"Database connected successfully \n")
            row = session.execute("SELECT * FROM project_credit.new_data;")
            for i in row:
                print(i)

            return session 
        except Exception as e:
            self.logger_obj.log(self.file_obj,"Error occured while connected with Database"+str(e))




    ##checks wether a table exist or not 

    def db_input_predicted_data(self,data,session):

        self.logger_obj.log(self.file_obj,"Entered to db_input_predicted_data")
        
        self.logger_obj.log(self.file_obj,"\n Insert new data to to_train_Table \n")
        
        row = session.execute("SELECT table_name  FROM system_schema.tables WHERE keyspace_name='project_credit';")
        table_name = []
        for i in row:
            table_name.append(i[0])
            
        data = tuple(data.iloc[0][:])
        #print(data)
        if "new_data" in table_name:
           
            ## If table exists insert the data
            try:
                session.execute("insert into project_credit.new_data(ID,LIMIT_BAL,SEX,EDUCATION,MARRIAGE,AGE,PAY_0,PAY_2,PAY_3,PAY_4,PAY_5,PAY_6,BILL_AMT1,BILL_AMT2,BILL_AMT3,BILL_AMT4,BILL_AMT5,BILL_AMT6,PAY_AMT1,PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6,default_payment_next_month) values(uuid(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",data).one()
                #session.execute("select count(*) from project_credit.new_data;")
            except Exception as e:
                self.logger_obj.log(self.file_obj,"error occured at db_input_predicted_data method in db_operations module \n"+str(e))

            
        else:
            ##As table does not exit we creates and insert value
            try:
                session.execute("create table project_credit.new_data(ID uuid,LIMIT_BAL decimal,SEX decimal,EDUCATION decimal,MARRIAGE decimal,AGE decimal,PAY_0 decimal,PAY_2 decimal,PAY_3 decimal,PAY_4 decimal,PAY_5 decimal,PAY_6 decimal,BILL_AMT1 decimal,BILL_AMT2 decimal,BILL_AMT3 decimal,BILL_AMT4 decimal,BILL_AMT5 decimal,BILL_AMT6 decimal,PAY_AMT1 decimal,PAY_AMT2 decimal,PAY_AMT3 decimal,PAY_AMT4 decimal,PAY_AMT5 decimal,PAY_AMT6 decimal,default_payment_next_month decimal,PRIMARY KEY(id));").one()
                session.execute("insert into project_credit.new_data(ID,LIMIT_BAL,SEX,EDUCATION,MARRIAGE,AGE,PAY_0,PAY_2,PAY_3,PAY_4,PAY_5,PAY_6,BILL_AMT1,BILL_AMT2,BILL_AMT3,BILL_AMT4,BILL_AMT5,BILL_AMT6,PAY_AMT1,PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6,default_payment_next_month) values(uuid(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",data).one()
                self.logger_obj.log(self.file_obj,"\n Successfully Inserted new data to new_data table \n")
                return print("Data entered successfully")
            except Exception as e:
                self.logger_obj.log(self.file_obj,"error occured at db_input_predicted_data method in db_operations module \n"+str(e))

        
        
        
        



        """
        
            def db_Input_predicted_Data(data):
        
        self.logger_obj.log(self.file_obj,"\n Insert new data to new_data table in keyspace project_credit \n")
        
        row = session.execute("SELECT table_name  FROM system_schema.tables WHERE keyspace_name='student_data';")
        table_name = []
        for i in row:
            table_name.append(i[0])

        if "project_credit" in table_name:
            ## If table exists insert the data
            session.execute("insert into project_credit.new_data(ID,LIMIT_BAL,SEX,EDUCATION,MARRIAGE,AGE,PAY_0,PAY_2,PAY_3,PAY_4,PAY_5,PAY_6,BILL_AMT1,BILL_AMT2,BILL_AMT3,BILL_AMT4,BILL_AMT5,BILL_AMT6,PAY_AMT1,PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6,default_payment_next_month) values(uuid(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",data).one()

        else:
            ##As table does not exit we creates and insert value
            session.execute("create table project_credit.new_data(id uuid,limit_bal decimal,SEX decimal,EDUCATION decimal,MARRIAGE decimal,AGE decimal,PAY_0 decimal,PAY_2 decimal,PAY_3 decimal,PAY_4 decimal,PAY_5 decimal,PAY_6 decimal,BILL_AMT1 decimal,BILL_AMT2 decimal,BILL_AMT3 decimal,BILL_AMT4 decimal,BILL_AMT5 decimal,BILL_AMT6 decimal,PAY_AMT1 decimal,PAY_AMT2 decimal,PAY_AMT3 decimal,PAY_AMT4 decimal,PAY_AMT5 decimal,PAY_AMT6 decimal,default_payment_next_month decimal,PRIMARY KEY(id))").one()
            session.execute("insert into project_credit.new_data(ID,LIMIT_BAL,SEX,EDUCATION,MARRIAGE,AGE,PAY_0,PAY_2,PAY_3,PAY_4,PAY_5,PAY_6,BILL_AMT1,BILL_AMT2,BILL_AMT3,BILL_AMT4,BILL_AMT5,BILL_AMT6,PAY_AMT1,PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6,default_payment_next_month) values(uuid(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",data).one()

        self.logger_obj.log(self.file_obj,"\n Successfully Inserted new data to new_data table \n")
        
        return print("Data entered successfully")
        
        """
    
    
    def db_data_to_train(self,session):

    
        df = pd.DataFrame()


        try:
            row = session.execute("SELECT table_name  FROM system_schema.tables WHERE keyspace_name='project_credit';")
            table_name = []
            for i in row:
                table_name.append(i[0])
            print(table_name)
            if "new_data" in table_name:
                row=session.execute("SELECT count(*) FROM project_credit.new_data;")
                print(row[0][0])
                if row[0][0] >= 30000:
                    print("from db_operations",row[0][0])
                    for row in session.execute('SELECT * FROM project_credit.new_data;'):
                        df = df.append(pd.DataFrame(row , index=row._fields).transpose())
                    df.to_csv("Data/TRAIN_DATA.csv")
                    return "Data/TRAIN_DATA.csv"
                else:
                    print("db to trainnnnnnnnnn")
                    for row1 in session.execute('SELECT * FROM project_credit."UCI_Credit_Card";'):
                        df = df.append(pd.DataFrame(row1 , index=row1._fields).transpose())
                        df = df.apply(pd.to_numeric)
                    df1 = pd.DataFrame()
                    for row2 in session.execute("SELECT * FROM project_credit.new_data;"):
                        df1 = df1.append(pd.DataFrame(row2 , index=row2._fields).transpose())
                        df1 = df1.apply(pd.to_numeric)

                    df2 = pd.concat([df,df1], axis=0)
                    df2.to_csv("Data/TRAIN_DATA.csv")
                    file_name = "Data/TRAIN_DATA.csv"
                    self.logger_obj.log(self.file_obj,"\n Successfully downloaded new data to train models \n")
                    print(file_name)
                    return file_name 
        except Exception as e:
                self.logger_obj.log(self.file_obj,"\n Error occure while downloading new data to train models \n"+str(e))
                print("ERROR FROM DB....."+str(e))
        
#        try:
#            row = session.execute("select count(*) from student_data.to_train_Table;")
#        
#            if (int(row[0][0]) >= 15000):
#                #for row in session.execute("SELECT * FROM student_data.to_train_Table;"):
#                   # df = df.append(pd.DataFrame(row , index=row._fields).transpose())
#                file_name = self.to_train_Table_from_db(session)
#                self.push_data_to_UCIdb(session)
#                return file_name
#        except:
        """
    
    def db_Data_To_Train():
    
    df = pd.DataFrame()
    
    
    row=session.execute("SELECT count(*) FROM project_credit.new_data;")
    if row[0][0] >= 30000:

        for row in session.execute("SELECT * FROM project_credit.new_data;"):
            df = df.append(pd.DataFrame(row , index=row._fields).transpose())
        
        df.to_csv("TRAIN_DATA.csv")
        return pd.read_csv("TRAIN_DATA.csv")
    
    else:
    
        for row in session.execute("SELECT * FROM project_credit.uci_credit_data;"):
            df = df.append(pd.DataFrame(row , index=row._fields).transpose())
         
        df1 = pd.DataFrame()
        for row in session.execute("SELECT * FROM project_credit.new_data;"):
            df1 = df1.append(pd.DataFrame(row , index=row._fields).transpose())
            
     
    df2 = pd.concat([df,df1], axis=0)
    df2.to_csv("TRAIN_DATA.csv")
    file_name = "TRAIN_DATA.csv"

    return file_name
    
"""
    
       
 




    