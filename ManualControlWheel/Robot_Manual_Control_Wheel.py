import turtle

class Robot_Manual_Control_Wheel():
    
    def __init__(self, canvas, title):
        t = turtle.RawTurtle(canvas)
        t.hideturtle()
        t.speed(0)
        t.pencolor("#000000")
        
        screen_dim_to_use = min(int(canvas['width']), int(canvas['height']))
        
        t.penup()
        t.sety(-screen_dim_to_use / 3.5)
        
        t.pendown()
        t.circle(screen_dim_to_use / 3.5)
        t.penup()
        
        t.sety(-screen_dim_to_use / 2.15)

        t.pendown()
        t.circle(screen_dim_to_use / 2.15)
        t.penup()