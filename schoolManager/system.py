import mysql.connector as mysql
import yagmail
from schoolManager.school import mark_attendance, update_attendance, check_student, add_student, \
    add_teacher, delete_student, delete_teacher, update_student, delete_subject, create_subject

#Using PHPmyadmin, change 'db' to where your db is located! (remember to also change in school.py!)
db = mysql.connect(host="localhost", user="root", password="", database="escola")
command_handler = db.cursor(buffered=True)


def main():
    while 1:
        print("Welcome to the School Management System!")
        print("")
        print("1. Login as Student")
        print("2. Login as Teacher")
        print("3. Login as Helper")
        print("4. Login as Admin")
        print("5. Recover Password")
        print("6. Exit")
        print("")

        user_opt = input(str("Option : "))
        if user_opt == "1":
            print("Logging in as Student!")
        elif user_opt == "2":
            print("Logging in as Teacher!")
            auth("Teacher")
        elif user_opt == "3":
            print("Logging in as Helper!")
            auth("Helper")
        elif user_opt == "4":
            print("Logging in as Admin")
            auth_adm()
        elif user_opt == "5":
            recover_pass_state()
        elif user_opt == "6":
            break
        else:
            print("No valid option was selected, please try again!")


def initialization():
    attendance = """CREATE TABLE IF NOT EXISTS `attendance` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `name` varchar(30) NOT NULL,
 `date` varchar(30) NOT NULL,
 `status` varchar(30) NOT NULL,
 `grade` varchar(30) NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8"""

    students = """CREATE TABLE IF NOT EXISTS `students` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `name` varchar(30) NOT NULL,
 `grade` int(3) NOT NULL,
 `birthdate` date NOT NULL,
 `father_name` varchar(30) NOT NULL,
 `mother_name` varchar(30) NOT NULL,
 `address` text NOT NULL,
 `mother_telefone` text NOT NULL,
 `father_telefone` text NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `name` (`name`),
 CONSTRAINT `fk_name_student` FOREIGN KEY (`name`) REFERENCES `users` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8"""

    subjects = """CREATE TABLE IF NOT EXISTS `subjects` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `name` varchar(30) NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8"""

    teachers = """CREATE TABLE IF NOT EXISTS `teachers` (
 `id` int(30) NOT NULL AUTO_INCREMENT,
 `name` varchar(30) NOT NULL,
 `subject` varchar(30) NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `name` (`name`),
 KEY `fk_sub_teach` (`subject`),
 CONSTRAINT `fk_name_teacher` FOREIGN KEY (`name`) REFERENCES `users` (`name`),
 CONSTRAINT `fk_sub_teach` FOREIGN KEY (`subject`) REFERENCES `subjects` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8"""

    users = """	CREATE TABLE IF NOT EXISTS `users` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `name` varchar(30) NOT NULL,
 `password` varchar(30) NOT NULL,
 `privilege` varchar(50) NOT NULL,
 `email` varchar(50) NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `name` (`name`),
 UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
    """

    command_handler.execute(attendance)
    command_handler.execute(students)
    command_handler.execute(subjects)
    command_handler.execute(teachers)
    command_handler.execute(users)

    main()


def auth(type):
    privilege = str(type).title()
    print("")
    print(privilege + "'s Login")
    print("")
    email = input(str("Email : "))
    password = input(str("Password : "))
    print("")
    query_vals = (email, password, privilege)
    command_handler.execute("SELECT * FROM users WHERE email = %s AND password = %s AND privilege = %s", query_vals)
    if command_handler.rowcount <= 0:
        print("Credentials not valid")
    else:
        print("Welcome " + privilege + "!")
        if privilege == "Student":
            """student_session()"""
        elif privilege == "Helper":
            helper_session()
        # elif privilege == "Teacher":


def auth_adm():
    print("")
    print("Admin Login")
    print("")
    user = input(str("User : "))
    password = input(str("Password : "))

    if user == "admin":
        if password == "password":
            admin_session()
        else:
            print("Incorrect Password!")
    else:
        print("Credentials not valid!")


def createuser(type):
    privilege = str(type).title()
    print("")
    print("Register New " + privilege)
    email = input(str(privilege + " email: "))
    name = input(str(privilege + " name: "))
    password = input(str(privilege + " password: "))
    query_vals = (name, email, password, privilege)
    command_handler.execute("INSERT INTO users (name, email, password, privilege) VALUES (%s,%s,%s,%s)", query_vals)
    db.commit()
    print(name + " has been registered as a new " + privilege + "!")
    if privilege == 'Student':
        add_student(name.title())
    elif privilege == 'Teacher':
        add_teacher(name.title())


def eraseuser(type):
    privilege = str(type).title()
    print("")
    print("Delete Existing " + privilege)
    if privilege == 'Student':
        command_handler.execute("SELECT name, email FROM users WHERE privilege = %s", (privilege,))
        user = command_handler.fetchall()
        for users in command_handler:
            user = str(user)
            user = user.replace('(', '')
            user = user.replace(')', '')
            user = user.replace("'", '')
            user = user.replace(',','\n')
        print(user)

        name = input(str(privilege + " name: (Exactly like above!)\n"))
        email = input(str(privilege + " email: "))
        query_vals = (email, privilege)
        if privilege == 'Student':
            delete_student(name.title())
        elif privilege == 'Teacher':
            delete_teacher(name.title())
        command_handler.execute("DELETE FROM users WHERE email = %s AND privilege = %s", query_vals)
        db.commit()
        if command_handler.rowcount < 1:
            print('User not found')
        else:
            print("The user linked to this email:" + email + ". has been deleted from the system!")

    else:
        email = input(str(privilege + " email: "))
        query_vals = (email, privilege)
        command_handler.execute("DELETE FROM users WHERE email = %s AND privilege = %s", query_vals)
        db.commit()
        if command_handler.rowcount < 1:
            print('User not found')
        else:
            print("The user linked to this email:"+ email + ". has been deleted from the system!")


def admin_session():
    while 1:
        blank()
        print("Admin Menu")
        blank()
        print("1. Register New Student")
        print("2. Register New Teacher")
        print("3. Register New Helper")
        print("4. Register New Subject")
        print("5. Delete Existing Student")
        print("6. Delete Existing Teacher")
        print("7. Delete Existing Helper")
        print("8. Delete Existing Subject")
        print("9. Logout")

        user_opt = input(str("Option: "))
        blank()
        if user_opt == "1":
            createuser("Student")
        elif user_opt == "2":
            createuser("Teacher")
        elif user_opt == "3":
            createuser("Helper")
        elif user_opt == "4":
            sub = input(str("Which subject do you want to create?\n"))
            create_subject(sub)
        elif user_opt == "5":
            eraseuser("Student")
        elif user_opt == "6":
            eraseuser("Teacher")
        elif user_opt == "7":
            eraseuser("Helper")
        elif user_opt == "8":
            sub = input(str("Which subject do you want to delete?\n"))
            delete_subject(sub)
        elif user_opt == "9":
            break


def helper_session():
    while 1:
        print("")
        print("Helper Menu")
        print("")
        print("1. Mark Student's Register")
        print("2. Update Student's Register")
        print("3. View Student's Register")
        print("4. View All Student's Registers")
        print("5. Update Student's Info")
        print("6. Logout")
        blank()
        user_opt = input(str("Option: "))
        blank()
        if user_opt == "1":
            print("Which student you want to mark?")
            view_all_students()
            student = input(str(""))
            mark_attendance(student)
        elif user_opt == "2":
            print("Which student you update the register?")
            view_all_students()
            student = input(str(""))
            update_attendance(student)
        elif user_opt == "3":
            print("Which student you want to check the registers?")
            view_all_students()
            student = input(str(""))
            is_student = check_student(student)
            if not is_student:
                print("This is a valid student, please try again!")
            else:
                print(f"Viewing {student} registers!")
                t_student = [student]
                command_handler.execute("SELECT name, date, status, grade FROM attendance WHERE name = %s", t_student)
                records = command_handler.fetchall()
                for record in records:
                    print(record)
        elif user_opt == "4":
            print("Viewing all student registers!")
            command_handler.execute("SELECT name, date, status, grade FROM attendance")
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_opt == "5":
            print("Which student you want to update? ")
            view_all_students()
            student = input(str(""))
            update_student(student)
        elif user_opt == "6":
            break
        else:
            print("No valid option was selected!")


def recover_pass_state():
    print("")
    print("Password Recovery System")
    print("")

    privilege = input(str("Are you a Student or a Teacher? (S for Student or T for Teacher) "))
    if privilege == "T":
        email = input(str("Hello Teacher, please input your email: "))
        email_check(email, "Teacher")
    elif privilege == "S":
        email = input(str("Hello Student, please input your email: "))
        email_check(email, "Student")
    else:
        print("You didn't input a valid option, please try again")
        recover_pass_state()


def get_pass(email, privilege):
    print("Getting Password")
    email = str(email)
    privilege = str(privilege).title()
    vals = (email, privilege)
    str_pass = ""
    command_handler.execute("SELECT password FROM users WHERE email = %s AND privilege = %s", vals)
    for password in command_handler:
        str_pass = str(password)
        str_pass = str_pass.replace('(', '')
        str_pass = str_pass.replace(')', '')
        str_pass = str_pass.replace("'", '')
        str_pass = str_pass.replace(',', '')
    return str_pass


def email_check(email, privilege):
    email = [email]
    privilege = str(privilege)
    command_handler.execute("SELECT * FROM users WHERE email = %s", email)
    if command_handler.rowcount <= 0:
        print("Wrong email, please try again!")
        recover_pass_state()
    else:
        print("You'll be receiving an email shortly!")
        email = str(email)
        recover_pass(email, privilege)


def recover_pass(email, privilege):
    receiver = str(email)
    str_rec = str(receiver)
    str_rec = str_rec.replace('[', '')
    str_rec = str_rec.replace(']', '')
    str_rec = str_rec.replace("'", '')

    privilege = str(privilege).title()
    password = get_pass(str_rec, privilege)
    body = """<p>&nbsp; &nbsp; &nbsp; &nbsp;<img src="https://i.imgur.com/gNGuk0h.png" alt="" /></p>
            <p>You requested a Password Recovery.</p>
            <p>Your password is:""" + password + """ .</p>
            <p></p>
            <p></p>
            <p>=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-</p>
            <p></p>
            <p></p>
            <p><strong>If you didn't request, please ignore this e-mail.</strong><strong></strong></p>
            <p><strong>Sent by School Management System, created using Python 3.9 by Pedro Rocha</strong><strong></strong></p>"""
    yag = yagmail.SMTP("testeescolapython@gmail.com", "!1escola1")
    yag.send(
        to=str_rec,
        subject="Password Recovery",
        contents=body
    )
    print("Email Sent!")


def view_all_students():
    students = ""
    command_handler.execute("SELECT name, grade FROM students WHERE privilege = 'Student'")
    for user in command_handler:
        students = str(user)
        students = students.replace('(', '')
        students = students.replace(')', '')
        students = students.replace("'", '')
    print(str(students))


def blank():
    print("")


initialization()
