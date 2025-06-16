import pygame
import time
import sys
from framework_objects.play_area import Play_Area




class Game:

    def __init__(self):
        pygame.display.init()

        #set up display
        sizes = pygame.display.get_desktop_sizes()
        flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(sizes[0], flags=flags)
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        pygame.display.set_caption("Snake")

        #set up game canvas 
        self.canvas_width, self.canvas_height = 1536, 864
        self.canvas = pygame.Surface((self.canvas_width, self.canvas_height))

        #set up play area canvas
        ps_width, ps_height = 1300, 700
        ps_topleft = (
            (self.canvas_width - ps_width)//2,
            (self.canvas_height - ps_height)//2
        )
        Play_Area.set_surface(ps_topleft, (ps_width, ps_height))

        self.framerate = 120

    

    def start(self):
        run = True
        last_time = time.time()
        clock = pygame.time.Clock()

        while run:
            delta_time = time.time() - last_time
            delta_time *= 60
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        run = False
                        pygame.quit()
                        sys.exit()


            self.canvas.fill((0, 0, 0))
            Play_Area.fill((255, 255, 255))
            Play_Area.set_surface_size((Play_Area.get_width() - 1, Play_Area.get_height()))


            Play_Area.draw_surface(self.canvas)
            self.screen.blit(pygame.transform.smoothscale(self.canvas, (self.screen_width, self.screen_height)), (0, 0))
            pygame.display.update()
            clock.tick(self.framerate)
    



def main():
    game = Game()
    game.start()




if __name__ == "__main__":
    main()