import pygame, math



class Bullet:
    def __init__(self, center_coords, target_coords, screen_dimensions, image, speed, color, stop_at_target=False):
        self.target_vector = pygame.math.Vector2(target_coords)
        self.vector = pygame.math.Vector2(center_coords)

        opposite_side = (self.target_vector.y - self.vector.y) * -1
        adjacent_side = self.target_vector.x - self.vector.x
        radian_angle = math.atan2(opposite_side, adjacent_side)
        angle = math.degrees(radian_angle)

        self.image = pygame.transform.rotozoom(image, angle, 1).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = center_coords

        self.speed = speed
        self.remove = False
        self.color = color

        if stop_at_target:
            line_slope = opposite_side / adjacent_side if adjacent_side != 0 else 0
            self.target_vector = self.calc_off_screen_target(line_slope, screen_dimensions)


    def calc_off_screen_target(self, slope, screen_dimensions):
        width_index = 0
        height_index = 1
        screen_width = screen_dimensions[width_index]
        screen_height = screen_dimensions[height_index]

        if slope == 0:
            x_change = self.target_vector.x - self.vector.x
            y_change = self.target_vector.y - self.vector.y
            if x_change == 0:
                end_y = 0 if y_change < 0 else screen_height
                return pygame.math.Vector2((self.target_vector.x, end_y))
            else:
                end_x = 0 if x_change < 0 else screen_width
                return pygame.math.Vector2((end_x, self.target_vector.y))
        
        end_x = screen_width if self.target_vector.x > self.vector.x else 0
        end_y = end_x * slope 
        if end_y < 0 or end_y > screen_height:
            end_y = screen_height if self.target_vector.y > self.vector.y else 0
            end_x = end_y / slope
        
        return pygame.math.Vector2((end_x, end_y))

    
    def update(self, surface, delta_time):
        if self.remove:
            return
        
        speed = delta_time * self.speed

        self.vector = self.vector.move_towards(self.target_vector, speed)
        self.rect.centerx = self.vector.x
        self.rect.centery = self.vector.y
        if self.vector == self.target_vector:
            self.remove = True

        self.draw(surface)
        

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


    def get_hitbox(self):
        return self.rect
    

    def get_mask(self):
        return self.mask
