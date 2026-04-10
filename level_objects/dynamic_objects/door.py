import pygame
from level_objects.proto_objects.level_tile import LevelTile
from level_objects.proto_objects.receiver import Receiver
from utils.animation import Animation
from asset_loaders.audio_loader import Audio



class Door(LevelTile, Receiver):
    def __init__(self, topleft, size, color, frame_data, source_image, is_open, is_vertical):
        super().__init__(topleft, size)

        if is_vertical:
            frame_data = self.rotate_frames(frame_data)
            source_image = pygame.transform.rotate(source_image, 90)

        self.source_image = source_image
        self.animation = Animation(frame_data)
        self.image = None
        self.color = color
        self.is_open = is_open
        self.starting_status = is_open
        self.open_rect = pygame.rect.Rect((-10, -10), (0, 0))

        # sound variables
        self.close_sound = Audio.get_sound_effect("door_close", "door")
        self.open_sound = Audio.get_sound_effect("door_open", "door")

    

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
        if not self.is_open:
            surface.blit(self.image, self.rect.topleft)

        surface.blit(self.source_image, self.rect.topleft)



    def open(self):
        self.is_open = True
        self.open_sound.hard_play()

    

    def close(self):
        self.is_open = False
        self.close_sound.soft_play()


    
    def toggle(self):
        self.is_open = not self.is_open
        if self.is_open:
            self.open_sound.hard_play()
        else:
            self.close_sound.soft_play()
    


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