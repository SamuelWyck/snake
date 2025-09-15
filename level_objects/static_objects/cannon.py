import pygame
from level_objects.proto_objects.level_tile import LevelTile



class Cannon(LevelTile):
    def __init__(self, topleft, size, image, position_angle):
        super().__init__(topleft, size)

        self.image = pygame.transform.rotate(image, position_angle)
        
