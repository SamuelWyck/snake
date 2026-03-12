import pygame
from level_objects.proto_objects.level_tile import LevelTile
from level_objects.agent_objects.snake.snake import Snake
from utils.color import Color



class Box(LevelTile):
    def __init__(self, topleft, size, color, image, good_warn_img, bad_warn_img):
        super().__init__(topleft, size)

        self.image = self.build_image(color, image, size)
        self.color = color
        self.move_distance = self.rect.width
        self.original_topleft = topleft

        # variables for warning ghost rect
        width, _  = size
        self.hor_ghost_trigger_rect = pygame.rect.Rect((0, 0), (width * 2, width // 2))
        self.hor_ghost_trigger_rect.center = self.rect.center
        self.vert_ghost_trigger_rect = pygame.rect.Rect((0, 0), (width // 2, width * 2))
        self.vert_ghost_trigger_rect.center = self.rect.center

        self.ghost_rect = pygame.rect.Rect((0, 0), size)
        self.draw_ghost_rect = False
        self.warn_move = False
        self.good_warn_img = good_warn_img
        self.bad_warn_img = bad_warn_img

    

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

        if self.draw_ghost_rect:
            warn_img = self.good_warn_img if not self.warn_move else self.bad_warn_img
            surface.blit(warn_img, self.ghost_rect.topleft)
            self.draw_ghost_rect = False
            self.warn_move = False

    

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
        
        self.position_trigger_rects()
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
    


    def position_trigger_rects(self):
        self.hor_ghost_trigger_rect.center = self.rect.center
        self.vert_ghost_trigger_rect.center = self.rect.center



    def trigger_ghost_rect(self, player_rect):
        if player_rect.center == self.rect.center:
            return False
        
        self.draw_ghost_rect = True
        self.ghost_rect.center = self.rect.center

        if player_rect.centerx < self.rect.centerx:
            self.ghost_rect.x += self.rect.width
        elif player_rect.centerx > self.rect.centerx:
            self.ghost_rect.x -= self.rect.width
        elif player_rect.centery < self.rect.centery:
            self.ghost_rect.y += self.rect.height
        elif player_rect.centery > self.rect.centery:
            self.ghost_rect.y -= self.rect.height

        return True



    def reset(self):
        self.rect.topleft = self.original_topleft
        self.position_trigger_rects()
        self.warn_move = False
        self.draw_ghost_rect = False

    

    def handle_teleport(self):
        self.position_trigger_rects()