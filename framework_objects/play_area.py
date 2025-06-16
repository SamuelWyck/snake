import pygame


# class Play_Area:

#     def __init__(self, topleft, size):
#         self.topleft = topleft
#         self.x = topleft[0]
#         self.y = topleft[1]

#         self.size = size
#         self.width = size[0]
#         self.height = size[1]

#         self.surface = pygame.Surface(size=size)
    

    
#     def blit(self, surface, topleft):
#         self.surface.blit(surface, topleft)

class Play_Area:
    topleft = (0, 0)
    size = (0, 0)
    surface = pygame.Surface(size)



    @property
    def x(cls):
        return cls.topleft[0]
    


    @property
    def y(cls):
        return cls.topleft[1]
    


    @property
    def width(cls):
        return cls.size[0]
    


    @property
    def height(cls):
        return cls.size[1]
    


    @classmethod
    def set_surface(cls, topleft, size):
        cls.topleft = topleft
        cls.size = size

        cls.surface = pygame.Surface(size)



    @classmethod
    def move_surface(cls, topleft):
        cls.topleft = topleft

    

    @classmethod
    def set_surface_size(cls, size):
        cls.size = size

        new_surface = pygame.Surface(size)
        new_surface.blit(pygame.transform.smoothscale(cls.surface, size), (0, 0))

        cls.surface = new_surface

    

    @classmethod
    def draw_surface(cls, surface):
        surface.blit(cls.surface, cls.topleft)



    @classmethod
    def blit(cls, surface, topleft):
        cls.surface.blit(surface, topleft)