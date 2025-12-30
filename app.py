from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
import os
import sqlite3
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load google Model to provide sql queries from text
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve data from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

prompt = [
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
    """
]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    question = ""
    if request.method == 'POST':
        question = request.form['question']
        if question:
            response = get_gemini_response(question, prompt)
            print(f"Gemini Response: {response}")
            # Basic cleanup if Gemini returns markdown code blocks despite instructions
            clean_sql = response.replace("```sql", "").replace("```", "").strip()
            try:
                result = read_sql_query(clean_sql, 'student.db')
            except Exception as e:
                result = [f"Error executing query: {e}"]
    
    return render_template('index.html', result=result, question=question)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
