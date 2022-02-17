from datetime import date
import mysql.connector as mysql
from time import sleep

db = mysql.connect(host="localhost", user="root", password="", database="escola")
command_handler = db.cursor(buffered=True)

today = date.today().strftime("%d-%m-%Y")


def create_subject(sub):
    command_handler.execute("INSERT INTO `subjects`(`name`) VALUES (%s)", [sub])
    print(f"Subject {sub.title()} has been created!")
    db.commit()


def delete_subject(name):
    command_handler.execute("DELETE FROM `subjects` WHERE name = (%s)", [name])
    print(f"Subject {name.title()} has been deleted!")
    db.commit()


def add_student(student):
    print("Into which grade do you want to set " + student + "? (7th grade = 7, 3rd grade = 3)")
    grade = input()
    student = str(student)
    query_vals = (student, grade)
    command_handler.execute("INSERT INTO students (name, grade) VALUES (%s, %s)", query_vals)
    db.commit()
    print("Student added to the Students DB")


def delete_student(student):
    command_handler.execute("DELETE FROM students WHERE name = %s", [student])
    print("Student deleted from the Students DB")
    db.commit()


def add_teacher(teacher):
    print("Into which subject do you want to set " + teacher + "?")
    subject = input()
    teacher = str(teacher)
    query_vals = (teacher, subject)
    command_handler.execute("INSERT INTO teachers (name, subject) VALUES (%s, %s)", query_vals)
    db.commit()
    print("Teacher added to the Teachers DB")


def delete_teacher(teacher):
    command_handler.execute("DELETE FROM teachers WHERE name = %s", [teacher])
    print("Teacher deleted from the Teachers DB")
    db.commit()


def get_grade(student):
    student = [student]
    command_handler.execute("SELECT grade FROM students WHERE name = %s", student)
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
        print("The student: " + student + " was set today (" + today + ") to the status of: " + status)


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
    command_handler.execute("SELECT * FROM students WHERE name = %s", student)
    if command_handler.rowcount <= 0:
        return False
    else:
        return True



def update_student(student):
    student = str(student)
    print("Select which attribute you want to change! (ID and NAME CANNOT be changed!)")
    command_handler.execute(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'students' ORDER BY ORDINAL_POSITION")
    che = command_handler.fetchall()
    for column in che:
        che = str(che)
        che = che.replace('(', '')
        che = che.replace(')', '')
        che = che.replace("'", '')
        print(che)
        selection = input(str())
        print("Updating " + student.title() + " " + selection.title() + "...")
        info = input(str("To what you want to update? "))
        query = f'UPDATE `students` SET `{selection}` = "{info}" WHERE `name` = "{student}"'
        command_handler.execute(query)
        db.commit()
        print(f"{selection.title()} changed to {info} for {student}!")
        sleep(5)