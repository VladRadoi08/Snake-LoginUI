from tkinter import *
import sqlite3

conn = sqlite3.connect('users_data.db')
cursor = conn.cursor()


def create_sql_table():
    cursor.execute('CREATE TABLE IF NOT EXISTS users(userName TEXT, passWord TEXT, score INTEGER)')
    conn.commit()
    return conn


create_sql_table()


class User:
    def __init__(self, username, password, score):
        self.username = username
        self.password = password
        self.score = score


def register_user_ui(conn, cursor, score=0):
    reg_window = Toplevel(main_window)
    Label(reg_window, text="Enter your username.").pack()
    name_entry = Entry(reg_window)
    name_entry.pack()
    username = name_entry.get()
    Label(reg_window, text="Enter your password.").pack()
    password_entry = Entry(reg_window)
    password_entry.pack()
    pass_word = password_entry.get()
    Button(reg_window, text="Complete Registration.", command=create_user(username, pass_word, conn, cursor)).pack()


def login_user_ui():
    login_window = Toplevel(main_window)
    Label(login_window, text="Enter you username.").pack()
    name_entry = Entry(login_window)
    name_entry.pack()
    login_username = name_entry.get()
    Label(login_window, text="Enter your password.").pack()
    pass_entry = Entry(login_window)
    pass_entry.pack()
    login_password = pass_entry.get()
    Button(login_window, text="Login")
    return login_username, login_password


def create_user(username, pass_word, conn, cursor, score=0):
    new_user = User(username, pass_word, score)
    query = "INSERT INTO users VALUES (?,?,?)"
    data = (str(new_user.username), str(new_user.password), new_user.score)
    cursor.execute(query, data)
    conn.commit()
    return new_user


def compare_user(user, conn, cursor, login_username, login_password):
    table_info = cursor.execute("SELECT * FROM users")
    print(table_info)


main_window = Tk()

Label(main_window, text="Existing Users.", bg="gray").pack()
login_button = Button(main_window, text="Login", command=login_user_ui).pack()
Label(main_window, text="New Users.", bg="gray").pack()
register_button = Button(main_window, text="Click register to make a new user.",
                         command=register_user_ui(conn, cursor)).pack()

main_window.mainloop()
