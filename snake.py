import turtle
import time
import random
from gui import User


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
snakeHead.goto(0,0)
snakeHead.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("grey")
food.penup()
food.goto(0,100)

segments = []

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.penup()
pen.ht()
pen.goto(0,260)
pen.write("Score: 0  High Score: 0", align="center", font = ("Courier", 25, "normal"))

def move():
    if snakeHead.direction == "up":
        y = snakeHead.ycor()
        snakeHead.sety(y+20)
    if snakeHead.direction == "down":
        y = snakeHead.ycor()
        snakeHead.sety(y-20)
    if snakeHead.direction == "right":
        x = snakeHead.xcor()
        snakeHead.setx(x+20)
    if snakeHead.direction == "left":
        x = snakeHead.xcor()
        snakeHead.setx(x-20)

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
    if snakeHead.xcor()>290 or snakeHead.xcor()<-290 or snakeHead.ycor()>290 or snakeHead.ycor()<-290:
        time.sleep(1)
        snakeHead.goto(0,0)
        snakeHead.direction = "stop"
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        point_score = 0
        pen.clear()    
        pen.write("Score: {}  High Score: {}".format(point_score, high_score), align = "center", font =("Courier", 25, "normal"))
        
    if snakeHead.distance(food) < 20:
        x = random.randint(-290,290)
        y = random.randint(-290, 290)
        food.goto(x,y)
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
        pen.write("Score: {}  High Score: {}".format(point_score, high_score), align = "center", font =("Courier", 25, "normal"))
        
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y= segments[i-1].ycor()
        segments[i].goto(x,y)
    if len(segments) > 0:
        x = snakeHead.xcor()
        y = snakeHead.ycor()
        segments[0].goto(x,y)
        
    move()

    for segment in segments:
        if segment.distance(snakeHead) < 20:
            time.sleep(1)
            snakeHead.goto(0,0)
            snakeHead.direction = "stop"
            for segment in segments:
                segment.goto(1000,1000)
            segments.clear()
            point_score = 0
            pen.clear()    
            pen.write("Score: {}  High Score: {}".format(point_score, high_score), align = "center", font =("Courier", 25, "normal"))
            
            
    
    time.sleep(delay)


window.mainloop()
