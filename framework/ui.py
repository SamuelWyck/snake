import pygame
from framework.user_interface.button_menu import ButtonMenu
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
        self.antialias = True

        self.audio_menu = self.get_audio_menu(screen_size, canvas_size, mouse_manager)
        self.settings_menu = self.get_settings_menu(screen_size, canvas_size, mouse_manager)
        self.main_menu = self.get_main_menu(screen_size, canvas_size, mouse_manager)
    


    def get_main_menu(self, screen_size, canvas_size, mouse_manager):
        button_gap = 20
        buttons_topleft = (30, 550)

        background_img = pygame.Surface(canvas_size)
        background_img.fill((0, 0, 0))

        title_text_display = TextDisplay(
            topleft=(0, 0), font=Fonts.title_font, color=Color.GREEN, text="PHASE SNAKE"
        )

        play_btn = Button(
            topleft=(0, 0), 
            image=Fonts.pickup_outline_font.render("PLAY", self.antialias, Color.GREEN),
            hover_image=Fonts.pickup_outline_font.render("PLAY", self.antialias, Color.ORANGE),
        )
        play_btn_callback = lambda **kwargs : (True, False)
        settings_btn = Button(
            topleft=(0, 0),
            image=Fonts.pickup_outline_font.render("SETTINGS", self.antialias, Color.GREEN),
            hover_image=Fonts.pickup_outline_font.render("SETTINGS", self.antialias, Color.ORANGE)
        )
        settings_btn_callback = self.settings_menu.run
        exit_btn = Button(
            topleft=(0, 0),
            image=Fonts.pickup_outline_font.render("EXIT", self.antialias, Color.GREEN),
            hover_image=Fonts.pickup_outline_font.render("EXIT", self.antialias, Color.ORANGE)
        )
        exit_btn_callback = lambda **kwargs : (True, True)

        main_menu = ButtonMenu(
            buttons_topleft, button_gap, background_img,
            screen_size, canvas_size, mouse_manager,
            title_text_display,
            (play_btn, play_btn_callback),
            (settings_btn, settings_btn_callback),
            (exit_btn, exit_btn_callback)
        )

        return main_menu
    


    def get_settings_menu(self, screen_size, canvas_size, mouse_manager):
        button_gap = 20
        buttons_topleft = (30, 550)

        background_img = pygame.Surface(canvas_size)
        background_img.fill((0, 0, 0))

        title_text_display = TextDisplay(
            topleft=(0, 0), font=Fonts.title_font, color=Color.GREEN, text="SETTINGS"
        )

        controls_button = Button(
            topleft=(0, 0),
            image=Fonts.pickup_outline_font.render("CONTROLS", self.antialias, Color.GREEN),
            hover_image=Fonts.pickup_outline_font.render("CONTROLS", self.antialias, Color.ORANGE)
        )
        controls_button_callback = lambda **kwargs : (False, False)
        mouse_button = Button(
            topleft=(0, 0),
            image=Fonts.pickup_outline_font.render("MOUSE", self.antialias, Color.GREEN),
            hover_image=Fonts.pickup_outline_font.render("MOUSE", self.antialias, Color.ORANGE)
        )
        mouse_button_callback = lambda **kwargs : (False, False)
        audio_button = Button(
            topleft=(0, 0),
            image=Fonts.pickup_outline_font.render("AUDIO", self.antialias, Color.GREEN),
            hover_image=Fonts.pickup_outline_font.render("AUDIO", self.antialias, Color.ORANGE)
        )
        audio_button_callback = self.audio_menu.run
        back_button = Button(
            topleft=(0, 0),
            image=Fonts.pickup_outline_font.render("BACK", self.antialias, Color.GREEN),
            hover_image=Fonts.pickup_outline_font.render("BACK", self.antialias, Color.ORANGE)
        )
        back_button_callback = lambda **kwargs : (True, (False, None))

        settings_menu = ButtonMenu(
            buttons_topleft, button_gap, background_img, 
            screen_size, canvas_size, mouse_manager,
            title_text_display,
            (controls_button, controls_button_callback),
            (mouse_button, mouse_button_callback),
            (audio_button, audio_button_callback),
            (back_button, back_button_callback)
        )

        return settings_menu
    


    @staticmethod
    def get_slider_str_val(slider):
        return str(round(slider.value, 2))



    def get_audio_menu(self, screen_size, canvas_size, mouse_manager):
        start_y_pos = 50
        element_gap = 15
        info_gap = 40

        background_img = pygame.Surface(canvas_size)
        background_img.fill((0, 0, 0))

        menu_title = TextDisplay(topleft=(0, 0), font=Fonts.title_font, color=Color.GREEN, text="AUDIO")

        sound_text = TextDisplay(
            topleft=(0, 0), font=Fonts.pickup_outline_font, color=Color.GREEN, text="SOUNDS"
        )
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

        music_text = TextDisplay(
            topleft=(0, 0), font=Fonts.pickup_outline_font, color=Color.GREEN, text="MUSIC"
        )
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
            image=Fonts.pickup_outline_font.render("BACK", self.antialias, Color.GREEN),
            hover_image=Fonts.pickup_outline_font.render("BACK", self.antialias, Color.ORANGE)
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