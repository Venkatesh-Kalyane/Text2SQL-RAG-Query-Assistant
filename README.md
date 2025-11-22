# Text2SQL RAG Query Assistant

A Streamlit-based **Text-to-SQL Retrieval-Augmented Generation (RAG) Query assistant** that allows users to query a SQLite database using natural language. The system generates SQL queries automatically, executes them on a local SQLite database, and displays results in a user-friendly interface.

---

## Folder Structure

```
images/
├─ sample_output.png
├─ Negative test cases/
│  ├─ Asking for data which is not there.png
│  └─ Giving column which is not present.png
.env
app.py
requirements.txt
sqlite.py
text2sql.db
```

* `images/` – Screenshots demonstrating sample outputs and negative test cases.
* `.env` – Environment file containing your Groq API key.
* `app.py` – Main Streamlit app for interacting with the Text2SQL assistant.
* `requirements.txt` – Python dependencies.
* `sqlite.py` – Script to set up the SQLite database and insert sample data.
* `text2sql.db` – SQLite database file.

---

## Features

* Query the database using natural language.
* Auto-generate SQL queries based on your input.
* Enforces table relationships:

  * `STUDENT.CLASS` ↔ `TEACHER.SUBJECT`
  * `STUDENT.ROLL_NO` ↔ `ADDRESS.ROLL_NO`
* Handles incomplete or unclear questions safely.
* Displays query results in a clean, tabular format.
* Prevents SQL duplicates using `DISTINCT` when needed.

---

## Setup & Installation

1. **Clone the repository** (if using GitHub):

```bash
git clone <repository-url>
cd <repository-folder>
```

2. **Set up Groq API key** in `.env`:

```
GROQ_API_KEY=<YOUR_GROQ_API_KEY>
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Initialize the database**:

```bash
python sqlite.py
```

* This will create the database `text2sql.db` with `STUDENT`, `ADDRESS`, and `TEACHER` tables.
* Inserts sample data automatically **only if tables are empty**.

5. **Run the Streamlit app**:

```bash
streamlit run app.py
```

6. Open the displayed URL (usually `http://localhost:8501`) in your browser.

---

## Usage

* Enter your natural language query in the input box.
* Click **Ask** to generate the SQL query and view results.
* Example queries:

  * "Show all student names in Data Science class"
  * "Return name, subject, and address of students enrolled in Data Engineering and give salary of teacher teaching it"

---

## Notes

* The assistant is **context-aware** and understands relationships between tables.
* If a question is unclear, incomplete, or references non-existent columns/tables, it will **prompt an error instead of guessing**.
* Screenshots of sample outputs and negative test cases are available in the `images/` folder.

---
