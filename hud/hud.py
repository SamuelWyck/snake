import pygame
from asset_loaders.image_loader import Images
from hud.border import Border
from user_interface.elements.live_text_display import LiveTextDisplay
from asset_loaders.font_loader import Fonts
from utils.color import Color



class Hud:
    def __init__(self, pa_topleft, pa_size):
        border_width = 40
        self.border = Border(
            topleft=(pa_topleft[0] - border_width, pa_topleft[1] - border_width),
            size=(pa_size[0] + (2 * border_width), pa_size[1] + (2 * border_width)),
            width=border_width,
            images=[Images.horizontal_border_img, Images.vertical_border_img]
        )
        self.player_length_display = None
        self.length_display_backing_center = None
    


    def draw(self, surface):
        self.border.draw(surface)

        if self.player_length_display != None:
            pygame.draw.circle(surface, Color.WHITE, self.length_display_backing_center, radius=30)
            self.player_length_display.update(surface)

    

    def create_length_display(self, player):
        center = (54,45)
        backing_center = (54, 46)
        length_getter = lambda player: str(player.real_length)

        self.player_length_display = LiveTextDisplay(
            topleft=(0, 0), font=Fonts.pickup_outline_font, color=Color.GRASS_GREEN,
            object_ref=player, text_getter=length_getter, 
        )
        self.player_length_display.set_center(center)

        self.length_display_backing_center = backing_center