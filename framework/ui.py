import pygame
from framework.menu import Menu
from asset_loaders.font_loader import Fonts
from utils.color import Color



class Ui:
    def __init__(self, screen_size, canvas_size, mouse_manager):
        self.main_menu = self.get_main_menu(screen_size, canvas_size, mouse_manager)
    


    def get_main_menu(self, screen_size, canvas_size, mouse_manager):
        btns_with_callbacks = [
            (Fonts.pickup_outline_font.render("PLAY", 1, Color.GREEN), Fonts.pickup_outline_font.render("PLAY", 1, Color.ORANGE), lambda **kwargs : (True, False)),
            (Fonts.pickup_outline_font.render("SETTINGS", 1, Color.GREEN), self.get_settings_menu(screen_size, canvas_size, mouse_manager)),
            # (Fonts.pickup_outline_font.render("TUTORIAL", 1, Color.GREEN), lambda **kwargs : False),
            (Fonts.pickup_outline_font.render("EXIT", 1, Color.GREEN), lambda **kwargs : (True, True))
        ]
        background_img = pygame.Surface((1536, 864))
        background_img.fill((0, 0, 0))
        main_menu = Menu(
            btns_with_callbacks, 
            background_img, 
            screen_size, 
            canvas_size, 
            mouse_manager, 
            btns_topleft=(30, 550), 
            title="PHASE SNAKE"
        )
        return main_menu
    


    def get_settings_menu(self, screen_size, canvas_size, mouse_manager):
        btn_imgs_with_callbacks = [
            (
                Fonts.pickup_outline_font.render("CONTROLS", 1, Color.GREEN), 
                Fonts.pickup_outline_font.render("CONTROLS", 1, Color.ORANGE), 
                lambda **kwargs : (False, False)
            ),
            (
                Fonts.pickup_outline_font.render("MOUSE", 1, Color.GREEN),
                Fonts.pickup_outline_font.render("MOUSE", 1, Color.ORANGE),
                lambda **kwargs : (False, False)
            ),
            (
                Fonts.pickup_outline_font.render("BACK", 1, Color.GREEN),
                Fonts.pickup_outline_font.render("BACK", 1, Color.ORANGE),
                lambda **kwargs : (True, (False, None))
            )
        ]
        background_img = pygame.Surface((1536, 864))
        background_img.fill((0, 0, 0))
        settings_menu = Menu(
            btn_imgs_with_callbacks,
            background_img,
            screen_size,
            canvas_size,
            mouse_manager,
            btns_topleft=(30, 550),
            title="SETTINGS"
        )

        return settings_menu.run
