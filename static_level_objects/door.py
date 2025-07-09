import pygame
from static_level_objects.level_tile import LevelTile



class Door(LevelTile):
    def __init__(self, topleft, size, border_radius=0, color=(0, 0, 255), image=None):
        super.__init__(topleft, size)

        self.border_radius = border_radius
        self.color = color
        self.image = image
        self.mask = None

        if self.image:
            self.mask = pygame.mask.from_surface(self.image)
            self.image_rect = self.image.get_rect()
            self.image_rect.center = self.rect.center

        self.is_open = False
    


    def update(self, surface, delta_time):
        if not self.is_open:
            self.draw(surface)

    

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.image_rect.topleft)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=self.border_radius)

    

    def open(self):
        self.is_open = True

    

    def close(self):
        self.is_open = False


    
    def toggle(self):
        self.is_open = not self.is_open


    
    def get_hitbox(self):
        return self.rect, self.mask