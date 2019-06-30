import turtle

class Robot_Manual_Control_Wheel():
    
    def __init__(self, canvas, screen_width, screen_height):
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
        #t.setpos(screen_width / 4, screen_height / 4)

        t.pendown()
        t.circle(screen_dim_to_use / 2.15)
        t.penup()