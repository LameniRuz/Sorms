""" General classes used as a building blocks, helper classes"""

from global_variables import * 

class Block():
    """ Creates rectangle, with another rectangle as a border if needed,
        + additional capabilities to draw and move the rectangle
    """
    def __init__(self, x, y, side=BLOCK_SIZE, color=PINK, **kwargs):
        self.x = x
        self.y = y
        self.side = side
        self.color = color 
        # Block border
        self.border_color = (0,0,0) 
        self.border_thickness = 1

        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def move(self, x, y):
        """ Changes block coordinates"""
        self.x = x
        self.y = y

    def draw(self, surface):
        """Draws block on the screen in current x,y position"""
        rect = (self.x, self.y, self.side, self.side)
        pg.draw.rect(surface, self.color, rect)

        # add border
        rect = (self.x, self.y, self.side+self.border_thickness, 
                self.side+self.border_thickness)
        pg.draw.rect(surface, self.border_color, rect, 
                     width=self.border_thickness)


    def teleport(self, x, y, surface):
        """ Moves block on the surface to a given position. """
        self.move(x,y)
        self.draw(surface)
        
