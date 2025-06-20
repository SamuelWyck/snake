import pygame
import time
import sys
from framework_objects.play_area import Play_Area
from hud_objects.hud import Hud
from snake_objects.snake import Snake




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

        self.framerate = 120

        #set up game canvas 
        self.canvas_width, self.canvas_height = 1536, 864
        self.canvas = pygame.Surface((self.canvas_width, self.canvas_height))

        #set up play area canvas
        pa_width, pa_height = 1230, 630
        pa_topleft = (
            (self.canvas_width - pa_width)//2,
            (self.canvas_height - pa_height)//2
        )
        Play_Area.set_surface(pa_topleft, (pa_width, pa_height))

        #set up player
        player_step_size = 40
        player_topleft = (
            player_step_size * 4,
            player_step_size * 10
        )
        self.player = Snake(
            player_topleft, 
            size=30, 
            step_size=player_step_size, 
            step_interval=20, 
            color=(0, 255, 0), 
            controller=None
        )

        #set up hud manager
        self.hud = Hud(pa_topleft, (pa_width, pa_height))

    

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
            self.hud.draw(self.canvas)
            Play_Area.fill((0, 0, 0))
            self.player.update(Play_Area.surface, delta_time)

            Play_Area.draw_surface(self.canvas)
            self.screen.blit(pygame.transform.smoothscale(self.canvas, (self.screen_width, self.screen_height)), (0, 0))
            pygame.display.update()
            clock.tick(self.framerate)
    



def main():
    game = Game()
    game.start()




if __name__ == "__main__":
    main()