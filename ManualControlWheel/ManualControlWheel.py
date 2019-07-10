import turtle


class ManualControlWheel:
    
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
        
        # Detect mouse clicked/dragged
        canvas.bind("<Button-1>", ManualControlWheel.mouse_clicked)
        canvas.bind("<B1-Motion>", ManualControlWheel.mouse_dragged)
        
    # Mouse clicked event
    @staticmethod
    def mouse_clicked(event):
        print("Clicked at", event.x, event.y)
        
    # Mouse dragged event
    @staticmethod
    def mouse_dragged(event):
        print("Dragged to", event.x, event.y)
