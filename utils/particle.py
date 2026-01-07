import pygame
from utils.color import Color



class Particle:
    def __init__(self, center, radius, target_radius, delta_radius, color=Color.WHITE):
        self.center = center
        self.radius = radius
        self.delta_radius = delta_radius
        self.target_radius = target_radius
        
        self.remove = False
        self.color = color 


    
    def update(self, surface, delta_time):
        if self.remove:
            return self.remove
        
        self.radius += (self.delta_radius * delta_time)

        min_hit = self.radius <= self.target_radius and self.delta_radius < 0
        max_hit = self.radius >= self.target_radius and self.delta_radius > 0
        
        if max_hit or min_hit:
            self.remove = True
            return self.remove
        
        pygame.draw.circle(surface, self.color, self.center, self.radius)

        return self.remove