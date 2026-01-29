import pygame
from level_objects.proto_objects.level_tile import LevelTile
from utils.color import Color



class SpikeBall(LevelTile):
    def __init__(self, target_points, tile_size, spike_size, velocity, color, foreground_img, background_img, circular_path):
        super().__init__((0, 0), (spike_size, spike_size))

        # Get the center coords for each target_point
        self.target_points = []
        x_index = 0
        y_index = 1
        tile_width_index = 0
        half_tile_size = tile_size[tile_width_index] // 2
        for point in target_points:
            x_pos = point[x_index]
            y_pos = point[y_index]
            x_pos += half_tile_size
            y_pos += half_tile_size
            self.target_points.append((x_pos, y_pos))
        self.rect.center = self.target_points[0]
        
        self.color = color
        self.image = self.build_image(foreground_img, background_img)
        self.circular_path = circular_path
        self.velocity = velocity
        self.target_index = 0
        self.target_index_change = 1
        self.vector = pygame.math.Vector2(self.rect.center)
    


    def build_image(self, foreground_img, background_img):
        color = self.color if self.color != Color.NO_COLOR else Color.BLACK
        foreground_img = foreground_img.copy()
        background_img = background_img.copy()
        foreground_img.fill(color, special_flags=pygame.BLEND_MIN)
        background_img.blit(foreground_img, (0, 0))
        return background_img
    


    def reset(self):
        self.rect.center = self.target_points[0]
        self.target_index = 0
        self.target_index_change = 1
        self.vector = pygame.math.Vector2(self.rect.center)
    


    def update(self, surface, delta_time):
        velocity = self.velocity * delta_time
        target_point = self.target_points[self.target_index]
        
        old_x = self.vector.x
        old_y = self.vector.y
        self.vector = self.vector.move_towards(target_point, velocity)
        if old_x == self.vector.x and old_y == self.vector.y:
            self.update_target_index()
        self.rect.centerx = self.vector.x
        self.rect.centery = self.vector.y

        self.draw(surface)


    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    


    def collide(self, rect):
        return self.rect.colliderect(rect)

    

    def update_target_index(self):
        new_index = self.target_index + self.target_index_change

        if self.circular_path:
            if new_index >= len(self.target_points):
                self.target_index = 0
            else:
                self.target_index += self.target_index_change
            return


        if new_index < 0:
            self.target_index_change = 1
        elif new_index >= len(self.target_points):
            self.target_index_change = -1

        self.target_index += self.target_index_change


    
    def reverse_direction(self):
        self.target_index_change = self.target_index_change * -1
        self.update_target_index()