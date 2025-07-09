from static_level_objects.level_tile import LevelTile



class PlateSegment(LevelTile):
    def __init__(self, topleft, size, images):
        super().__init__(topleft, size)

        self.not_pressed_img = images[0]
        self.pressed_img = images[1]
        
        self.pressed = False

    

    def update(self, surface, delta_time):
        if self.pressed:
            self.draw(surface, self.pressed_img)
        else:
            self.draw(surface, self.not_pressed_img)

    

    def draw(self, surface, image=None):
        if not image:
            image = self.not_pressed_img
        
        surface.blit(image, self.rect.topleft)
    


    def get_hitbox(self):
        return self.rect, None
    


    def press(self):
        self.pressed = True


    
    def unpress(self):
        self.pressed = False