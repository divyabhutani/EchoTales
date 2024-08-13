from pygame import gfxdraw

BG_CLR = (40, 41, 35) 
CLR_R = (249, 36, 114) 
CLR_B = (103, 216, 239)
CLR_G = (166, 226, 43)
CLR_O = (253, 150, 34)
CLR_W = (248, 248, 239)
CLR_P = (172, 128, 255)
CLR_LG = (116, 112, 93)

class Shape:
    '''
    A class to define shapes and their attributes.
    '''
    def __init__(self, x, y, color, radius):
        self.position = (x, y)
        self.color = color
        self.radius = radius

    def distance_to(self, other_shape):
        return ((self.position[0]-other_shape.position[0])**2 + (self.position[1]-other_shape.position[1])**2)


    def draw_ring(self, surface, thickness):
        gfxdraw.aacircle(surface, self.position[0], self.position[1], self.radius+thickness//2, self.color)
        gfxdraw.filled_circle(surface, self.position[0], self.position[1], self.radius+thickness//2, self.color)
        gfxdraw.aacircle(surface, self.position[0], self.position[1], self.radius-thickness//2, BG_CLR)
        gfxdraw.filled_circle(surface, self.position[0], self.position[1], self.radius-thickness//2, BG_CLR)

    def draw_circle(self, surface):
        gfxdraw.aacircle(surface, self.position[0], self.position[1], self.radius, CLR_W)
        gfxdraw.filled_circle(surface, self.position[0], self.position[1], self.radius, CLR_W)
        gfxdraw.aacircle(surface, self.position[0], self.position[1], self.radius-2, self.color)
        gfxdraw.filled_circle(surface, self.position[0], self.position[1], self.radius-2, self.color)


    
