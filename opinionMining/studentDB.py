import sqlite3 as sql

"""con = sql.connect('student_data.db')
print("Database opened successfully")


con.execute("CREATE TABLE students (matric_no VARCHAR PRIMARY KEY, first_name TEXT,"
            " last_name TEXT, department CHARACTER, level VARCHAR, password VARCHAR)")
print("Table created successfully")
con.close()"""


con = sql.connect('opinion_data.db')
print("Database opened successfully")


con.execute("CREATE TABLE opinions (lecturer VARCHAR, course_code VARCHAR,q1 VARCHAR, q2 VARCHAR, "
            "q3 VARCHAR, q4 VARCHAR, q5 VARCHAR, q6 VARCHAR, q7 VARCHAR, q8 VARCHAR, q9 VARCHAR, q10 VARCHAR, result VARCHAR)")
print("Table created successfully")
con.close()
