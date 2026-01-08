import pygame
from utils.color import Color



class Explosion:
    def __init__(self, center, width, radius, delta_width, delta_radius, color=Color.WHITE):
        self.center = center

        self.width = width
        self.delta_width = delta_width
        self.max_width_change_count = 1
        self.width_change_count = self.max_width_change_count

        self.radius = radius
        self.delta_radius = delta_radius
        self.finished = False
        self.color = color


    def update(self, surface, delta_time):
        if self.finished:
            return
        
        self.width_change_count -= delta_time
        if self.width_change_count <= 0:
            self.width -= self.delta_width
            self.width_change_count = self.max_width_change_count
        
        if self.width <= 0:
            self.finished = True
            return
        
        self.radius += (self.delta_radius * delta_time)
        pygame.draw.circle(surface, self.color, self.center, self.radius, self.width)