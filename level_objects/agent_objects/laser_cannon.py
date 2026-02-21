import pygame
from framework.play_area import PlayArea
from level_objects.proto_objects.level_tile import LevelTile
from level_objects.agent_objects.snake.snake import Snake
from level_objects.interactables.laser import Laser
from utils.color import Color



class LaserCannon(LevelTile):
    def __init__(self, topleft, size, color, image, barrel_image, moveable, angle, interactables, lasers):
        super().__init__(topleft, size)

        angle = int(angle)
        self.image = self.build_image(image, barrel_image, color, angle)
        self.angle = angle
        self.color = color

        self.moveable = moveable
        self.original_topleft = self.rect.topleft
        self.move_distance = self.rect.width

        self.laser_max_length, _ = PlayArea.size
        self.laser_short_length = 8

        self.laser = Laser(
            self.get_laser_start_coords(), 
            self.angle, 
            self.color, 
            self.laser_max_length, 
            self.laser_short_length
        )
        interactables.append(self.laser)
        lasers.append(self.laser)

    
    def build_image(self, base_image, barrel_image, color, angle):
        image = barrel_image.copy()
        color = color if color != Color.NO_COLOR else Color.GRAY
        image.fill(color, special_flags=pygame.BLEND_MAX)
        image.blit(base_image, (0, 0))
        
        image = pygame.transform.rotate(image, angle * -1) # correct angle because pygame rotates counter-clockwise
        return image
    

    def get_laser_start_coords(self):
        angle_up = 0
        angle_right = 90
        angle_down = 180
        if self.angle == angle_up:
            return self.rect.midtop
        if self.angle == angle_right:
            return self.rect.midright
        if self.angle == angle_down:
            return self.rect.midbottom
        return self.rect.midleft

    
    def update(self, surface, delta_time):
        self.draw(surface)


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    

    def collide(self, rect):
        return self.rect.colliderect(rect)


    def move(self, collider, static_tiles, dynamic_tiles, agents, tile_to_skip, in_bounds):
        if not self.moveable:
            return False
        
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
        
        new_laser_start = self.get_laser_start_coords()
        self.laser.set_laser_start(new_laser_start)
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
        laser_start_coords = self.get_laser_start_coords()
        self.laser.set_laser_start(laser_start_coords)