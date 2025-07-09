from level_objects.static_objects.pressure_plate.pressure_plate import PressurePlate



class StickyPressurePlate(PressurePlate):
    def __init__(self, topleft_positions, tile_size, images):
        super().__init__(topleft_positions, tile_size, images)
    


    def close_receiver(self):
        pass