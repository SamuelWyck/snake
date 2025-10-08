import pygame, random
from level_objects.proto_objects.level_tile import LevelTile



class Wall(LevelTile):
    def __init__(self, topleft, size, color, color_key):
        super().__init__(topleft, size)

        self.image = pygame.Surface(size)
        self.image.fill(color_key)
        self.color = color
    


    def update(self, surface, delta_time):
        self.draw(surface)



    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    


    def collide(self, collider):
        if collider.color == self.color:
            return False
        return True