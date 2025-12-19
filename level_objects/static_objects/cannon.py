import pygame
import math
from level_objects.proto_objects.level_tile import LevelTile
from level_objects.interactables.bullet import Bullet
from utils.animation import Animation
from framework.play_area import PlayArea



class Cannon(LevelTile):
    def __init__(self, topleft, size, image, frame_data, smoke_data, bullet_image, bullet_color, position_angle, bullet_list):
        super().__init__(topleft, size)

        self.image = pygame.transform.rotozoom(image, position_angle, 1).convert_alpha()
        self.img_rect = self.image.get_rect()
        self.img_rect.center = self.rect.center
        self.bullet_image = bullet_image

        self.shoot_animation = Animation(frame_data)
        self.play_shoot_animation = False
        self.position_angle = position_angle
        self.smoke_animation = Animation(smoke_data)
        self.smoke_animation_rect = self.get_smoke_animation_rect()
        self.play_smoke_animation = False

        self.screen_dimensions = PlayArea.size
        self.max_fire_delay = 2 * 60
        self.fire_delay = self.max_fire_delay
        self.bullet_speed = 2
        self.bullet_list = bullet_list
        self.bullet_color = bullet_color
        self.bullet_target_coords = self.get_bullet_target_coords(position_angle)


    def get_smoke_animation_rect(self):
        angle_down = 0
        angle_left = -90
        angle_right = 90
        angle_up = 180

        smoke_animation_rect = pygame.rect.Rect((0, 0), (self.rect.width, self.rect.height))
        smoke_animation_rect.center = self.rect.center
        
        half_rect_width = self.rect.width // 2
        if self.position_angle == angle_down:
            smoke_animation_rect.centery += half_rect_width
        elif self.position_angle == angle_up:
            smoke_animation_rect.centery -= half_rect_width
        elif self.position_angle == angle_left:
            smoke_animation_rect.centerx -= half_rect_width
        elif self.position_angle == angle_right:
            smoke_animation_rect.centerx += half_rect_width
        
        return smoke_animation_rect


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
            self.play_shoot_animation = True
            self.play_smoke_animation = True
            self.shoot_bullet()
        
        self.draw(surface, delta_time)
    

    def draw(self, surface, delta_time):
        image = self.image
        if self.play_shoot_animation:
            image = self.shoot_animation.get_frame(delta_time, self.position_angle)
            if self.shoot_animation.completed:
                self.play_shoot_animation = False

        surface.blit(image, self.img_rect.topleft)
        if self.play_smoke_animation:
            smoke_image = self.smoke_animation.get_frame(delta_time)
            if self.smoke_animation.completed:
                self.play_smoke_animation = False
            else:
                surface.blit(smoke_image, self.smoke_animation_rect.topleft)
    

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
