from level_objects.dynamic_objects.pressure_plate.pressure_plate import PressurePlate



class StickyPressurePlate(PressurePlate):
    def __init__(self, topleft_positions, tile_size, color, images):
        super().__init__(topleft_positions, tile_size, color, images)

        self.activated = False



    def update(self, surface, delta_time):
        for segment in self.segments:
            if segment in self.hit_segments or self.activated:
                segment.press()
            else:
                segment.unpress()

            segment.update(surface, delta_time)
        

        if len(self.hit_segments) == len(self.segments) and not self.same_activation:
            self.toggle_receivers()
            self.same_activation = True
            self.activated = not self.activated
        elif len(self.hit_segments) != len(self.segments) and self.same_activation:
            self.same_activation = False
        
        self.hit_segments = set()
