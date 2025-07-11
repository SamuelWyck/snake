from level_objects.proto_objects.level_tile import LevelTile
from level_objects.proto_objects.receiver import Receiver



class Door(LevelTile, Receiver):
    def __init__(self, topleft, size, color, image):
        super().__init__(topleft, size)

        self.image = image
        self.color = color
        self.is_open = False
    


    def update(self, surface, delta_time):
        if not self.is_open:
            self.draw(surface)

    

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)



    def open(self):
        self.is_open = True

    

    def close(self):
        self.is_open = False


    
    def toggle(self):
        self.is_open = not self.is_open