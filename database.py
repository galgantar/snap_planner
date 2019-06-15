import mail
import sys

def establish_connection():
    import os
    import psycopg2

    DATABASE_URL = os.environ['DATABASE_URL']

    return psycopg2.connect(DATABASE_URL, sslmode='require')

def hash_password(password):
    import bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(15)).decode()

def confirm_data(name="a", surname="a", email="g@g.g", number="0"):
    import re

    if not re.search(r"^[a-zA-Z\ čšž]+$", name) and len(name) <= 100:
        return "Name must only contain characters"
    elif not re.search(r"^[a-zA-Z\ čšž]+$", surname) and len(surname) <= 100:
        return "Surname must only contain characters"
    elif not re.search(r"[^@]+@[^@]+\.[^@]+", email) and len(email) <= 30:
        return "Invalid email address"
    elif not re.search(r"^[0-9\ \+]+$", number) and len(number) <= 20:
        return "Invalid phone number"

    return False #No mistakes found

def user_is_new(email):
    connection = establish_connection()
    cursor = connection.cursor()

    cursor.execute("""SELECT ID FROM Users WHERE Email = %s;""", (email,))
    connection.commit()

    if cursor.fetchone() == None:
        return False #No mistakes found
    else:
        return "Account already exists"

def insert_new_user(name, surname, password, email, number):
    connection = establish_connection()
    cursor = connection.cursor()

    cursor.execute("""\
                    INSERT INTO Users (Name, Surname, Password, Email, Tel, Role)
                    VALUES(%s, %s, %s, %s, %s, %s);
                    """, (name, surname, hash_password(password), email, number, "user"))

    cursor.close()
    connection.commit()
    connection.close()

def check_login(email, password):
    import bcrypt
    connection = establish_connection()
    cursor = connection.cursor()
    cursor.execute("""SELECT Password FROM Users WHERE Email = %s ;""", (email,)) #(x,) forces python to make a touple

    response = cursor.fetchone()
    if not response:
        return False

    hash = response[0]
    connection.close()

    if password and bcrypt.checkpw(password.encode(), hash.encode()):
        return True
    else:
        return False

def list_database():
    connection = establish_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Users ORDER BY Surname")
    response = cursor.fetchall()

    cursor.close()
    connection.commit()
    connection.close()

    return response

def get_user_data(email):
    connection = establish_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Users WHERE Email = %s;", (email,))

    data = cursor.fetchone()
    cursor.close()
    connection.close()
    return data

def change_data(datatype_index, user_email, data):
    """Datatype index code: 0 = password, 1 = name, 2 = surname, 3 = telephone"""
    connection = establish_connection()
    cursor = connection.cursor()

    if datatype_index == 0:
        cursor.execute("UPDATE Users SET Password = %s WHERE Email = %s", (hash_password(data), user_email))
    elif datatype_index == 1:
        cursor.execute("UPDATE Users SET Name = %s WHERE Email = %s", (data, user_email))
    elif datatype_index == 2:
        cursor.execute("UPDATE Users SET Surname = %s WHERE Email = %s", (data, user_email))
    elif datatype_index == 3:
        cursor.execute("UPDATE Users SET Tel = %s WHERE Email = %s", (data, user_email))

    cursor.close()
    connection.commit()
    connection.close()

def generate_confirmation_code():
    """generates random code and returns it with the time of creation"""
    from string import ascii_letters, digits
    from random import choice
    import datetime

    code = "".join([choice(ascii_letters+digits) for i in range(50)])
    confirmation_link = "http://galgantar.tk/confirmation/" + code

    time = datetime.datetime.utcnow().strftime('%Y-%m-%d')

    return (code, time)

def email_conformation(email):
    """Sends email confirmation code"""
    code = generate_confirmation_code()

    confirmation_link = "http://galgantar.tk/confirmation/" + code[0]
    time = code[1]

    connection = establish_connection()
    cursor = connection.cursor()
    cursor.execute("""\
                INSERT INTO Confirmations (Email, Code, Creation, Type)
                VALUES (%s, %s, %s, 'email')
                """, (email, code, time))
    cursor.close()

    mail.send_conformation(email, confirmation_link)

    connection.commit()
    connection.close()

def confirm_email(code):
    """Validates email confirmation code"""
    connection = establish_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT Email FROM Confirmations WHERE Code = %s", (code,))

    try:
        email = cursor.fetchone()[0]
        cursor.execute("UPDATE Users SET Confirmed = TRUE WHERE Email = %s", (email,))
        cursor.execute("DELETE FROM Confirmations WHERE Email = %s AND Type = 'email'", (email,))
        cursor.close()
        connection.commit()
        connection.close()
        return True

    except TypeError:
        pass

    cursor.close()
    connection.commit()
    connection.close()
    return False

def reset_password(email):
    timed_code = generate_confirmation_code()
    confirmation_link = "http://galgantar.tk/password/" + timed_code[0] +"?email="+ email.replace("@", "<at>")
    time = timed_code[1]

    connection = establish_connection()
    cursor = connection.cursor()

    cursor.execute("""\
                    INSERT INTO Confirmations (Email, Code, Creation, Type)
                    VALUES (%s, %s, %s, 'password')
                    """, (email, timed_code[0], time))
    cursor.close()
    connection.commit()
    connection.close()

    mail.send_password_reset(email, confirmation_link)

def check_password_code(email, code):
    """Validates password reset code"""
    connection = establish_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT Email FROM Confirmations WHERE Email = %s AND Code = %s", (email, code))

    try:
        email = cursor.fetchone()[0]
        cursor.execute("DELETE FROM Confirmations WHERE Email = %s AND Type = 'password'", (email,))
        cursor.close()
        connection.commit()
        connection.close()
        return True

    except TypeError:
        pass

    cursor.close()
    connection.commit()
    connection.close()
    return False

def manual_execute(code=None):
    if not code:
        code = open("query.sql", "r").read()
    connection = establish_connection()
    cursor = connection.cursor()

    cursor.execute(code)



    if cursor.statusmessage.split()[0] == "SELECT":
        response = cursor.fetchall()
        print(response)

    cursor.close()
    connection.commit()
    connection.close()


if __name__ == "__main__":
    if sys.argv[0]:
        if sys.argv[0] == "-u":
            print(list_database())

        elif sys.argv[0] == "-c":
            manual_execute("SELECT * FROM Confirmations")

    else:
        manual_execute()
