import pygame
from user_interface.elements.text_display import TextDisplay
from asset_loaders.image_loader import Images
from utils.color import Color



class Tutorial:
    def __init__(self, topleft, level_tutorial_map, font, color, wrap_length=0, use_bg_image=False):
        self.tutorials_map = self.build_tutorial_displays(topleft, level_tutorial_map, font, color, wrap_length)

        self.wood_texture = Images.controls_menu_bg_img
        self.bg_image = None
        self.bg_image_topleft = None
        self.bg_image_padding = 5
        self.bg_image_border_width = 3

        self.use_bg_image = use_bg_image
        self.last_level_num = None



    def build_tutorial_displays(self, topleft, level_tutorials, font, color, wrap_length):
        tutorials_map = {}

        for level_num in level_tutorials:
            text_display = TextDisplay(topleft, font, color, level_tutorials[level_num], wrap_length=wrap_length)
            tutorials_map[level_num] = text_display

        return tutorials_map
    


    def get_bg_image(self, text_display):
        x_pos, y_pos = text_display.get_topleft()
        height_correction = 1
        self.bg_image_topleft = (x_pos - self.bg_image_padding, y_pos - self.bg_image_padding + height_correction)

        img_padding = self.bg_image_padding * 2
        self.bg_image = pygame.Surface((text_display.get_width() + img_padding, text_display.get_height() + img_padding))
        self.bg_image.blit(self.wood_texture, (0, 0))

        border = pygame.rect.Rect((0, 0), self.bg_image.get_rect().size)
        pygame.draw.rect(self.bg_image, Color.BLACK, border, width=self.bg_image_border_width)

    

    def draw(self, surface, level_num):
        if level_num not in self.tutorials_map:
            return 
        
        text_display = self.tutorials_map[level_num]

        if self.use_bg_image and level_num != self.last_level_num:
            self.get_bg_image(text_display)
            self.last_level_num = level_num

        if self.use_bg_image:
            surface.blit(self.bg_image, self.bg_image_topleft)

        text_display.update(surface)