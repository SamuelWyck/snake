from level_objects.static_level_objects.pressure_plate.plate_segment import PlateSegment
from level_objects.proto_objects.transmitter import Transmitter



class PressurePlate(Transmitter):
    def __init__(self, topleft_positions, tile_size, images):
        super().__init__()
        self.segments = []
        for position in topleft_positions:
            segment = PlateSegment(position, tile_size, images)
            self.segments.append(segment)
    


    def update(self, surface, delta_time):
        for segment in self.segments:
            segment.update(surface, delta_time)