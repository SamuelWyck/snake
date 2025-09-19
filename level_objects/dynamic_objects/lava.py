from level_objects.proto_objects.level_tile import LevelTile



class Lava(LevelTile):
    def __init__(self, topleft, size, color, image):
        super().__init__(topleft, size)

        self.color = color
        self.image = image
    

    def update(self, surface, delta_time):
        self.draw(surface)

    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    

    def get_hitbox(self):
        return self.rect