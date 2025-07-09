from static_level_objects.level_tile import LevelTile



class Wall(LevelTile):
    def __init__(self, topleft, size, image):
        super().__init__(topleft, size)

        self.image = image
    


    def update(self, surface, delta_time):
        self.draw(surface)



    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    


    def get_hitbox(self):
        return self.rect, None