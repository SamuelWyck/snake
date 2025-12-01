import pygame
import random
from level_objects.proto_objects.level_tile import LevelTile
from utils.animation import Animation
from utils.color import Color



class Lava(LevelTile):
    def __init__(self, topleft, size, color, frame_data, image):
        super().__init__(topleft, size)

        self.color = color
        self.image = image.copy()
        image_color = color if color != Color.NO_COLOR else Color.WHITE
        self.image.fill(image_color, special_flags=pygame.BLEND_MIN)
        self.active_image = self.image

        frame_data = self.color_frames(frame_data, image_color)
        self.animation = Animation(frame_data)

        one_second = 60
        self.max_animation_cooldown = random.choice([one_second * 3, one_second * 5, one_second * 7, one_second * 10])
        self.animation_cooldown = random.randint(0, self.max_animation_cooldown)



    def color_frames(self, frame_data, image_color):
        new_frame_data = []
        for frame in frame_data:
            image, duration = frame
            colored_image = image.copy()
            colored_image.fill(image_color, special_flags=pygame.BLEND_MIN)
            new_frame_data.append((colored_image, duration))
        return new_frame_data
    


    def update(self, surface, delta_time):
        if self.animation_cooldown < self.max_animation_cooldown:
            self.animation_cooldown += delta_time
            self.active_image = self.image
        else:
            bubble_image = self.animation.get_frame(delta_time)
            self.active_image = bubble_image
            if self.animation.completed:
                self.animation_cooldown = 0
                self.active_image = self.image

        self.draw(surface)

    

    def draw(self, surface):
        surface.blit(self.active_image, self.rect.topleft)
    


    def get_hitbox(self):
        return self.rect
    


    def collide(self, rect):
        return False