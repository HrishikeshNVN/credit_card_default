from flask import Flask, render_template, request
from predict_functions import Predict_Class as p_class
import pandas as pd
from training import TrainModel as tr_mdl

app = Flask(__name__)

print("Hello")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/checks")
def checks():
    return render_template("index.html")


@app.route("/predict" , methods=["POST"])
def predict():
    if request.method == "POST":
        
        if request.form['sub'] == 'PREDICT':
                  
              
            LIMIT_BAL = request.form["LIMIT_BAL"]
            AGE = request.form["AGE"]
            EDUCATION = request.form["EDUCATION"]
            SEX = request.form["SEX"]
            MARRIAGE = request.form["MARRIAGE"]
            PAY_0 = request.form["PAY_0"]
            PAY_2 = request.form["PAY_2"]
            PAY_3 = request.form["PAY_3"]
            PAY_4 = request.form["PAY_4"]
            PAY_5 = request.form["PAY_5"]
            PAY_6 = request.form["PAY_6"]
            BILL_AMT1 = request.form["BILL_AMT1"]
            BILL_AMT2 = request.form["BILL_AMT2"]
            BILL_AMT3 = request.form["BILL_AMT3"]
            BILL_AMT4 = request.form["BILL_AMT4"]
            BILL_AMT5 = request.form["BILL_AMT5"]
            BILL_AMT6 = request.form["BILL_AMT6"]
            PAY_AMT1 = request.form["PAY_AMT1"]
            PAY_AMT2 = request.form["PAY_AMT1"]
            PAY_AMT3 = request.form["PAY_AMT1"]
            PAY_AMT4 = request.form["PAY_AMT1"]
            PAY_AMT5 = request.form["PAY_AMT1"]
            PAY_AMT6 = request.form["PAY_AMT1"]
            
            columns = ["LIMIT_BAL","SEX","EDUCATION","MARRIAGE","AGE","PAY_0","PAY_2","PAY_3","PAY_4","PAY_5","PAY_6",
            "BILL_AMT1","BILL_AMT2","BILL_AMT3","BILL_AMT4","BILL_AMT5","BILL_AMT6","PAY_AMT1","PAY_AMT2","PAY_AMT3","PAY_AMT4","PAY_AMT5","PAY_AMT6"]

            to_show1 = list(map(int,[LIMIT_BAL,SEX,EDUCATION,MARRIAGE,AGE,PAY_0,PAY_2,PAY_3,PAY_4,PAY_5,PAY_6]))
            to_show2 = list(map(float,[BILL_AMT1,BILL_AMT2,BILL_AMT3,BILL_AMT4,BILL_AMT5,BILL_AMT6,PAY_AMT1,PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6]))
            to_show3 = [to_show1+to_show2]
            df = pd.DataFrame(to_show3, columns=columns)
            print(df)
            pred = p_class()
            predicted_value = pred.predict(df)
            print("PREDICTED VALUE IS....",predicted_value)
    if predicted_value == 1:
        return render_template("show.html", content = "Will default")

    elif predicted_value == 0:
        return render_template("show.html", content = "Won't Default....")


@app.route("/train")
def train():
    tr = tr_mdl()
    tr.model_training()
    return f"<h2>Training done successfully</h2>"


if __name__ == '__main__':
    app.run(debug=True)