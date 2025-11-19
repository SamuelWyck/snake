import pygame
from level_objects.proto_objects.level_tile import LevelTile
from asset_loaders.font_loader import Fonts
from utils.color import Color



class Goal(LevelTile):
    def __init__(self, topleft, size, color, value, image):
        super().__init__(topleft, size)

        self.image = self.build_image(color, value, image)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

        self.length = value
        self.color = color
    


    def update(self, surface, delta_time):
        self.draw(surface)
    


    def draw(self, surface):
        surface.blit(self.image, self.image_rect.topleft)
    


    def collide(self, player):
        if self.color != None and player.color != self.color:
            return False
        if self.value != None and player.body_length != self.length:
            return False
        return True
    


    def build_image(self, color, value, image):
        value_str = str(value) if value != None else "∞"
        value_image = Fonts.pickup_font.render(value_str, True, Color.WHITE)

        image_base = image
        if color != None:
            image_base.fill(color, special_flags=pygame.BLEND_MIN)
        
        image_rect = image_base.get_rect()
        value_img_rect = value_image.get_rect()
        value_img_rect.center = image_rect.center

        image_base.blit(value_image, value_img_rect.topleft)
        return image_base