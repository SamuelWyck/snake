import pygame



class PlayArea:
    topleft = (0, 0)
    size = (0, 0)
    surface = pygame.Surface(size)



    @classmethod
    def get_x(cls):
        return cls.topleft[0]
    


    @classmethod
    def get_y(cls):
        return cls.topleft[1]
    


    @classmethod
    def get_width(cls):
        return cls.size[0]
    


    @classmethod
    def get_height(cls):
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
        if size[0] < 0 or size[1] < 0:
            return
        
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

    

    @classmethod
    def fill(cls, color):
        cls.surface.fill(color)