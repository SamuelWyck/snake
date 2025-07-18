from level_objects.static_objects.pressure_plate.plate_segment import PlateSegment
from level_objects.proto_objects.transmitter import Transmitter



class PressurePlate(Transmitter):
    def __init__(self, topleft_positions, tile_size, color, images):
        super().__init__()

        self.color = color

        self.hit_segments = set()
        self.same_activation = False

        self.segments = []
        for position in topleft_positions:
            segment = PlateSegment(position, tile_size, images)
            self.segments.append(segment)
    


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
            self.toggle_recivers()
            self.same_activation = False
        
        self.hit_segments = set()