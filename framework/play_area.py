import pygame



class PlayArea:
    topleft = (0, 0)
    size = (0, 0)
    surface = pygame.Surface(size)

    backing_surface = pygame.Surface(size)
    use_backing_surface = False



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
        cls.backing_surface = pygame.Surface(size)



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
        cls.backing_surface = pygame.Surface(size)

    

    @classmethod
    def draw_to_surface(cls, surface):
        if not cls.use_backing_surface:
            surface.blit(cls.surface, cls.topleft)
            return

        cls.backing_surface.blit(cls.surface, (0, 0))
        surface.blit(cls.backing_surface, cls.topleft)



    @classmethod
    def blit(cls, surface, topleft):
        cls.surface.blit(surface, topleft)

    

    @classmethod
    def backing_surface_blit(cls, surface, topleft):
        cls.backing_surface.blit(surface, topleft)

    

    @classmethod
    def fill(cls, color):
        cls.surface.fill(color)



    @classmethod
    def backing_surface_fill(cls, color):
        cls.backing_surface.fill(color)

    

    @classmethod
    def set_surface_colorkey(cls, color):
        cls.surface.set_colorkey(color)

    

    def get_surface_colorkey(cls):
        return cls.surface.get_colorkey()

    

    @classmethod
    def set_use_backing_surface(cls, use_backing_surface):
        cls.use_backing_surface = use_backing_surface