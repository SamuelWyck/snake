import pygame



class LevelTile:
    def __init__(self, topleft, size):
        self.rect = pygame.rect.Rect(topleft, size)



    def update(self, surface, delta_time):
        ...
    


    def get_hitbox(self):
        return self.rect, None
    

    
    def set_topleft(self, topleft):
        self.rect.topleft = topleft
    


    def set_size(self, size):
        self.rect.size = size