import pygame
import time
import sys
from framework_objects.display import Display
from framework_objects.play_area import PlayArea
from hud_objects.hud import Hud
from snake_objects.snake import Snake
from controllers.player_controller import PlayerController
from level_manager_objects.level_manager import LevelManager




class Game:
    def __init__(self):

        #setup display variables
        self.screen = Display.screen
        self.screen_width = Display.screen_width
        self.screen_height = Display.screen_height

        self.framerate = 480

        #setup game canvas 
        self.canvas_width, self.canvas_height = 1536, 864
        self.canvas = pygame.Surface((self.canvas_width, self.canvas_height))

        #setup play area canvas
        pa_width, pa_height = 1240, 640
        pa_topleft = (
            (self.canvas_width - pa_width)//2,
            (self.canvas_height - pa_height)//2
        )
        PlayArea.set_surface(pa_topleft, (pa_width, pa_height))

        #setup player controller
        player_controls = {
            "UP": pygame.K_w,
            "DOWN": pygame.K_s,
            "RIGHT": pygame.K_d,
            "LEFT": pygame.K_a
        }
        self.player_controller = PlayerController(player_controls, holdable_inputs=set())

        #setup player
        player_step_size = 40
        player_size = 30
        player_topleft = (
            player_step_size * 4 + ((player_step_size - player_size) // 2),
            player_step_size * 10 + ((player_step_size - player_size) // 2)
        )
        self.player = Snake(
            player_topleft, 
            size=player_size, 
            step_size=player_step_size, 
            step_interval=25, 
            color=(0, 255, 0), 
            controller=self.player_controller
        )

        #setup hud manager
        self.hud = Hud(pa_topleft, (pa_width, pa_height))

        #setup level manager
        self.level_manager = LevelManager((pa_width, pa_height), single_tile_size=40)
        self.level_manager.load_level(1)

    

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
                    #temp event set up to test player growth
                    elif event.key == pygame.K_e:
                        self.player.grow_snake()
                    else:
                        self.player_controller.key_down(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.player_controller.mouse_down(event.button)



            self.canvas.fill((0, 0, 0))
            self.hud.draw(self.canvas)
            PlayArea.fill((0, 0, 0))

            self.level_manager.update(PlayArea.surface, delta_time)
            self.player.update(PlayArea.surface, delta_time)

            PlayArea.draw_surface(self.canvas)
            self.screen.blit(pygame.transform.smoothscale(self.canvas, (self.screen_width, self.screen_height)), (0, 0))
            pygame.display.update()

            self.player_controller.reset_inputs()
            clock.tick(self.framerate)
    



def main():
    game = Game()
    game.start()




if __name__ == "__main__":
    main()