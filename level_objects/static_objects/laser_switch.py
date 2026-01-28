import pygame
from level_objects.proto_objects.transmitter import Transmitter
from utils.color import Color



class LaserSwitch(Transmitter):
    def __init__(self, topleft, size, color, base_image, socket_image, angle):
        super().__init__()
        angle = int(angle)

        self.rect = pygame.rect.Rect(topleft, size)
        self.target_side_coords = self.get_target_side_coords(angle)

        self.image = self.build_image(base_image, socket_image, color, angle)
        self.color = color

        self.is_on = False
        self.opened = False

    
    def build_image(self, base_image, socket_image, color, angle):
        image = socket_image.copy()
        color = color if color != Color.NO_COLOR else Color.GRAY
        image.fill(color, special_flags=pygame.BLEND_MAX)
        image.blit(base_image, (0, 0))
        image = pygame.transform.rotate(image, angle * -1) # correct angle because pygame rotates counter-clockwise
        return image
    

    def get_target_side_coords(self, angle):
        angle_up = 0
        angle_down = 180
        angle_right = 90
        if angle == angle_up:
            return self.rect.midtop
        if angle == angle_down:
            return self.rect.midbottom
        if angle == angle_right:
            return self.rect.midright
        return self.rect.midleft
    

    def update(self, surface, delta_time):
        if self.is_on and not self.opened:
            self.toggle_receivers()
            self.opened = True
        elif not self.is_on and self.opened:
            self.toggle_receivers()
            self.opened = False

        self.draw(surface)
        self.is_on = False


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


    def test_laser(self, laser):
        if self.color != laser.color and self.color != Color.NO_COLOR:
            return
        
        laser_end_coords = laser.get_end_coords()
        if laser_end_coords == self.target_side_coords:
            self.is_on = True
        

    def collide(self, rect):
        return self.rect.colliderect(rect)