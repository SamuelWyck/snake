import pygame



class LevelTile:
    def __init__(self, topleft, size):
        self.rect = pygame.rect.Rect(topleft, size)
    


    def update(self, surface):
        ...
    


    def get_hitbox(self):
        return self.rect, None