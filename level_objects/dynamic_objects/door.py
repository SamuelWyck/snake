import pygame
from level_objects.proto_objects.level_tile import LevelTile
from level_objects.proto_objects.receiver import Receiver



class Door(LevelTile, Receiver):
    def __init__(self, topleft, size, color, image, is_open):
        super().__init__(topleft, size)

        self.image = image
        self.color = color
        self.is_open = is_open
        self.open_rect = pygame.rect.Rect((-10, -10), (0, 0))
    


    def update(self, surface, delta_time):
        if not self.is_open:
            self.draw(surface)

    

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)



    def open(self):
        self.is_open = True

    

    def close(self):
        self.is_open = False


    
    def toggle(self):
        self.is_open = not self.is_open

    

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