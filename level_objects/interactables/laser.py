import pygame
from utils.color import Color



class Laser:
    def __init__(self, start_coords, angle, color, long_length, short_length):
        self.max_length = long_length
        self.short_length = short_length
        self.start_coords = start_coords

        self.angle = angle
        self.angle_up = 0
        self.angle_down = 180
        self.angle_right = 90
        self.angle_left = 270
        
        self.rect = pygame.rect.Rect((0, 0), (0, 0))
        self.reset_laser()

        self.color = color
        self.render_color = color if color != Color.NO_COLOR else Color.GRAY
        self.remove = False
    

    def set_laser_start(self, coords):
        if self.angle == self.angle_up:
            self.rect.midbottom = coords
        elif self.angle == self.angle_down:
            self.rect.midtop = coords
        elif self.angle == self.angle_right:
            self.rect.midleft = coords
        else:
            self.rect.midright = coords
        self.start_coords = coords


    def reset_laser(self): 
        if self.angle == self.angle_up:
            self.rect.height = self.max_length
            self.rect.width = self.short_length
            self.rect.midbottom = self.start_coords
        elif self.angle == self.angle_right:
            self.rect.height = self.short_length
            self.rect.width = self.max_length
            self.rect.midleft = self.start_coords
        elif self.angle == self.angle_down:
            self.rect.height = self.max_length
            self.rect.width = self.short_length
            self.rect.midtop = self.start_coords
        else:
            self.rect.height = self.short_length
            self.rect.width = self.max_length
            self.rect.midright = self.start_coords
    

    def shorten_laser(self, rect):
        if self.angle == self.angle_up:
            new_height = self.rect.bottom - rect.bottom
            self.rect.height = new_height
            self.rect.midbottom = self.start_coords
        elif self.angle == self.angle_right:
            new_width = rect.x - self.rect.x
            self.rect.width = new_width
            self.rect.midleft = self.start_coords
        elif self.angle == self.angle_down:
            new_height = rect.y - self.rect.y
            self.rect.height = new_height
            self.rect.midtop = self.start_coords
        else:
            new_width = self.rect.right - rect.right
            self.rect.width = new_width
            self.rect.midright = self.start_coords

    
    def get_end_coords(self):
        if self.angle == self.angle_up:
            return self.rect.midtop
        if self.angle == self.angle_down:
            return self.rect.midbottom
        if self.angle == self.angle_left:
            return self.rect.midleft
        return self.rect.midright
    

    def update(self, surface, delta_time):
        self.draw(surface)
        self.reset_laser()

    
    def draw(self, surface):
        pygame.draw.rect(surface, self.render_color, self.rect)