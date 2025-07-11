import pygame



class Display:
    pygame.display.init()

    sizes = pygame.display.get_desktop_sizes()
    flags = pygame.FULLSCREEN
    screen = pygame.display.set_mode(sizes[0], flags=flags)
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    pygame.display.set_caption("Snake")