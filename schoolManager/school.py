from datetime import date
import mysql.connector as mysql

db = mysql.connect(host="localhost", user="root", password="", database="escola")
command_handler = db.cursor(buffered=True)

today = date.today().strftime("%d-%m-%Y")


def create_subject(subject):
    subject = str(subject)


def delete_subject(subject):
    subject = str(subject)


def add_student(subject, student):
    subject = str(subject)


def delete_student(subject, student):
    subject = str(subject)


def add_teacher(subject, teacher):
    subject = str(subject)


def delete_teacher(subject, student):
    subject = str(subject)


def set_grades(student):
    is_student = check_student(str(student))
    if not is_student:
        print("This student does not exists, check for spelling errors!")
    else:
        student = str(student)
        print("You want to set which grade for this Student? (Seventh Grade = 7th Grade; Third Grade = 3rd Grade) ")
        grade = input(str(""))
        query_vals = (grade, student)
        command_handler.execute("UPDATE users SET grade = %s WHERE name = %s", query_vals)
        db.commit()
        print(f"The student {query_vals[1]} was set to the {query_vals[0]}!")


def get_grade(student):
    student = [student]
    command_handler.execute("SELECT grade FROM users WHERE privilege = 'Student' AND name = %s", student)
    stu_grade = command_handler.fetchall()
    grade = ''
    for grade in stu_grade:
        grade = str(grade).replace("'", "")
        grade = str(grade).replace(",", "")
        grade = str(grade).replace("(", "")
        grade = str(grade).replace(")", "")
    return grade


def mark_attendance(student):
    is_student = check_student(str(student))
    if not is_student:
        print("This student does not exists, check for spelling errors!")
    else:
        student = str(student)
        print("")
        print("Mark Student Register")
        print("")
        grade = get_grade(student)
        print("Status for " + student + ". P = Present, A = Absent, L = Late")
        status = input(str(""))
        query_vals = (student, today, status, grade)
        command_handler.execute("INSERT INTO attendance (name, date, status, grade) VALUES (%s,%s,%s,%s)", query_vals)
        db.commit()
        print("The student: "+ student + " was set today ("+ today +") to the status of: " + status)


def update_attendance(student):
    is_student = check_student(str(student))
    if not is_student:
        print("This student does not exists, check for spelling errors!")
    else:
        student = str(student)
        print("")
        print("Update Student Register")
        print("")
        print("New status for " + student + ". P = Present, A = Absent, L = Late")
        status = input(str(""))
        query_vals = (today, status, student)
        command_handler.execute("UPDATE attendance SET date = %s, status = %s WHERE name = %s", query_vals)
        db.commit()
        print("The student: " + student + " was updated today (" + today + ") to the status of: " + status)


def check_student(student):
    student = [student]
    command_handler.execute("SELECT * FROM users WHERE name = %s", student)
    if command_handler.rowcount <= 0:
        return False
    else:
        return True
