import pygame, math



class Bullet:
    def __init__(self, center_coords, target_coords, screen_dimensions, image, speed, stop_at_target=False):
        self.target_vector = pygame.math.Vector2(target_coords)
        self.vector = pygame.math.Vector2(center_coords)

        opposite_side = self.target_vector.x - self.vector.x
        adjacent_side = self.target_vector.y - self.vector.y
        radian_angle = math.atan2(opposite_side, adjacent_side)
        angle = math.degrees(radian_angle)

        self.image = pygame.transform.rotozoom(image, angle, 1)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = center_coords

        self.speed = speed
        self.line_slope = opposite_side / adjacent_side
        self.remove = False
        self.stop_at_target = stop_at_target

    
    def update(self, surface, delta_time):
        if self.remove:
            return
        
        speed = delta_time * self.speed
        if self.stop_at_target:
            self.vector = self.vector.move_towards(self.target_vector, speed)
            self.rect.centerx = self.vector.x
            self.rect.centery = self.vector.y
            if self.vector == self.target_vector:
                self.remove = True
        else:
            x_change = speed
            y_change = speed * self.line_slope
            self.vector.x += x_change
            self.vector.y += y_change
            self.rect.centerx = self.vector.x
            self.rect.centery = self.vector.y

        self.draw(surface)
        

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
