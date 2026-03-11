from level_objects.proto_objects.level_tile import LevelTile
from utils.color import Color



class Portal(LevelTile):

    def __init__(self, topleft, size, image, color):
        super().__init__(topleft, size)

        self.image = image
        self.color = color

        self.paired_portal = None

        self.teleported_object = None
        self.hit_teleported_object = False

    

    def update(self, surface, delta_time):
        self.draw(surface)

        if not self.hit_teleported_object:
            self.teleported_object = None

        self.hit_teleported_object = False


    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)



    def link_portal(self, portal):
        self.paired_portal = portal



    def get_hitbox(self):
        return self.rect
    


    def position_moveable_for_teleport(self, collider, player, moveable_old_pos):
        spacing = 10

        collider.rect.center = self.paired_portal.rect.center

        old_x, old_y = moveable_old_pos
        if player.rect.centerx < old_x:
            collider.rect.centerx -= spacing
        elif player.rect.centerx > old_x:
            collider.rect.centerx += spacing
        elif player.rect.centery < old_y:
            collider.rect.centery -= spacing
        elif player.rect.centery > old_y:
            collider.rect.centery += spacing



    def teleport(self, collider, player, is_moveable, static_tiles, dynamic_tiles, agents, is_box_skippable, in_bounds):    
        if is_moveable(collider) and is_moveable(self.paired_portal.teleported_object):
            old_pos = collider.rect.center
            self.position_moveable_for_teleport(collider, player, old_pos)

            if self.paired_portal.teleported_object.move(
                collider, static_tiles, dynamic_tiles, agents, is_box_skippable, in_bounds
            ):
                collider.rect.center = self.paired_portal.rect.center
                self.paired_portal.teleported_object = collider
                self.paired_portal.hit_teleported_object = True
                return True
            else:
                collider.rect.center = old_pos
                self.hit_teleported_object = True
                self.teleported_object = collider
                return False
            
        else:
            collider.rect.center = self.paired_portal.rect.center
            self.paired_portal.teleported_object = collider
            self.paired_portal.hit_teleported_object = True
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