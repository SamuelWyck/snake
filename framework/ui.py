import pygame
from framework.main_menu import MainMenu
from asset_loaders.font_loader import Fonts
from utils.color import Color



class Ui:
    def __init__(self, screen_size, canvas_size, mouse_manager):
        self.main_menu = self.get_main_menu(screen_size, canvas_size, mouse_manager)
    


    def get_main_menu(self, screen_size, canvas_size, mouse_manager):
        btns_with_callbacks = [
            (Fonts.pickup_outline_font.render("PLAY", 1, Color.GREEN), Fonts.pickup_outline_font.render("PLAY", 1, Color.ORANGE), lambda **kwargs : True),
            (Fonts.pickup_outline_font.render("SETTINGS", 1, Color.GREEN), lambda **kwargs : False),
            (Fonts.pickup_outline_font.render("TUTORIAL", 1, Color.GREEN), lambda **kwargs : False),
            (Fonts.pickup_outline_font.render("EXIT", 1, Color.GREEN), lambda **kwargs : True)
        ]
        background_img = pygame.Surface((1536, 864))
        background_img.fill((0, 0, 0))
        main_menu = MainMenu(btns_with_callbacks, background_img, screen_size, canvas_size, mouse_manager, (0, 0), "PHASE SNAKE")
        return main_menu