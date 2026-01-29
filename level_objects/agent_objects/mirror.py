import pygame
from level_objects.interactables.laser import Laser
from level_objects.agent_objects.snake.snake import Snake
from level_objects.proto_objects.level_tile import LevelTile
from framework.play_area import PlayArea
from utils.color import Color



class Mirror(LevelTile):
    def __init__(
            self, topleft, size, color, base_img, color_img, moveable, angle, interactables, lasers
        ):
        super().__init__(topleft, size)

        self.original_position = self.rect.center
        self.move_distance = self.rect.width

        angle = int(angle)
        self.image = self.build_images(base_img, color_img, color, angle)

        self.color = color
        self.moveable = moveable

        self.angle = angle
        self.angle_up = 0
        self.angle_down = 180
        self.angle_right = 90
        self.angle_left = 270

        self.lasers = lasers
        self.interactables = interactables

        self.laser_max_length, _ = PlayArea.size
        self.laser_short_length = 8

        self.first_target_coords, self.second_target_coords = self.get_target_coords()
        self.first_bounce_laser, self.second_bounce_laser = self.get_bounce_lasers()

        self.entrance_bounce_laser = self.first_bounce_laser
        self.exit_bounce_laser = self.second_bounce_laser
        self.entrance_laser_color = None
        self.exit_laser_color = None
        self.laser = None
        self.last_laser_color = None

        self.is_hit = False


    def build_images(self, base_img, color_img, color, angle):
        color = color if color != Color.NO_COLOR else Color.GRAY

        image = color_img.copy()
        image.fill(color, special_flags=pygame.BLEND_MAX)
        image.blit(base_img, (0, 0))
        image = pygame.transform.rotate(image, angle * -1) # correct angle because pygame rotates counter-clockwise

        return image

    
    def update(self, surface, delta_time):
        if not self.is_hit and self.laser != None:
            self.laser.remove = True
            self.laser = None

        self.draw(surface)
        self.is_hit = False
    

    def draw(self, surface):
        if self.is_hit:
            pygame.draw.rect(surface, self.entrance_laser_color, self.entrance_bounce_laser)
            pygame.draw.rect(surface, self.exit_laser_color, self.exit_bounce_laser)
        surface.blit(self.image, self.rect.topleft)

    
    def collide(self, rect):
        return self.rect.colliderect(rect)
    

    def test_laser(self, laser):
        if laser == self.laser:
            return
        laser_end_coords = laser.get_end_coords()
        if laser_end_coords != self.first_target_coords and laser_end_coords != self.second_target_coords:
            return
        if self.laser != None and self.laser.start_coords == laser_end_coords:
            return
        if self.laser != None and laser.color == self.last_laser_color:
            self.is_hit = True
            return

        self.entrance_laser_color = laser.color if laser.color != Color.NO_COLOR else Color.GRAY
        self.exit_laser_color = self.color if self.color != Color.NO_COLOR else laser.color
        self.exit_laser_color = self.exit_laser_color if self.exit_laser_color != Color.NO_COLOR else Color.GRAY

        new_laser_start = self.first_target_coords
        self.entrance_bounce_laser = self.second_bounce_laser
        self.exit_bounce_laser = self.first_bounce_laser
        if laser_end_coords == self.first_target_coords:
            new_laser_start = self.second_target_coords
            self.entrance_bounce_laser = self.first_bounce_laser
            self.exit_bounce_laser = self.second_bounce_laser
        
        laser_color = laser.color if self.color == Color.NO_COLOR else self.color
        if self.laser != None:
            self.laser.remove = True
        self.laser = Laser(
            new_laser_start, 
            self.get_laser_angle(new_laser_start), 
            laser_color, 
            self.laser_max_length, 
            self.laser_short_length
        )
        self.interactables.append(self.laser)
        self.lasers.append(self.laser)
        self.is_hit = True
        self.last_laser_color = laser.color
        

    def get_target_coords(self):
        if self.angle == self.angle_up:
            return self.rect.midbottom, self.rect.midright
        if self.angle == self.angle_right:
            return self.rect.midleft, self.rect.midbottom
        if self.angle == self.angle_down:
            return self.rect.midtop, self.rect.midleft
        if self.angle == self.angle_left:
            return self.rect.midright, self.rect.midtop
        
    
    def get_bounce_lasers(self):
        laser_long_length = self.rect.width * .75
        first_laser = pygame.rect.Rect((0, 0), (0, 0))
        second_laser = pygame.rect.Rect((0, 0), (0, 0))
        if self.angle == self.angle_up or self.angle == self.angle_down:
            first_laser.height = laser_long_length
            first_laser.width = self.laser_short_length
            second_laser.width = laser_long_length
            second_laser.height = self.laser_short_length
        else:
            first_laser.width = laser_long_length
            first_laser.height = self.laser_short_length
            second_laser.width = self.laser_short_length
            second_laser.height = laser_long_length
        
        if self.angle == self.angle_up:
            first_laser.midbottom = self.first_target_coords
            second_laser.midright = self.second_target_coords
        elif self.angle == self.angle_right:
            first_laser.midleft = self.first_target_coords
            second_laser.midbottom = self.second_target_coords
        elif self.angle == self.angle_down:
            first_laser.midtop = self.first_target_coords
            second_laser.midleft = self.second_target_coords
        else:
            first_laser.midright = self.first_target_coords
            second_laser.midtop = self.second_target_coords
        
        return first_laser, second_laser

    

    def get_laser_angle(self, start_coords):
        if self.angle == self.angle_up:
            angle = self.angle_right if start_coords != self.first_target_coords else self.angle_down
            return angle
        if self.angle == self.angle_right:
            angle = self.angle_down if start_coords != self.first_target_coords else self.angle_left
            return angle
        if self.angle == self.angle_down:
            angle = self.angle_left if start_coords != self.first_target_coords else self.angle_up
            return angle
        if self.angle == self.angle_left:
            angle = self.angle_up if start_coords != self.first_target_coords else self.angle_right

    
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
            if agent == self:
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
        self.rect.center = self.original_position