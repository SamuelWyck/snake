import pygame
from level_manager.tile_config import TileConfig
from user_interface.button_menu import ButtonMenu
from user_interface.general_menu import GeneralMenu
from user_interface.select_menu import SelectMenu
from user_interface.control_menu import ControlMenu
from user_interface.elements.button import Button
from user_interface.elements.slider import Slider
from user_interface.elements.text_display import TextDisplay
from user_interface.elements.live_text_display import LiveTextDisplay
from asset_loaders.font_loader import Fonts
from asset_loaders.image_loader import Images
from utils.color import Color



# button callbacks return shape must be (bool, info) where bool is whether to exit the menu or not,
# and info is any info to pass along when the menu is exited

class Ui:
    def __init__(self, screen_size, canvas_size, mouse_manager, level_manager):
        self.slider_size = (300, 50)
        self.slide_border_radius = 20
        self.antialias = True

        self.control_menu = self.get_control_menu(screen_size, canvas_size, mouse_manager)
        self.audio_menu = self.get_audio_menu(screen_size, canvas_size, mouse_manager)
        self.mouse_menu = self.get_mouse_menu(screen_size, canvas_size, mouse_manager)
        self.settings_menu = self.get_settings_menu(screen_size, canvas_size, mouse_manager)
        self.level_select_menu = self.get_level_select_menu(screen_size, canvas_size, mouse_manager)
        self.main_menu = self.get_main_menu(screen_size, canvas_size, mouse_manager)
        self.pause_menu = self.get_pause_menu(screen_size, canvas_size, mouse_manager, level_manager)
        self.win_menu = self.get_win_menu(screen_size, canvas_size, mouse_manager, level_manager)
    


    def get_main_menu(self, screen_size, canvas_size, mouse_manager):
        button_gap = 20
        buttons_topleft = (30, 550)

        play_btn = Button(topleft=(0, 0), image=Images.play_btn_img, hover_image=Images.play_btn_hvr_img)
        play_btn_callback = self.level_select_menu.run

        settings_btn = Button(topleft=(0, 0), image=Images.settings_btn_img, hover_image=Images.settings_btn_hvr_img)
        settings_btn_callback = self.settings_menu.run

        exit_btn = Button(topleft=(0, 0), image=Images.exit_btn_img, hover_image=Images.exit_btn_hvr_img)
        exit_btn_callback = lambda **kwargs : (True, (True, None))

        btns_with_callbacks = [
            (play_btn, play_btn_callback),
            (settings_btn, settings_btn_callback),
            (exit_btn, exit_btn_callback)
        ]

        main_menu = ButtonMenu(
            buttons_topleft, button_gap, Images.main_menu_bg_img,
            screen_size, canvas_size, mouse_manager,
            btns_with_callbacks
        )

        return main_menu
    


    def get_settings_menu(self, screen_size, canvas_size, mouse_manager):
        button_gap = 20
        buttons_topleft = (30, 500)

        background_img = pygame.Surface(canvas_size)
        background_img.fill((0, 0, 0))

        title_text_display = TextDisplay(
            topleft=(0, 0), font=Fonts.title_font, color=Color.GREEN, text="SETTINGS"
        )

        controls_button = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("CONTROLS", self.antialias, Color.GREEN),
            hover_image=Fonts.menu_font.render("CONTROLS", self.antialias, Color.ORANGE)
        )
        controls_button_callback = self.control_menu.run
        mouse_button = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("MOUSE", self.antialias, Color.GREEN),
            hover_image=Fonts.menu_font.render("MOUSE", self.antialias, Color.ORANGE)
        )
        mouse_button_callback = self.mouse_menu.run
        audio_button = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("AUDIO", self.antialias, Color.GREEN),
            hover_image=Fonts.menu_font.render("AUDIO", self.antialias, Color.ORANGE)
        )
        audio_button_callback = self.audio_menu.run
        back_button = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("BACK", self.antialias, Color.GREEN),
            hover_image=Fonts.menu_font.render("BACK", self.antialias, Color.ORANGE)
        )
        back_button_callback = lambda **kwargs : (True, (False, None))

        btns_with_callbacks = [
            (audio_button, audio_button_callback),
            (controls_button, controls_button_callback),
            (mouse_button, mouse_button_callback),
            (back_button, back_button_callback)
        ]

        settings_menu = ButtonMenu(
            buttons_topleft, button_gap, background_img, 
            screen_size, canvas_size, mouse_manager,
            btns_with_callbacks,
            title_text_display
        )

        return settings_menu
    


    def get_mouse_menu(self, screen_size, canvas_size, mouse_manager):
        start_y_pos = 50 
        element_gap = 15
        info_gap = 40

        background_img = pygame.Surface(canvas_size)
        background_img.fill((0, 0, 0))

        title_display = TextDisplay(
            topleft=(0, 0), font=Fonts.title_font, color=Color.GREEN, text="MOUSE SETTINGS"
        )

        mouse_text = TextDisplay(
            topleft=(0, 0), font=Fonts.pickup_outline_font, color=Color.GREEN, text="SENSITIVITY"
        )
        mouse_slider = Slider(
            topleft=(0, 0),
            size=self.slider_size, callback=mouse_manager.set_sensitivity,
            slide_bar_color=Color.GREEN, slide_color=Color.ORANGE,
            border_radius=self.slide_border_radius
        )
        mouse_slider_val = LiveTextDisplay(
            topleft=(0, 0), font=Fonts.goal_font, color=Color.GREEN, 
            object_ref=mouse_slider, text_getter=self.get_mouse_slider_val
        )

        back_button = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("BACK", self.antialias, Color.GREEN),
            hover_image=Fonts.menu_font.render("BACK", self.antialias, Color.ORANGE)
        )
        back_button_callback = lambda **kwargs: (True, (False, None))

        init_callback = lambda : mouse_slider.set_value(mouse_manager.get_sensitivity_val())
        cleanup_callback = mouse_manager.save_sensitivity

        mouse_menu = GeneralMenu(
            start_y_pos, element_gap, background_img,
            mouse_manager, screen_size, canvas_size,
            init_callback,
            cleanup_callback,
            title_display,
            info_gap,
            mouse_text, mouse_slider_val, mouse_slider,
            info_gap,
            (back_button, back_button_callback)
        )

        return mouse_menu



    @staticmethod
    def get_slider_str_val(slider):
        return str(round(slider.value, 2))
    


    @staticmethod
    def get_mouse_slider_val(slider):
        value = round(slider.value, 2) * 2
        if value < .1:
            value = .1
        return str(value)



    def get_audio_menu(self, screen_size, canvas_size, mouse_manager):
        start_y_pos = 50
        element_gap = 15
        info_gap = 40

        background_img = pygame.Surface(canvas_size)
        background_img.fill((0, 0, 0))

        menu_title = TextDisplay(topleft=(0, 0), font=Fonts.title_font, color=Color.GREEN, text="AUDIO SETTINGS")

        sound_text = TextDisplay(
            topleft=(0, 0), font=Fonts.pickup_outline_font, color=Color.GREEN, text="SOUND EFFECTS"
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
            image=Fonts.menu_font.render("BACK", self.antialias, Color.GREEN),
            hover_image=Fonts.menu_font.render("BACK", self.antialias, Color.ORANGE)
        )
        back_btn_callback = lambda **kwargs: (True, (False, None))

        cleanup_callback = lambda : None

        menu = GeneralMenu(
            start_y_pos, element_gap, 
            background_img, mouse_manager, 
            screen_size, canvas_size, None, cleanup_callback,
            menu_title,
            info_gap,
            sound_text, sounds_slider_val, sound_slider, 
            info_gap, 
            music_text, music_slider_val, music_slider,
            info_gap,
            (back_btn, back_btn_callback)
        )

        return menu
    


    def get_level_select_menu(self, screen_size, canvas_size, mouse_manager):
        starting_y = 290
        num_cols = 4
        num_rows = 3
        row_gap = 10
        col_gap = 20

        click_callback = lambda id: (True, (False, id))

        buttons = []
        for i in range(1, 17):
            image = Fonts.menu_font.render(str(i), self.antialias, Color.YELLOW)
            hover_image = Fonts.menu_font.render(str(i), self.antialias, Color.MENU_GREEN)
            button = Button(topleft=(0, 0),image=image, hover_image=hover_image)
            buttons.append(button)

        
        exit_btn = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("BACK", self.antialias, Color.YELLOW),
            hover_image=Fonts.menu_font.render("BACK", self.antialias, Color.MENU_GREEN)
        )

        page_up_btn = Button(
            topleft=(0, 0), 
            image=Fonts.menu_font.render("PAGE UP", self.antialias, Color.YELLOW),
            hover_image=Fonts.menu_font.render("PAGE UP", self.antialias, Color.MENU_GREEN)
        )
        page_down_btn = Button(
            topleft=(0, 0), 
            image=Fonts.menu_font.render("PAGE DOWN", self.antialias, Color.YELLOW),
            hover_image=Fonts.menu_font.render("PAGE DOWN", self.antialias, Color.MENU_GREEN)
        )

        select_menu = SelectMenu(
            starting_y, num_cols, num_rows, col_gap, row_gap, 
            Images.level_menu_bg_img, screen_size, canvas_size, mouse_manager, 
            page_up_btn, page_down_btn, exit_btn, click_callback, buttons
        )

        return select_menu
    


    def get_control_menu(self, screen_size, canvas_size, mouse_manager):
        y_pos = 250
        row_gap = 20
        col_gap = 40
        num_rows = 4

        controls = dict(TileConfig.player_controller.controls)

        background_img = pygame.Surface(canvas_size)
        background_img.fill((0, 0, 0))

        control_menu = ControlMenu(
            y_pos, num_rows, row_gap, col_gap, controls, 
            background_img, Fonts.menu_font,
            Color.GREEN, Color.ORANGE,
            canvas_size, screen_size, mouse_manager,
            TileConfig.player_controller.update_controls
        )

        return control_menu
    

    def get_pause_menu(self, screen_size, canvas_size, mouse_manager, level_manager):
        y_pos = 250
        gap = 20

        resume_btn = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("RESUME", antialias=True, color=Color.YELLOW),
            hover_image=Fonts.menu_font.render("RESUME", antialias=True, color=Color.MENU_GREEN)
        )
        resume_btn_callback = lambda **kwargs : (True, (False, None))

        level_btn = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("LEVEL SELECT", antialias=True, color=Color.YELLOW),
            hover_image=Fonts.menu_font.render("LEVEL SELECT", antialias=True, color=Color.MENU_GREEN)
        )
        level_btn_callback = self.level_select_menu.run

        settings_btn = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("SETTINGS", antialias=True, color=Color.YELLOW),
            hover_image=Fonts.menu_font.render("SETTINGS", antialias=True, color=Color.MENU_GREEN)
        )
        settings_btn_callback = self.settings_menu.run

        reset_btn = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("RESET", antialias=True, color=Color.YELLOW),
            hover_image=Fonts.menu_font.render("RESET", antialias=True, color=Color.MENU_GREEN)
        )
        reset_btn_callback = lambda **kwargs : (True, (False, level_manager.current_level))

        quit_btn = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("QUIT", antialias=True, color=Color.YELLOW),
            hover_image=Fonts.menu_font.render("QUIT", antialias=True, color=Color.MENU_GREEN)
        )
        quit_btn_callback = lambda **kwargs : (True, (True, None))

        pause_menu = GeneralMenu(
            y_pos, gap,
            Images.pause_bg_img,
            mouse_manager,
            screen_size,
            canvas_size,
            None,
            None,
            (resume_btn, resume_btn_callback),
            (level_btn, level_btn_callback),
            (settings_btn, settings_btn_callback),
            (reset_btn, reset_btn_callback),
            (quit_btn, quit_btn_callback)
        )

        return pause_menu
    


    def get_win_menu(self, screen_size, canvas_size, mouse_manager, level_manager):
        y_pos = 250
        gap = 20
        title_gap = 35
        init_callback = None
        cleanup_callback = None


        lvl_cleared_display = TextDisplay(
            topleft=(0, 0), font=Fonts.level_win_font, color=Color.YELLOW, text="LEVEL CLEARED!"
        )

        level_btn = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("LEVEL SELECT", antialias=True, color=Color.YELLOW),
            hover_image=Fonts.menu_font.render("LEVEL SELECT", antialias=True, color=Color.MENU_GREEN)
        )
        level_btn_callback = self.level_select_menu.run

        quit_btn = Button(
            topleft=(0, 0),
            image=Fonts.menu_font.render("QUIT", antialias=True, color=Color.YELLOW),
            hover_image=Fonts.menu_font.render("QUIT", antialias=True, color=Color.MENU_GREEN)
        )
        quit_btn_callback = lambda **kwargs : (True, (True, None))


        win_menu = GeneralMenu(
            y_pos, gap, 
            Images.pause_bg_img, mouse_manager,
            screen_size, canvas_size,
            init_callback, cleanup_callback,
            lvl_cleared_display,
            title_gap,
            (level_btn, level_btn_callback),
            (quit_btn, quit_btn_callback)
        )

        return win_menu