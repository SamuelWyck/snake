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
    


    def teleport(self, collider):        
        collider.rect.center = self.paired_portal.rect.center

        self.paired_portal.teleported_object = collider
        self.paired_portal.hit_teleported_object = True



    def collide(self, collider):
        if self.color != Color.NO_COLOR and self.color != collider.color:
            return False
        
        if self.rect.contains(collider.rect):
            if collider is self.teleported_object:
                self.hit_teleported_object = True
                return False
            else:
                return True
            

    
    def reset(self):
        self.teleported_object = None
        self.hit_teleported_object = False