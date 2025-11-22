import os
import sqlite3
from groq import Groq
import streamlit as st
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# ---------------- CONFIG ----------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
DB_PATH = r"text2sql.db"

# ---------------- GET SCHEMA ----------------
def get_db_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    schema = ""
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    for t in tables:
        table_name = t[0]
        schema += f"\nTable: {table_name}\nColumns:\n"
        cur.execute(f"PRAGMA table_info({table_name});")
        cols = cur.fetchall()
        for col in cols:
            schema += f" - {col[1]} ({col[2]})\n"

    conn.close()
    return schema

schema_text = get_db_schema()

# ---------------- MODEL PROMPT ----------------
SYSTEM_PROMPT = f"""
You are a Text-to-SQL RAG Query Assistant.

ONLY use the tables and columns exactly as shown below.

DATABASE SCHEMA:
{schema_text}

TABLE RELATIONSHIPS AND CHEAT SHEET:
- STUDENT.CLASS represents the class a student is enrolled in.
- TEACHER.SUBJECT represents the subject a teacher teaches.
- A student is considered to be taught by a teacher if STUDENT.CLASS matches TEACHER.SUBJECT.
- ADDRESS.ROLL_NO links to STUDENT.ROLL_NO (for student addresses).
- STUDENT.ROLL_NO links to TEACHER.ROLL_NO only if explicitly mapped (not automatically assumed).

STRICT RULES:
1. Always generate SQL only using the tables and columns in the schema.
2. Only create joins if the relationship is explicitly defined in the cheat sheet.
3. If the user question references multiple tables but the relationship is unclear, respond exactly:
   "Error: Question is incomplete or unclear. Please clarify table relationships or conditions."
4. Do NOT guess or hallucinate any column, table, or value.
5. Always generate case-insensitive SQL using:
   LOWER(column_name) = LOWER('value')
6. Only output the SQL query. No extra explanations.
7. If the user question references a non-existent column or table, respond with:
   "Error: Column not found in database schema." or "Error: Table not found."
8. If the user question is unrelated to SQL, respond with:
   "Error: Question is incomplete or unclear."
"""

# ---------------- MODEL CALL ----------------
def get_model_response(question):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content.strip()

# ---------------- SQL EXECUTION ----------------
def is_valid_sql(sql_text):
    error_keywords = ["error:", "not found", "invalid", "unknown"]
    return not any(k in sql_text.lower() for k in error_keywords)

def read_sql_query(sql):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    conn.close()
    return rows, columns

# ---------------- UI ----------------
st.title("Text2SQL RAG Query Assistant")

# Use a multi-line text area for better visibility
question = st.text_area("Enter your question here:", height=100)

if st.button("Ask"):
    sql_query = get_model_response(question)

    # Show SQL only if it's NOT an error
    if sql_query.startswith("Error:"):
        st.error(sql_query)
        st.stop()
    else:
        st.subheader("Generated SQL Query:")
        st.code(sql_query)

    try:
        rows, columns = read_sql_query(sql_query)

        st.subheader("Query Result:")
        if rows:
            import pandas as pd
            df = pd.DataFrame(rows, columns=columns)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Query returned no rows.")

    except Exception as e:
        st.error(f"SQL Error: {e}")


