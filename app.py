from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key'

def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS notices
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  date TEXT, 
                  title TEXT, 
                  description TEXT,
                  publisher TEXT)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  roll_no TEXT UNIQUE, 
                  name TEXT,
                  password TEXT,
                  attendance TEXT,
                  percentage TEXT,
                  student_class TEXT,
                  section TEXT,
                  fee_status TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS teachers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  email TEXT UNIQUE, 
                  name TEXT,
                  password TEXT,
                  salary INTEGER,
                  subject TEXT,
                  syllabus_status TEXT,
                  schedule TEXT)''')
                  
    c.execute('''CREATE TABLE IF NOT EXISTS salary_requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  teacher_name TEXT, 
                  email TEXT, 
                  salary INTEGER, 
                  status TEXT, 
                  date TEXT)''')
    
    # Students data initialization
    c.execute("SELECT COUNT(*) FROM students")
    if c.fetchone()[0] == 0:
        first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan"]
        last_names = ["Gupta", "Sharma", "Verma", "Singh", "Kumar", "Patel", "Mehta", "Reddy", "Iyer", "Nair"]
        school_classes = ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"]
        sections = ["A", "B", "C"]
        fee_dues_options = ["Paid", "Paid", "Paid", "₹4,500 Due", "₹8,000 Due", "Paid"]

        for i in range(1, 101):
            roll_no = str(i)
            f_name = first_names[(i - 1) % len(first_names)]
            l_name = last_names[((i - 1) * 3) % len(last_names)]
            student_name = f"{f_name} {l_name}"
            password = f"pass{roll_no}"
            random.seed(i)
            attendance = f"{random.randint(75, 98)}%"
            percentage = f"{round(random.uniform(60.0, 96.5), 2)}%"
            student_class = school_classes[(i - 1) % len(school_classes)]
            section = sections[(i - 1) % len(sections)]
            fee_status = fee_dues_options[(i * 3) % len(fee_dues_options)]

            c.execute("""INSERT INTO students (roll_no, name, password, attendance, percentage, student_class, section, fee_status) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
                      (roll_no, student_name, password, attendance, percentage, student_class, section, fee_status))

    # 50 Indian Teachers data initialization with Unique Names, Emails & Passwords
    c.execute("SELECT COUNT(*) FROM teachers")
    if c.fetchone()[0] == 0:
        t_first_names = [
            "Rajesh", "Amit", "Suresh", "Ramesh", "Manoj", "Alok", "Sunil", "Anil", "Deepak", "Pankaj",
            "Sanjay", "Vinod", "Ashok", "Vijay", "Ajay", "Mukesh", "Rakesh", "Dinesh", "Naveen", "Praveen",
            "Pooja", "Sunita", "Anita", "Rekha", "Meena", "Kavita", "Geeta", "Seema", "Neelam", "Suman",
            "Priyanka", "Deepika", "Neha", "Divya", "Swati", "Pallavi", "Monika", "Ritu", "Jyoti", "Asha",
            "Kiran", "Madhu", "Archana", "Vandana", "Sarita", "Pushpa", "Shweta", "Preeti", "Mamta", "Radha"
        ]
        t_last_names = [
            "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Mishra", "Pandey", "Tiwari", "Dubey", "Joshi",
            "Saxena", "Thakur", "Yadav", "Jain", "Bansal", "Agrawal", "Chauhan", "Sinha", "Mehta", "Rawat"
        ]
        subjects = ["Mathematics", "Physics", "Chemistry", "Biology", "English", "Computer Science", "Social Studies", "Hindi"]
        syllabus_options = ["75% Completed (25% Remaining)", "60% Completed (40% Remaining)", "90% Completed (10% Remaining)", "50% Completed (50% Remaining)"]
        schedules = [
            "Mon-Fri: 09:00 AM - 10:00 AM (Class 10-A), 11:00 AM - 12:00 PM (Class 9-B)",
            "Mon, Wed, Fri: 10:00 AM - 11:30 AM (Class 12-Science)",
            "Tue, Thu, Sat: 08:30 AM - 10:00 AM (Class 8-C), 12:00 PM - 01:00 PM (Class 11)"
        ]
        
        for i in range(1, 51):
            f_name = t_first_names[i - 1].lower()
            l_name = t_last_names[(i * 2) % len(t_last_names)].lower()
            
            # Real name formatting
            name = f"Mr. {t_first_names[i - 1]} {t_last_names[(i * 2) % len(t_last_names)]}" if i <= 35 else f"Mrs. {t_first_names[i - 1]} {t_last_names[(i * 2) % len(t_last_names)]}"
            
            # Unique email based on name: e.g., rajesh.sharma@apex.com
            email = f"{f_name}.{l_name}@apex.com"
            
            # Unique secure password based on name and ID: e.g., rajesh@2026#1
            password = f"{f_name}@{2026}#{i}"
            
            salary = random.randint(35000, 85000)
            subject = subjects[i % len(subjects)]
            syllabus = syllabus_options[i % len(syllabus_options)]
            schedule = schedules[i % len(schedules)]
            
            c.execute("INSERT OR IGNORE INTO teachers (email, name, password, salary, subject, syllabus_status, schedule) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                      (email, name, password, salary, subject, syllabus, schedule))
        
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notices ORDER BY id DESC LIMIT 3")
    notices = c.fetchall()
    conn.close()
    return render_template('index.html', notices=notices)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/notices')
def all_notices():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notices ORDER BY id DESC")
    notices = c.fetchall()
    conn.close()
    return render_template('notices.html', notices=notices)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'apex123':
            session['is_admin'] = True
            return redirect(url_for('admin'))
        else:
            error = "Invalid Admin Username or Password!"
    return render_template('admin_login.html', error=error)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = datetime.now().strftime("%d %b") 
        c.execute("INSERT INTO notices (date, title, description, publisher) VALUES (?, ?, ?, ?)", (date, title, description, "System Admin"))
        conn.commit()
    
    c.execute("SELECT id, teacher_name, email, salary, date FROM salary_requests WHERE status = 'Pending'")
    salary_requests = c.fetchall()
    
    conn.close()
    return render_template('admin.html', salary_requests=salary_requests)

@app.route('/admin/approve-salary/<int:req_id>')
def approve_salary(req_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("UPDATE salary_requests SET status = 'Approved' WHERE id = ?", (req_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/admin/fees-dues')
def admin_fees_dues():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    c.execute("SELECT roll_no, name, student_class, section, fee_status FROM students WHERE fee_status != 'Paid'")
    dues_students = c.fetchall()
    conn.close()
    
    return render_template('admin_fees.html', students=dues_students)

@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    error = None
    if request.method == 'POST':
        roll_no = request.form['roll_no'].strip()
        password = request.form['password'].strip()
        
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE roll_no = ? AND password = ?", (roll_no, password))
        student = c.fetchone()
        conn.close()
        
        if student:
            session['student_name'] = student[2]
            session['roll_no'] = student[1]
            session['attendance'] = student[4]
            session['percentage'] = student[5]
            session['student_class'] = student[6]
            session['section'] = student[7]
            session['fee_status'] = student[8]
            return redirect(url_for('student_dashboard'))
        else:
            error = f"Invalid Roll Number or Password!"
    return render_template('student_login.html', error=error)

@app.route('/student-dashboard')
def student_dashboard():
    if 'student_name' not in session:
        return redirect(url_for('student_login'))
    
    return render_template('student_dashboard.html', 
                           name=session['student_name'], 
                           roll=session['roll_no'],
                           attendance=session['attendance'],
                           percentage=session['percentage'],
                           student_class=session['student_class'],
                           section=session['section'],
                           fee_status=session['fee_status'])

@app.route('/teacher-login', methods=['GET', 'POST'])
def teacher_login():
    error = None
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("SELECT * FROM teachers WHERE email = ? AND password = ?", (email, password))
        teacher = c.fetchone()
        conn.close()
        if teacher:
            session['teacher_name'] = teacher[2]
            session['teacher_email'] = teacher[1]
            session['teacher_salary'] = teacher[4]
            session['teacher_subject'] = teacher[5]
            session['teacher_syllabus'] = teacher[6]
            session['teacher_schedule'] = teacher[7]
            return redirect(url_for('teacher_dashboard'))
        else:
            error = "Invalid Email or Password!"
    return render_template('teacher_login.html', error=error)

@app.route('/teacher-dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if 'teacher_name' not in session:
        return redirect(url_for('teacher_login'))
        
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        action_type = request.form.get('action_type')
        
        if action_type == 'notice':
            title = request.form['title']
            description = request.form['description']
            date = datetime.now().strftime("%d %b")
            publisher = session['teacher_name']
            c.execute("INSERT INTO notices (date, title, description, publisher) VALUES (?, ?, ?, ?)", (date, title, description, publisher))
            conn.commit()
        elif action_type == 'salary_request':
            date = datetime.now().strftime("%d %b %Y")
            c.execute("INSERT INTO salary_requests (teacher_name, email, salary, status, date) VALUES (?, ?, ?, 'Pending', ?)",
                      (session['teacher_name'], session['teacher_email'], session['teacher_salary'], date))
            conn.commit()
            
        conn.close()
        return redirect(url_for('teacher_dashboard'))
        
    c.execute("SELECT * FROM notices ORDER BY id DESC")
    notices = c.fetchall()
    
    c.execute("SELECT status FROM salary_requests WHERE email = ? AND status = 'Pending'", (session['teacher_email'],))
    pending_req = c.fetchone()
    
    conn.close()
    return render_template('teacher_dashboard.html', 
                           name=session['teacher_name'], 
                           email=session['teacher_email'],
                           salary=session['teacher_salary'],
                           subject=session.get('teacher_subject'),
                           syllabus=session.get('teacher_syllabus'),
                           schedule=session.get('teacher_schedule'),
                           notices=notices, 
                           has_pending_request=pending_req is not None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)