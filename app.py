from dotenv import load_dotenv

#load environment variables from a .env file
load_dotenv()

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

#configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Function to load google Model to provide sql queries from text

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel("gemini-2.5-flash")
    response=model.generate_content([prompt[0],question])
    return response.text

# function to retrieve data from the database

def read_sql_quer(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
        print(row)
    return rows

promt=[
    """
     You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    \nNow, answer the following question based on the above information.
    
    """,
]

#streamlit app code
st.set_page_config(page_title="Text to SQL using Gemini-1.5",page_icon=":robot_face:")
st.header("Text to SQL using Gemini-1.5 :robot_face:")
question=st.text_input("Input:",key="input")
submit=st.button("Ask the question")

if submit:
    response=get_gemini_response(question,promt)
    print(response)
    data=read_sql_quer(response,'student.db')
    st.subheader("SQL Query:")
    for row in data:
        print(row)
        st.header(row)