import pygame
from framework.user_interface.menu import Menu
from framework.user_interface.general_menu import GeneralMenu
from framework.user_interface.button import Button
from framework.user_interface.slider import Slider
from framework.user_interface.text_display import TextDisplay
from framework.user_interface.live_text_display import LiveTextDisplay
from asset_loaders.font_loader import Fonts
from utils.color import Color



# button callbacks return shape must be (bool, info) where bool is whether to exit the menu or not,
# and info is any info to pass along when the menu is exited

class Ui:
    def __init__(self, screen_size, canvas_size, mouse_manager):
        self.slider_size = (250, 50)
        self.slide_border_radius = 20

        self.audio_menu = self.get_audio_menu(screen_size, canvas_size, mouse_manager)
        self.settings_menu = self.get_settings_menu(screen_size, canvas_size, mouse_manager)
        self.main_menu = self.get_main_menu(screen_size, canvas_size, mouse_manager)
    


    def get_main_menu(self, screen_size, canvas_size, mouse_manager):
        btns_with_callbacks = [
            (Fonts.pickup_outline_font.render("PLAY", 1, Color.GREEN), Fonts.pickup_outline_font.render("PLAY", 1, Color.ORANGE), lambda **kwargs : (True, False)),
            (Fonts.pickup_outline_font.render("SETTINGS", 1, Color.GREEN), self.settings_menu.run),
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
                Fonts.pickup_outline_font.render("AUDIO", 1, Color.GREEN),
                Fonts.pickup_outline_font.render("AUDIO", 1, Color.ORANGE),
                self.audio_menu.run
            ),
            (
                Fonts.pickup_outline_font.render("BACK", 1, Color.GREEN),
                Fonts.pickup_outline_font.render("BACK", 1, Color.ORANGE),
                lambda **kwargs : (True, (False, None))
            )
        ]
        background_img = pygame.Surface(canvas_size)
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

        return settings_menu
    


    @staticmethod
    def get_slider_str_val(slider):
        return str(round(slider.value, 2))



    def get_audio_menu(self, screen_size, canvas_size, mouse_manager):
        start_y_pos = 50
        element_gap = 15
        info_gap = 40
        antialias = True

        background_img = pygame.Surface(canvas_size)
        background_img.fill((0, 0, 0))

        menu_title = TextDisplay(topleft=(0, 0), font=Fonts.title_font, color=Color.GREEN, text="AUDIO")

        sound_text = TextDisplay(topleft=(0, 0), font=Fonts.pickup_outline_font, color=Color.GREEN, text="SOUNDS")
        sound_slider = Slider(
            topleft=(0, 0), size=self.slider_size, 
            slide_bar_color=Color.GREEN, slide_color=Color.ORANGE, 
            border_radius=self.slide_border_radius, callback=lambda val: None
        )
        sounds_slider_val = LiveTextDisplay(
            topleft=(0, 0), font=Fonts.goal_font, 
            color=Color.GREEN, object_ref=sound_slider,
            text_getter=self.get_slider_str_val
        )

        music_text = TextDisplay(topleft=(0, 0), font=Fonts.pickup_outline_font, color=Color.GREEN, text="MUSIC")
        music_slider = Slider(
            topleft=(0, 0), size=self.slider_size, 
            slide_bar_color=Color.GREEN, slide_color=Color.ORANGE,
            border_radius=self.slide_border_radius, callback=lambda val: None
        )
        music_slider_val = LiveTextDisplay(
            topleft=(0, 0), font=Fonts.goal_font,
            color=Color.GREEN, object_ref=music_slider,
            text_getter=self.get_slider_str_val
        )

        back_btn = Button(
            topleft=(0, 0), 
            image=Fonts.pickup_outline_font.render("BACK", antialias, Color.GREEN),
            hover_image=Fonts.pickup_outline_font.render("BACK", antialias, Color.ORANGE)
        )
        back_btn_callback = lambda **kwargs: (True, (False, None))

        menu = GeneralMenu(
            start_y_pos, element_gap, 
            background_img, mouse_manager, 
            screen_size, canvas_size,
            menu_title,
            info_gap,
            sound_text, sounds_slider_val, sound_slider, 
            info_gap, 
            music_text, music_slider_val, music_slider,
            info_gap,
            (back_btn, back_btn_callback)
        )

        return menu