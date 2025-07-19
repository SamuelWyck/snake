from level_objects.dynamic_objects.pressure_plate.pressure_plate import PressurePlate



class StickyPressurePlate(PressurePlate):
    def __init__(self, topleft_positions, tile_size, color, images):
        super().__init__(topleft_positions, tile_size, color, images)



    def update(self, surface, delta_time):
        for segment in self.segments:
            if segment in self.hit_segments:
                segment.press()
            else:
                segment.unpress()

            segment.update(surface, delta_time)
        

        if len(self.hit_segments) == len(self.segments) and not self.same_activation:
            self.toggle_recivers()
            self.same_activation = True
        elif len(self.hit_segments) != len(self.segments) and self.same_activation:
            self.same_activation = False
        
        self.hit_segments = set()
