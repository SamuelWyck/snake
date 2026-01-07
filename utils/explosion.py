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

        




# class Explosion:
#     def __init__(self, bounding_rect, num_effects, delta_radius):
    #     self.particles = []
    #     self.finished = False

    #     for _ in range(num_effects):
    #         particle = self.create_particle(bounding_rect, delta_radius)
    #         self.particles.append(particle)
    

    # def create_particle(self, bounding_rect, delta_radius):
    #     max_radius = bounding_rect.width
    #     radius = max_radius / 4
    
    #     center_x = random.randint(bounding_rect.x, bounding_rect.x + bounding_rect.width)
    #     center_y = random.randint(bounding_rect.y, bounding_rect.y + bounding_rect.height)
    #     center = (center_x, center_y)

    #     return Particle(center, radius, delta_radius=delta_radius, target_radius=max_radius)


    # def update(self, surface, delta_time):
    #     if self.finished:
    #         return
        
    #     for particle in self.particles:
    #         remove = particle.update(surface, delta_time)
    #         if remove:
    #             self.finished = True
        
