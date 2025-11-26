import pygame
from level_objects.proto_objects.level_tile import LevelTile
from level_objects.proto_objects.receiver import Receiver
from utils.animation import Animation



class Door(LevelTile, Receiver):
    def __init__(self, topleft, size, color, frame_data, is_open, is_vertical):
        super().__init__(topleft, size)

        if is_vertical:
            frame_data = self.rotate_frames(frame_data)

        self.animation = Animation(frame_data)
        self.image = None
        self.color = color
        self.is_open = is_open
        self.starting_status = is_open
        self.open_rect = pygame.rect.Rect((-10, -10), (0, 0))

    

    def rotate_frames(self, frame_data):
        frame_list = []
        for frame in frame_data:
            image, duration = frame
            image = pygame.transform.rotate(image, 90).convert_alpha()
            frame_list.append((image, duration))
        return frame_list
    


    def update(self, surface, delta_time):
        if not self.is_open:
            self.image = self.animation.get_frame(delta_time)
            self.draw(surface)

    

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)



    def open(self):
        self.is_open = True

    

    def close(self):
        self.is_open = False


    
    def toggle(self):
        self.is_open = not self.is_open
    


    def reset(self):
        self.is_open = self.starting_status

    

    def collide(self, rect):
        if self.is_open:
            return False
        if self.rect.colliderect(rect):
            return True
        return False
    


    def get_hitbox(self):
        if self.is_open:
            return self.open_rect
        return self.rect