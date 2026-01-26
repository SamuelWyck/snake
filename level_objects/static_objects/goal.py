import pygame
from level_objects.proto_objects.level_tile import LevelTile
from asset_loaders.font_loader import Fonts
from utils.color import Color



class Goal(LevelTile):
    def __init__(self, topleft, size, image, color, value):
        super().__init__(topleft, size)

        self.image = self.build_image(color, value, image)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

        self.value = value
        self.color = color
    


    def update(self, surface, delta_time):
        self.draw(surface)
    


    def draw(self, surface):
        surface.blit(self.image, self.image_rect.topleft)
    


    def collide(self, player):
        if self.color != None and player.color != self.color:
            return False
        if self.value != None and player.real_length != self.value:
            return False
        return self.rect.colliderect(player.rect)
    


    def build_image(self, color, value, image):
        value_str = str(value) if value != None else ""
        value_image = Fonts.goal_font.render(value_str, True, Color.WHITE)

        image_outline = image.copy()
        colored_image = pygame.transform.smoothscale_by(image_outline, .8)
        image_outline.fill(Color.WHITE, special_flags=pygame.BLEND_ADD)
        if color != None:
            colored_image.fill(Color.WHITE, special_flags=pygame.BLEND_ADD)
            colored_image.fill(color, special_flags=pygame.BLEND_MIN)
        
        image_rect = image_outline.get_rect()
        value_img_rect = value_image.get_rect()
        value_img_rect.center = image_rect.center
        colored_image_rect = colored_image.get_rect()
        colored_image_rect.center = image_rect.center
        
        # visually correct value img rect
        value_img_rect.centery += 4

        image_outline.blit(colored_image, colored_image_rect.topleft)
        image_outline.blit(value_image, value_img_rect.topleft)
        return image_outline