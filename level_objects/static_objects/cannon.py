import pygame
import math
from level_objects.proto_objects.level_tile import LevelTile
from utils.bullet import Bullet
from framework.play_area import PlayArea



class Cannon(LevelTile):
    def __init__(self, topleft, size, image, bullet_image, bullet_color, position_angle, bullet_list):
        super().__init__(topleft, size)

        self.image = pygame.transform.rotate(image, position_angle).convert_alpha()
        self.img_rect = self.image.get_rect()
        self.img_rect.center = self.rect.center
        self.bullet_image = bullet_image

        self.screen_dimensions = PlayArea.size
        self.max_fire_delay = 2 * 60
        self.fire_delay = self.max_fire_delay
        self.bullet_speed = 2
        self.bullet_list = bullet_list
        self.bullet_color = bullet_color
        self.bullet_target_coords = self.get_bullet_target_coords(position_angle)


    def get_bullet_target_coords(self, angle):
        radian_angle = math.radians(angle)
        hypotenuse = self.rect.width

        x_length = math.sin(radian_angle) * hypotenuse
        y_length = math.cos(radian_angle) * hypotenuse

        return (self.rect.centerx + x_length, self.rect.centery + y_length)


    def update(self, surface, delta_time):
        self.fire_delay -= delta_time
        if self.fire_delay <= 0:
            self.fire_delay = self.max_fire_delay
            self.shoot_bullet()
        
        self.draw(surface)
    

    def draw(self, surface):
        surface.blit(self.image, self.img_rect.topleft)
    

    def shoot_bullet(self):
        bullet = Bullet(
            self,
            center_coords=self.rect.center,
            target_coords=self.bullet_target_coords,
            screen_dimensions=self.screen_dimensions,
            image=self.bullet_image,
            speed=self.bullet_speed,
            color=self.bullet_color,
            stop_at_target=True
        )
        self.bullet_list.append(bullet)
            
    
    def collide(self, rect):
        return self.rect.colliderect(rect)
