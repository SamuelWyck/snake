from level_objects.proto_objects.level_tile import LevelTile
from asset_loaders.audio_loader import Audio



class PlateSegment(LevelTile):
    def __init__(self, topleft, size, images):
        super().__init__(topleft, size)

        self.not_pressed_img = images[0]
        self.pressed_img = images[1]
        
        self.pressed = False

        self.press_sound = Audio.get_sound_effect("plate_press", "plate")
        self.unpress_sound = Audio.get_sound_effect("plate_unpress", "plate")

    

    def update(self, surface, delta_time):
        if self.pressed:
            self.draw(surface, self.pressed_img)
        else:
            self.draw(surface, self.not_pressed_img)

    

    def draw(self, surface, image=None):
        if not image:
            image = self.not_pressed_img
        
        surface.blit(image, self.rect.topleft)
    


    def press(self):
        if self.pressed:
            return

        self.pressed = True
        self.press_sound.hard_play()


    
    def unpress(self):
        if not self.pressed:
            return
        
        self.pressed = False
        self.unpress_sound.hard_play()