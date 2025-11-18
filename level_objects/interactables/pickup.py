from level_objects.proto_objects.level_tile import LevelTile
from asset_loaders.font_loader import Fonts
from level_objects.agent_objects.snake.snake import Snake
from utils.color import Color


class Pickup(LevelTile):
    def __init__(self, topleft, size, value, color):
        super().__init__(topleft, size)

        self.color = color
        self.value = int(value)
        self.original_position = self.rect.center

        self.image = Fonts.pickup_outline_font.render(value, 1, Color.WHITE)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

        colored_image = Fonts.pickup_font.render(value, 1, self.color)
        self.image.blit(colored_image, (3, 2))

        self.remove = False

    

    def update(self, surface, delta_time):
        self.draw(surface)
    


    def draw(self, surface):
        surface.blit(self.image, self.image_rect.topleft)
    


    def collide(self, collider):
        if collider.__class__ != Snake:
            return False
        if self.color == collider.color and self.color != Color.NO_COLOR:
            return False
        return collider.rect.colliderect(self.rect)