import pygame
from level_objects.dynamic_objects.sticky_pressure_plate import StickyPressurePlate
from asset_loaders.font_loader import Fonts
from utils.color import Color



class ColorLengthPlate(StickyPressurePlate):
    def __init__(self, topleft_positions, tile_size, pressed_img, color, length):
        images = self.create_images(pressed_img, color, length, tile_size)
        super().__init__(topleft_positions, tile_size, color, images)

        self.length = length

    

    def create_images(self, pressed_img, color, length, tile_size):
        border_thickness = 2
        color = color if color != Color.NO_COLOR else Color.GRAY

        pressed_img_base = pygame.Surface(tile_size)
        pressed_img_base.fill(color)
        pressed_img_base.blit(pressed_img, (0, 0))
        self.draw_image_border(pressed_img_base, border_thickness, tile_size[0])


        unpressed_image_base = pygame.Surface(tile_size)
        unpressed_image_base.fill(color)

        str_length = str(length) if length != None else ""
        length_render = Fonts.goal_font.render(str_length, antialias=True, color=Color.WHITE)
        length_render_rect = length_render.get_rect()
        unpressed_image_rect = unpressed_image_base.get_rect()
        length_render_rect.center = unpressed_image_rect.center
        unpressed_image_base.blit(length_render, length_render_rect.topleft)
        self.draw_image_border(unpressed_image_base, border_thickness, tile_size[0])

        return [unpressed_image_base, pressed_img_base]
    

    
    def draw_image_border(self, image, border_thickness, tile_size):
        image_padding = 3
        border_width = tile_size - (image_padding * 2)

        border_rect = pygame.rect.Rect(
            (image_padding, image_padding), 
            (border_width, border_width)
        )

        pygame.draw.rect(image, Color.WHITE, border_rect, width=border_thickness)



    def can_collide(self, player):
        color_match = player.color == self.color or self.color == Color.NO_COLOR
        length_match = player.real_length == self.length or self.length == None
        return color_match and length_match
