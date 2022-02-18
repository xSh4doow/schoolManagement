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

def check_subject(subject):
    command_handler.execute("SELECT * FROM subjects WHERE name = (%s)", [subject])
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


def add_record():
    student = input(str("To which student do you want to add the record?\n"))
    tof = check_student(student)
    if tof:
        record = input(str("Which is the student's record? (8,5 = 8.5; 10 = 10.0)\n"))
        date = input(str("What was the date of the test? (YYYY-MM-DD)\n"))
        subject = input(str("Which subject was the test about?\n"))
        tofs = check_subject(subject)
        if tofs:
            name = input(str("What is the name of the test?\n"))
            query_vals = (name, student, record, date, subject)
            query = "INSERT INTO `records`(`test_name`, `student_name`, `student_record`, `test_date`, `subject`) VALUES (%s,%s,%s,%s,%s)"
            command_handler.execute(query,query_vals)
            db.commit()
            print(f"The record for {student} in the {subject} test was set to {record}!")
        else:
            print("This is not a valid subject!")
    else:
        print("This is not a valid student!")

def update_record():
    student = input(str("To which student do you want to update the record?\n"))
    tof = check_student(student)
    if tof:
        record = input(str("Which is the new student's record? (8,5 = 8.5; 10 = 10.0)\n"))
        subject = input(str("Which subject was the test about?\n"))
        tofs = check_subject(subject)
        if tofs:
            name = input(str("What is the name of the test?\n"))
            query = f'UPDATE `records` SET `student_record` = "{record}" WHERE `subject` = "{subject}" AND `student_name` = "{student}" AND `test_name` = "{name}"'
            command_handler.execute(query)
            db.commit()
            print(f"The record for {student} in the {subject} test was updated to {record}!")
        else:
            print("This is not a valid subject!")
    else:
        print("This is not a valid student!")


def view_subject_records():
    subject = input(str("Which subject do you wish to see the records?\n"))
    tofs = check_subject(subject)
    if tofs:
        query = f'SELECT `test_name`, `student_name`, `student_record` FROM `records` WHERE `subject` = "{subject}"'
        command_handler.execute(query)
        records = command_handler.fetchall()
        for record in records:
            record = str(records)
            record = record.replace('(', '')
            record = record.replace(')', '')
            record = record.replace("'", '')
        print(record)
    else:
        print("This is not a valid subject!")


def view_student_records():
    subject = input(str("Which subject do you wish to see the records?\n"))
    student = input(str("Which student do you wish to see the records?\n"))
    tofs = check_subject(subject)
    tof = check_student(student)
    if tofs and tof:
        query = f'SELECT `test_name`, `student_name`, `student_record` FROM `records` WHERE `subject` = "{subject}" AND `student_name` = "{student}"'
        command_handler.execute(query)
        records = command_handler.fetchall()
        for record in records:
            record = str(records)
            record = record.replace('(', '')
            record = record.replace(')', '')
            record = record.replace("'", '')
        print(record)
    else:
        print("This is not a valid subject or student, please try again!")

def view_avg_record():
    subject = input(str("Which subject do you wish to see the average record?\n"))
    tofs = check_subject(subject)
    if tofs:
        query = f'SELECT AVG(student_record) AS average FROM records WHERE `subject` = "{subject}"'
        command_handler.execute(query)
        avg = command_handler.fetchall()
        for i in avg:
            i = str(avg)
            i = i.replace('(', '')
            i = i.replace(')', '')
            i = i.replace("'", '')
            i = i.replace(",", '')
            i = i.replace("[", '')
            i = i.replace("]", '')
            print(f"The average record for this subject ({subject}) is "+str(i))
    else:
        print("This is not a valid subject!")

def view_avg_student_record():
    subject = input(str("Which subject do you wish to see the average record?\n"))
    student = input(str("Which student do you wish to see the average record?\n"))
    tofs = check_subject(subject)
    tof = check_student(student)
    if tofs and tof:
        query = f'SELECT AVG(student_record) AS average FROM records WHERE `subject` = "{subject}" AND `student_name` = "{student}"'
        command_handler.execute(query)
        avg = command_handler.fetchall()
        for i in avg:
            i = str(avg)
            i = i.replace('(', '')
            i = i.replace(')', '')
            i = i.replace("'", '')
            i = i.replace(",", '')
            i = i.replace("[", '')
            i = i.replace("]", '')
            print(f"The average record for {student} in this subject ({subject}) is "+str(i))
    else:
        print("This is not a valid subject or student, please try again!")


def view_student():
    student = input(str("Which student do you wish to see the profile?\n"))
    tof = check_student(student)
    if tof:
        command_handler.execute(
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'students' ORDER BY ORDINAL_POSITION")
        che = command_handler.fetchall()
        for column in che:
            che = str(che)
            che = che.replace('(', '')
            che = che.replace(')', '')
            che = che.replace("'", '')
        print("The informations will be presented in this format:")
        print(che)
        sleep(1)
        print("Displaying info:")
        query_info = "`id`,`name`, `grade`, `birthdate`, `father_name`, `mother_name`, `address`, `mother_telefone`, `father_telefone`"
        query = f'SELECT {query_info} FROM `students` WHERE `name` = "{student}"'
        command_handler.execute(query)
        infos = command_handler.fetchall()
        info = ""
        for info in infos:
            info = str(infos)
            info = info.replace('(', '')
            info = info.replace(')', '')
            info = info.replace("'", '')
            info = info.replace("datetime.date", '')
        print(info)
    else:
        print("This is not a valid student!")

def bulk_update_student():
    student = input(str("Which student do you wish to update the profile?\n"))
    tof = check_student(student)
    if tof:
        print("Updating Student's Information!\nThis is going to update ALL of the entries!\nDo you wish to continue? Y or N")
        print("(If you don't want to change a specific entry, when asked to what will be the change, just insert the information it already contains!)")
        resp = input(str(""))
        if resp == "Y":
            print("Starting Update")
            sleep(2)

            birthdate = input(str("What is the student's birthdate?(YYYY-MM-DD)\n"))
            father_name = input(str("What is the student's father's name?\n"))
            mother_name = input(str("What is the student's mother's name?\n"))
            address = input(str("What is the student's address?\n"))
            mother_telefone = input(str("What is the student's mother's telephone?\n"))
            father_telefone = input(str("What is the student's father's telephone?\n"))

            print(f"The following entries will be inserted into the students profile: {birthdate},{father_name},{mother_name},{address},{mother_telefone},{father_telefone}")

            query = f"UPDATE `students` SET `birthdate`='{birthdate}',`father_name`='{father_name}',`mother_name`='{mother_name}',`address`='{address}',`mother_telefone`='{mother_telefone}',`father_telefone`='{father_telefone}' WHERE `name` = '{student}'"
            command_handler.execute(query)
            print("Update complete!")
            db.commit()
        else:
            print("You will be redirected to the previous menu!")
            sleep(2)
    else:
        print("This is not a valid student!")

