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
        self.length_display_bg_img = Images.length_display
        self.length_display_bg_rect = self.length_display_bg_img.get_rect()
        backing_center = (54, 46)
        self.length_display_bg_rect.center = backing_center
    


    def draw(self, surface):
        self.border.draw(surface)

        if self.player_length_display != None:
            self.draw_length_display(surface)

        
    
    def draw_length_display(self, surface):
        surface.blit(self.length_display_bg_img, self.length_display_bg_rect.topleft)
        self.player_length_display.update(surface)


    

    def create_length_display(self, player):
        length_getter = lambda player: str(player.real_length)
        self.player_length_display = LiveTextDisplay(
            topleft=(0, 0), font=Fonts.pickup_outline_font, color=Color.GRASS_GREEN,
            object_ref=player, text_getter=length_getter, 
        )

        # subtract one from center to visually center font
        center = (self.length_display_bg_rect.centerx, self.length_display_bg_rect.centery - 1)
        self.player_length_display.set_center(center)