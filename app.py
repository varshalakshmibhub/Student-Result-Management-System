
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ---------------- #

def init_db():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Students Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT UNIQUE,
            name TEXT,
            department TEXT,
            semester TEXT
        )
    ''')

    # Results Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT UNIQUE,
            subject1 INTEGER,
            subject2 INTEGER,
            subject3 INTEGER,
            total INTEGER,
            percentage REAL,
            grade TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ---------------- #

@app.route('/')
def home():
    return render_template('index.html')

# ---------------- ADD STUDENT ---------------- #

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        usn = request.form['usn']
        name = request.form['name']
        department = request.form['department']
        semester = request.form['semester']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM students WHERE usn=?",
            (usn,)
        )

        if cur.fetchone():
            conn.close()
            return """
            <script>
            alert('Student Already Exists!');
            window.location='/add_student';
            </script>
            """

        cur.execute('''
            INSERT INTO students(usn,name,department,semester)
            VALUES(?,?,?,?)
        ''', (usn, name, department, semester))

        conn.commit()
        conn.close()

        return """
        <script>
        alert('Student Added Successfully!');
        window.location='/';
        </script>
        """

    return render_template('add_student.html')

# ---------------- ADD MARKS ---------------- #

@app.route('/add_marks', methods=['GET', 'POST'])
def add_marks():

    if request.method == 'POST':

        usn = request.form['usn']

        subject1 = int(request.form['subject1'])
        subject2 = int(request.form['subject2'])
        subject3 = int(request.form['subject3'])

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM results WHERE usn=?",
            (usn,)
        )

        if cur.fetchone():
            conn.close()
            return """
            <script>
            alert('Marks Already Added For This Student!');
            window.location='/add_marks';
            </script>
            """

        total = subject1 + subject2 + subject3
        percentage = total / 3

        if percentage >= 90:
            grade = 'A+'
        elif percentage >= 75:
            grade = 'A'
        elif percentage >= 60:
            grade = 'B'
        elif percentage >= 40:
            grade = 'C'
        else:
            grade = 'Fail'

        cur.execute('''
            INSERT INTO results
            (usn, subject1, subject2, subject3,
             total, percentage, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            usn,
            subject1,
            subject2,
            subject3,
            total,
            percentage,
            grade
        ))

        conn.commit()
        conn.close()

        return """
        <script>
        alert('Marks Added Successfully!');
        window.location='/view_results';
        </script>
        """

    return render_template('add_marks.html')

# ---------------- VIEW RESULTS ---------------- #

@app.route('/view_results')
def view_results():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
        SELECT results.id,
               students.usn,
               students.name,
               students.department,
               students.semester,
               results.subject1,
               results.subject2,
               results.subject3,
               results.total,
               results.percentage,
               results.grade

        FROM students
        JOIN results
        ON students.usn = results.usn
    ''')

    data = cur.fetchall()

    conn.close()

    return render_template('view_results.html', data=data)

# ---------------- DELETE RESULT ---------------- #

@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM results WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return """
    <script>
    alert('Record Deleted Successfully!');
    window.location='/view_results';
    </script>
    """

# ---------------- SEARCH RESULT ---------------- #

@app.route('/search', methods=['POST'])
def search():

    usn = request.form['usn']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
        SELECT students.usn,
               students.name,
               students.department,
               students.semester,
               results.subject1,
               results.subject2,
               results.subject3,
               results.total,
               results.percentage,
               results.grade

        FROM students
        JOIN results
        ON students.usn = results.usn

        WHERE students.usn = ?
    ''', (usn,))

    data = cur.fetchone()

    conn.close()

    return render_template('search_result.html', data=data)

# ---------------- RUN APP ---------------- #

if __name__ == '__main__':
    app.run(debug=True)