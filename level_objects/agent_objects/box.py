import pygame
from level_objects.proto_objects.level_tile import LevelTile
from level_objects.agent_objects.snake.snake import Snake
from utils.color import Color



class Box(LevelTile):
    def __init__(self, topleft, size, color, image):
        super().__init__(topleft, size)

        self.image = self.build_image(color, image, size)
        self.color = color
        self.move_distance = self.rect.width
        self.original_topleft = topleft

    

    def build_image(self, color, image, size):
        background_img = pygame.Surface(size)
        color = color if color != Color.NO_COLOR else Color.GRAY
        background_img.fill(color)
        background_img.blit(image, (0, 0))
        return background_img



    def update(self, surface, delta_time):
        self.draw(surface)
    


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    

    def collide(self, rect):
        return self.rect.colliderect(rect)

    

    def move(self, collider, static_tiles, dynamic_tiles, agents, tile_to_skip, in_bounds):
        old_position = self.move_self(collider)

        if not in_bounds(self.rect):
            self.rect.center = old_position
            return False
        if collider.collide(self.rect):
            self.rect.center = old_position
            return False
        
        for tile in static_tiles:
            if tile_to_skip(tile):
                continue
            if tile.collide(self.rect):
                self.rect.center = old_position
                return False

        for tile in dynamic_tiles:
            if tile_to_skip(tile):
                continue
            if tile.collide(self.rect):
                self.rect.center = old_position
                return False

        for agent in agents:
            if agent == self or tile_to_skip(agent):
                continue
            if agent.collide(self.rect):
                self.rect.center = old_position
                return False
        
        return True
    


    def move_self(self, collider):
        old_position = self.rect.center

        direction = None
        if collider.__class__ != Snake:
            direction = "right"
            if collider.rect.centerx > self.rect.centerx:
                direction = "left"
            elif collider.rect.centery < self.rect.centery:
                direction = "down"
            elif collider.rect.centery > self.rect.centery:
                direction = "up"
        else:
            direction = collider.get_direction_as_str()

        if direction == "right":
            self.rect.x += self.move_distance
        elif direction == "left":
            self.rect.x -= self.move_distance
        elif direction == "up":
            self.rect.y -= self.move_distance
        else:
            self.rect.y += self.move_distance

        return old_position
    


    def reset(self):
        self.rect.topleft = self.original_topleft