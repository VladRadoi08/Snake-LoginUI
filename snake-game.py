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


def snake_func(current_user):
    delay = 0.1

    point_score = 0
    high_score = 0

    window = turtle.Screen()
    window.title("Snake Game!")
    window.bgcolor("green")
    window.setup(width=600, height=600)
    window.tracer(0)

    snakeHead = turtle.Turtle()
    snakeHead.speed(0)
    snakeHead.shape("square")
    snakeHead.color("yellow")
    snakeHead.penup()
    snakeHead.goto(0, 0)
    snakeHead.direction = "stop"

    food = turtle.Turtle()
    food.speed(0)
    food.shape("square")
    food.color("grey")
    food.penup()
    food.goto(0, 100)

    segments = []

    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.penup()
    pen.ht()
    pen.goto(0, 260)
    pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 25, "normal"))

    def move():
        if snakeHead.direction == "up":
            y = snakeHead.ycor()
            snakeHead.sety(y + 20)
        if snakeHead.direction == "down":
            y = snakeHead.ycor()
            snakeHead.sety(y - 20)
        if snakeHead.direction == "right":
            x = snakeHead.xcor()
            snakeHead.setx(x + 20)
        if snakeHead.direction == "left":
            x = snakeHead.xcor()
            snakeHead.setx(x - 20)

    def go_up():
        if snakeHead.direction != "down":
            snakeHead.direction = "up"

    def go_down():
        if snakeHead.direction != "up":
            snakeHead.direction = "down"

    def go_left():
        if snakeHead.direction != "right":
            snakeHead.direction = "left"

    def go_right():
        if snakeHead.direction != "left":
            snakeHead.direction = "right"

    window.listen()
    window.onkeypress(go_up, "Up")
    window.onkeypress(go_down, "Down")
    window.onkeypress(go_left, "Left")
    window.onkeypress(go_right, "Right")

    while True:
        window.update()
        if snakeHead.xcor() > 290 or snakeHead.xcor() < -290 or snakeHead.ycor() > 290 or snakeHead.ycor() < -290:
            time.sleep(1)
            snakeHead.goto(0, 0)
            snakeHead.direction = "stop"
            current_user.update_score(high_score)
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            point_score = 0
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(point_score, high_score), align="center",
                      font=("Courier", 25, "normal"))

        if snakeHead.distance(food) < 20:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            food.goto(x, y)
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("orange")
            new_segment.penup()
            segments.append(new_segment)
            point_score += 10
            if point_score > high_score:
                high_score = point_score
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(point_score, high_score), align="center",
                      font=("Courier", 25, "normal"))

        for i in range(len(segments) - 1, 0, -1):
            x = segments[i - 1].xcor()
            y = segments[i - 1].ycor()
            segments[i].goto(x, y)
        if len(segments) > 0:
            x = snakeHead.xcor()
            y = snakeHead.ycor()
            segments[0].goto(x, y)

        move()

        for segment in segments:
            if segment.distance(snakeHead) < 20:
                time.sleep(1)
                snakeHead.goto(0, 0)
                snakeHead.direction = "stop"
                current_user.update_score(high_score)
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()
                point_score = 0
                pen.clear()
                pen.write("Score: {}  High Score: {}".format(point_score, high_score), align="center",
                          font=("Courier", 25, "normal"))

        time.sleep(delay)

    window.mainloop()

def main_func():
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

    def show_leaderboard():
        global main_window
        query = 'SELECT userName, score FROM users ORDER BY score DESC'
        c.execute(query)
        leaderboard = c.fetchall()
        pd.DataFrame(leaderboard)
        for widget in main_window.winfo_children():
            widget.pack_forget()
        Label(main_window, text = leaderboard).pack()

    def compare_users():
        pass_match = False
        global log_name_entry, log_pass_entry
        global log_name,log_pass
        log_name = str(log_name_entry.get())
        log_pass = str(log_pass_entry.get())
        current_user = User(log_name,log_pass,0)
        data = current_user.username
        query = 'SELECT * FROM users WHERE userName = ?'
        c.execute(query,(data,))
        db_data = c.fetchall()
        db_output = db_data.pop()
        db_output = db_output[:0] + db_output[1:]
        db_list = list(db_output)
        db_list.remove(0)
        for password in db_list:                        #loops through what is found in the SQL database
            if str(current_user.password) == password:      #checks if the password from sql is the same as what I've entered
                pass_match = True
                print(pass_match)
                correct_pass = messagebox.showinfo("Correct Password!", "You've entered the right password!")       #if its correct show the little message
                snake_func(current_user)       #run the Turtle stuff
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

    def main_menu():
        global main_window
        main_window = Tk()
        main_window.geometry("300x200")
        Label(main_window,text = "Welcome to PySnake").pack()
        Label(main_window, text="").pack()
        Label(main_window, text="If you already have an account, log in, otherwise register!")
        Button(main_window, text="Login.",command=login_ui).pack()
        Label(main_window,text="").pack()
        Button(main_window,text="Register",command=register_ui).pack()
        Label(main_window, text="").pack()
        Button(main_window, text = "Show leaderboard",command=show_leaderboard).pack()
        main_window.mainloop()


    create_table()
    main_menu()
    return

if __name__ == '__main__':
    print(__name__)
    main_func()

