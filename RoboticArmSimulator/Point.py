class Point():
    
    """
    xPos - Position of x coordinate
    yPos - Position of y coorinate
    """
    
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        
    def move(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos