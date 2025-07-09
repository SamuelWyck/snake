import pygame
from static_level_objects.level_tile import LevelTile



class Wall(LevelTile):
    def __init__(self, topleft, size, border_radius=0, color=(255, 255, 255), image=None):
        super().__init__(topleft, size)
        
        self.border_radius = border_radius
        self.color = color

        self.image = image
        self.mask = None
        if image: 
            self.mask = pygame.mask.from_surface(self.image)
            self.image_rect = self.image.get_rect()
            self.image_rect.center = self.rect.center
    


    def update(self, surface, delta_time):
        self.draw(surface)



    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.image_rect.topleft)
        else:
            pygame.draw.rect(surface, self.color, self.rect, border_radius=self.border_radius)
    


    def get_hitbox(self):
        return self.rect, self.mask