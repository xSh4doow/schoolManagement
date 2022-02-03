import mysql.connector as mysql
import yagmail

db = mysql.connect(host="localhost", user="root", password="", database="escola")
command_handler = db.cursor(buffered=True)


def main():
    while 1:
        print("Welcome to the School Management System!")
        print("")
        print("1. Login as Student")
        print("2. Login as Teacher")
        print("3. Login as Admin")
        print("4. Recover Password")
        print("5. Exit")
        print("")

        user_opt = input(str("Option : "))
        if user_opt == "1":
            print("Logging in as Student!")
        elif user_opt == "2":
            print("Logging in as Teacher!")
            auth("Teacher")
        elif user_opt == "3":
            print("Logging in as Admin")
            auth_adm()
        elif user_opt == "4":
            recover_pass_state()
        elif user_opt == "5":
            break
        else:
            print("No valid option was selected, please try again!")


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


def eraseuser(type):
    privilege = str(type).title()
    print("")
    print("Delete Existing " + privilege)
    email = input(str(privilege + " email: "))
    query_vals = (email, privilege)
    command_handler.execute("DELETE FROM users WHERE email = %s AND privilege = %s", query_vals)
    db.commit()
    if command_handler.rowcount < 1:
        print('User not found')
    else:
        print(email + " has been deleted!")


def admin_session():
    while 1:
        print("")
        print("Admin Menu")
        print("")
        print("1. Register New Student")
        print("2. Register New Teacher")
        print("3. Delete Existing Student")
        print("4. Delete Existing Teacher")
        print("5. Logout")

        user_opt = input(str("Option: "))
        if user_opt == "1":
            createuser("Student")
        elif user_opt == "2":
            createuser("Teacher")
        elif user_opt == "3":
            eraseuser("Student")
        elif user_opt == "4":
            eraseuser("Teacher")
        elif user_opt == "5":
            break


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
    body = "You have requested a password recovery.\n Your password is: " + password + ".\n If you didn't requested the recovery, please ignore this email."
    yag = yagmail.SMTP("testeescolapython@gmail.com", "!1escola1")
    yag.send(
        to=str_rec,
        subject="Password Recovery",
        contents=body
    )
    print("Email Sent!")


main()