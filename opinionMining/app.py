from flask import Flask, render_template, request, flash, redirect
from flask_bootstrap import Bootstrap
import sqlite3
import pickle
import random
import time
from inspect import getmembers
from pprint import pprint

import pandas as pd
#NLP packages




pickle_in = open('opinionMining.pkl', 'rb')
model = pickle.load(pickle_in)
# prediction = model.predict([[1,3,2,4,5,2,3,1,2,4]])
#print(prediction)



app = Flask(__name__, static_url_path='/static')
Bootstrap(app)



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            matric_no = request.form['matric_no']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            department = request.form['department']
            level = request.form['level']
            password = request.form['password']
            with sqlite3.connect("student_data.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into students (matric_no, first_name, last_name, department, level, password)VALUES(?,?,?,?,?,?)",
                            (matric_no, first_name, last_name, department, level, password))
                con.commit()
                msg = "Registration Complete."
        except:
            con.rollback()
            msg = "Unable to complete registration."
            return render_template("home.html", msg=msg)
        finally:
            return render_template("login.html", msg=msg)




@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/getinfo', methods=['POST','GET'])
def getinfo():
    if request.method == 'POST':
        try:
            matric_no = request.form['matric_no']
            password = request.form['password']
            with sqlite3.connect("student_data.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM students WHERE matric_no = '%s' AND password = '%s'" % (matric_no, password))
                if cur.fetchone() is not None:
                    return render_template("survey.html")
                else:
                    msg = "Login Failed."
                    return render_template("login.html", msg=msg)
        except:
            error = "Try again."
            return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    return render_template('home.html')


@app.route('/survey')
def survey():
    return render_template('survey.html')

result = random.randint(0,1)
@app.route('/analyse', methods=['POST', 'GET'])
def analyse():
    global result
    if request == 'POST':
        lecturer = request.form['lecturer']
        course_code = request.form['course_code']
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        q6 = request.form['q6']
        q7 = request.form['q7']
        q8 = request.form['q8']
        q9 = request.form['q9']
        q10 = request.form['q10']
        prediction = model.predict([[q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]])
        result = random.randint(0, 1)

        with sqlite3.connect("opinion_data.db") as con:
            cur = con.cursor()
            cur.execute("INSERT into opinions (lecturer TEXT, course_code TEXT, q1 VARCHAR, "
                        "q2 VARCHAR, q3 VARCHAR, q4 VARCHAR, q5 VARCHAR,"
                        " q6 VARCHAR, q7 VARCHAR, q8 VARCHAR, q9 VARCHAR, q10 VARCHAR, result VARCHAR"
                        ")VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (lecturer, course_code, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, result))
            con.commit()

    return render_template('result.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    if request.form['password'] == 'admin1234' and request.form['username'] == 'admin':
        return redirect('/dashboard')
    else:
        flash('wrong password!')

@app.route('/dashboard')
def dashboard():
    con = sqlite3.connect("student_data.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()


    conn = sqlite3.connect("opinion_data.db")
    conn.row_factory = sqlite3.Row
    curr = conn.cursor()
    curr.execute("SELECT * FROM opinions")
    data = curr.fetchall()
    return render_template("dashboard.html", rows=rows, data=data)




if __name__ == '__main__':
    app.run(debug=True)