class Size():
    
    """
    width - width of the shape
    height - height of the shape
    """
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def resize(self, width, height):
        self.width = width
        self.height = height