import pygame
import time
import sys
from framework.display import Display
from framework.play_area import PlayArea
from framework.mouse import Mouse
from hud.hud import Hud
from level_manager.level_manager import LevelManager
from collision_manager.collision_manager import CollisionManager
from asset_loaders.image_loader import Images
from utils.color import Color



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
        PlayArea.set_surface_colorkey(Color.COLOR_KEY)
        PlayArea.set_use_backing_surface(True)

        #setup hud manager
        self.hud = Hud(pa_topleft, (pa_width, pa_height))

        #setup level manager and get player ref
        self.level_manager = LevelManager((pa_width, pa_height), single_tile_size=40)
        self.player = self.level_manager.load_level(1)
        self.player_controller = self.player.controller

        #setup collision manager
        self.collision_manager = CollisionManager((pa_width, pa_height))

        #setup mouse
        self.mouse = Mouse(self.canvas.size, self.screen.size, Images.mouse_img)

    

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
                    else:
                        self.player_controller.key_down(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.player_controller.mouse_down(event.button)
                elif event.type == pygame.KEYUP:
                    self.player_controller.key_up(event.key)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.player_controller.mouse_up(event.button)



            self.canvas.fill((0, 0, 0))
            self.hud.draw(self.canvas)
            PlayArea.blit(Images.background_img, topleft=(0, 0))

            self.mouse.update()
            mouse_pos = self.mouse.get_pos()

            self.level_manager.update(PlayArea.surface, delta_time)
            self.player.update(PlayArea.surface, delta_time)

            self.collision_manager.check_collisions(
                self.player, 
                self.level_manager.get_level_objects
            )

            PlayArea.backing_surface_blit(Images.wall_texture_img, (0, 0))
            PlayArea.draw_to_surface(self.canvas)

            self.mouse.draw(self.canvas)

            self.screen.blit(pygame.transform.smoothscale(self.canvas, (self.screen_width, self.screen_height)), (0, 0))
            pygame.display.update()

            self.player_controller.reset_inputs()
            clock.tick(self.framerate)
    



def main():
    game = Game()
    game.start()




if __name__ == "__main__":
    main()