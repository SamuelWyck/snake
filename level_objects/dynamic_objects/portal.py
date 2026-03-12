import pygame
from level_objects.proto_objects.level_tile import LevelTile
from utils.color import Color
from utils.animation import Animation



class Portal(LevelTile):

    def __init__(self, topleft, size, image, frame_data, color):
        super().__init__(topleft, size)

        self.image = image
        self.animation = Animation(frame_data)
        self.animation_img = None

        self.color = color

        self.paired_portal = None

        self.object_to_teleport = None

        self.teleported_object = None
        self.hit_teleported_object = False



    def update(self, surface, delta_time):
        self.animation_img = self.animation.get_frame(delta_time)
        self.draw(surface)

        if not self.hit_teleported_object:
            self.teleported_object = None

        self.hit_teleported_object = False


    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        surface.blit(self.animation_img, self.rect.topleft)



    def link_portal(self, portal):
        self.paired_portal = portal



    def get_hitbox(self):
        return self.rect
    


    def teleport(self):
        if self.object_to_teleport == None:
            return
        
        self.object_to_teleport.rect.center = self.paired_portal.rect.center
        self.paired_portal.teleported_object = self.object_to_teleport
        self.paired_portal.hit_teleported_object = True

        self.object_to_teleport.handle_teleport()
        self.object_to_teleport = None



    def queue_teleport(self, collider, is_moveable):    
        if is_moveable(collider) and self.paired_portal.teleported_object != None:
            return False
        if self.object_to_teleport != None:
            return False
        
        self.object_to_teleport = collider
        return True



    def collide(self, collider):
        if self.color != Color.NO_COLOR and self.color != collider.color:
            return False
        if self.teleported_object != None and collider is not self.teleported_object:
            return False
        
        if collider is self.teleported_object and self.rect.contains(collider.rect):
            self.hit_teleported_object = True
            return False
        elif self.rect.contains(collider.rect):
            return True
            

    
    def reset(self):
        self.teleported_object = None
        self.hit_teleported_object = False