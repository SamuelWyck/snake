import pygame
from asset_loaders.image_loader import Images
from hud.border import Border
from user_interface.elements.live_text_display import LiveTextDisplay
from user_interface.elements.text_display import TextDisplay
from asset_loaders.font_loader import Fonts
from asset_loaders.image_loader import Images
from utils.color import Color



class Hud:
    def __init__(self, pa_topleft, pa_size, screen_size):
        border_width = 40
        self.border = Border(
            topleft=(pa_topleft[0] - border_width, pa_topleft[1] - border_width),
            size=(pa_size[0] + (2 * border_width), pa_size[1] + (2 * border_width)),
            width=border_width,
            images=[Images.horizontal_border_img, Images.vertical_border_img]
        )

        # variables needed for player length display
        self.player_length_display = None
        self.length_display_bg_img = Images.length_display
        self.length_display_bg_rect = self.length_display_bg_img.get_rect()
        backing_center = (54, 54)
        self.length_display_bg_rect.center = backing_center

        # variables needed for player pickups display
        self.player_pickups = None
        _, screen_height = screen_size
        self.pickups_center_y_start = screen_height - 250
        self.pickups_center_x = 54
        self.pickups_gap = 10
        self.player_pickups_length = 0
        self.num_shown_pickups = 6
        self.pickups_start_idx = 0
        # create rect for bg with a size slightly bigger than the tiles size of 40
        self.pickups_display_bg = pygame.rect.Rect((0, 0), (48, 48))
        # eaten pickups border image
        self.pickups_border = Images.eaten_pickups_border
        self.pickups_border_rect = self.pickups_border.get_rect()
        self.pickups_border_rect.topleft = (15, 278)

        # variables for level num display
        level_display_x = 1325
        level_display_y = 10
        self.level_title_display = TextDisplay(
            topleft=(level_display_x, level_display_y), 
            font=Fonts.pickup_outline_font, color=Color.YELLOW, text="LEVEL:"
        )
        self.level_num_display = TextDisplay(
            topleft=(self.level_title_display.get_width() + level_display_x + 10, level_display_y), 
            font=Fonts.pickup_outline_font,
            color=Color.YELLOW,
            text="999"
        )
        


    def update_level_num(self, level_num):
        self.level_num_display.change_text(str(level_num + 1))

        

    def draw(self, surface):
        self.border.draw(surface)

        if self.player_length_display != None:
            self.draw_length_display(surface)
        
        if self.player_pickups != None:
            self.update_player_pickups(surface)

        self.level_title_display.update(surface)
        self.level_num_display.update(surface)

        
    
    def draw_length_display(self, surface):
        surface.blit(self.length_display_bg_img, self.length_display_bg_rect.topleft)
        self.player_length_display.update(surface)

    

    def create_length_display(self, player):
        length_getter = lambda player: str(player.real_length)
        self.player_length_display = LiveTextDisplay(
            topleft=(0, 0), font=Fonts.pickup_outline_font, color=Color.MENU_GREEN,
            object_ref=player, text_getter=length_getter, 
        )

        # subtract one from center to visually center font
        center = (self.length_display_bg_rect.centerx, self.length_display_bg_rect.centery - 1)
        self.player_length_display.set_center(center)


    
    def link_player_pickups_list(self, player):
        self.player_pickups = player.eaten_pickups

    

    def update_player_pickups(self, surface):
        if self.player_pickups_length != len(self.player_pickups):
            self.player_pickups_length = len(self.player_pickups)

            self.pickups_start_idx = self.player_pickups_length - self.num_shown_pickups
            if self.pickups_start_idx < 0:
                self.pickups_start_idx = 0

            center_y = self.pickups_center_y_start
            first_pickup = None
            for idx in range(self.pickups_start_idx, len(self.player_pickups)):
                pickup = self.player_pickups[idx]
                pickup.set_center_position((self.pickups_center_x, center_y))
                center_y -= (pickup.image_rect.height + self.pickups_gap)
                if first_pickup is None:
                    first_pickup = pickup
            
            self.adjust_bg_rect(first_pickup)
        
        self.draw_player_pickups(surface)
    


    def draw_player_pickups(self, surface):
        if self.player_pickups_length != 0:
            pygame.draw.rect(surface, Color.YELLOW, self.pickups_display_bg, border_radius=28)

            for idx in range(self.pickups_start_idx, self.player_pickups_length):
                pickup = self.player_pickups[idx]
                pickup.update(surface, None)

        surface.blit(self.pickups_border, self.pickups_border_rect.topleft)
    


    def adjust_bg_rect(self, first_pickup):
        if first_pickup is None:
            return

        num_displayed_pickups = self.player_pickups_length
        if num_displayed_pickups > self.num_shown_pickups:
            num_displayed_pickups = self.num_shown_pickups

        height = (num_displayed_pickups * first_pickup.image_rect.height) + (
            self.pickups_gap * (num_displayed_pickups - 1))
        self.pickups_display_bg.height = height
        self.pickups_display_bg.midbottom = first_pickup.image_rect.midbottom