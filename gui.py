from tkinter import *
from tkinter import messagebox
import sqlite3
import time
import turtle
import random


class User:
    def __init__(self,username,password,score):
        self.username=username
        self.password=password
        self.score=score
    def update_score(self,high_score):
        self.score = high_score
        data = self.username, self.score
        query = 'UPDATE users SET score = (?) WHERE userName = (?)'
        c.execute(query, data)
        insert_data = c.fetchall()




def main():
    global c
    global conn
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    global query
    global data
    query = None
    data = None

    def create_table():
        c.execute('CREATE TABLE IF NOT EXISTS users(userName TEXT, passWord TEXT, score INTEGER)')
        conn.commit()

    def compare_users():
        pass_match = False
        global log_name_entry, log_pass_entry
        global log_name,log_pass
        log_name = str(log_name_entry.get())
        log_pass = str(log_pass_entry.get())
        current_user= User(log_name,log_pass,score=0)
        data = current_user.username
        query = 'SELECT * FROM users WHERE userName = ?'
        c.execute(query,(data,))
        db_data = c.fetchall()
        db_output = db_data.pop()
        db_output = db_output[:0] + db_output[1:]
        db_list = list(db_output)
        db_list.remove(0)
        for password in db_list:
            if str(current_user.password) == password:
                pass_match = True
                print(pass_match)
                correct_pass = messagebox.showinfo("Correct Password!", "You've entered the right password!")
                import snake
            else:
                pass_match = False
                print(pass_match)
                wrong_pass = messagebox.showerror("Wrong Password!", "You've entered the wrong password!")
        print(current_user.score)
        current_user.update_score(2000)
        print(current_user.score)
        return current_user

    def login_ui():
        global main_window
        login_window = Toplevel(main_window)
        Label(login_window, text = "Please enter your username:").pack()
        global log_name_entry
        log_name_entry = Entry(login_window)
        log_name_entry.pack()
        Label(login_window, text = "Please enter your password:").pack()
        global log_pass_entry
        log_pass_entry = Entry(login_window)
        log_pass_entry.pack()
        Button(login_window, text="Click to login!",command = compare_users).pack()

    def create_user():
        global name_entry
        reg_name = name_entry.get()
        name_entry.delete(0, END)
        global pass_entry
        reg_pass=pass_entry.get()
        new_user = User(reg_name,reg_pass,score=0)
        data = new_user.username, new_user.password, new_user.score
        query = 'INSERT INTO users VALUES(?,?,?)'
        c.execute(query, data)
        conn.commit()
        Label(reg_window, fg="green",text="Registration Complete!").pack()
        return new_user


    def register_ui():
        global main_window
        global reg_window
        global name_entry
        global pass_entry
        reg_window = Toplevel(main_window)
        Label(reg_window, text="Enter your desired username:").pack()
        name_entry = Entry(reg_window)
        name_entry.pack()
        Label(reg_window,text="Enter your desired password:").pack()
        pass_entry = Entry(reg_window)
        pass_entry.pack()
        Label(reg_window,text="").pack()
        Button(reg_window, text="Click to finish registration!",command= create_user).pack()


    global main_window
    main_window = Tk()
    main_window.geometry("300x200")
    Label(main_window,text = "Welcome to PySnake").pack()
    Label(main_window, text="").pack()
    Label(main_window, text="If you already have an account, log in, otherwise register!")
    Button(main_window, text="Login.",command=login_ui).pack()
    Label(main_window,text="").pack()
    Button(main_window,text="Register",command=register_ui).pack()



    create_table()
    main_window.mainloop()
    return main_window


main()
