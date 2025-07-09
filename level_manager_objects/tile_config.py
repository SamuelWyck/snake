from level_objects.static_level_objects.receiver import Receiver
from asset_loaders.image_loader import Images
from level_objects.static_level_objects.wall import Wall
from level_objects.static_level_objects.door import Door
from level_objects.static_level_objects.pressure_plate.pressure_plate import PressurePlate



class TileConfig:
    tile_map = {
        "W": Wall,
        "D": Door,
        "P": PressurePlate
    }
    empty_symbol = "O"
    tile_args_map = {
        "W": [Images.wall_img],
        "D": [Images.door_img],
        "P": [[Images.pressure_plate_img, Images.pressure_plate_pressed_img]]
    }

    tiles_to_explore = set(["P"])
    tiles_to_link = {}



    @classmethod
    def get_tile(cls, topleft, size, tile_symbol):
        tile_symbol, tile_id = cls.parse_tile_symbol(tile_symbol)

        tile_class = cls.tile_map[tile_symbol]
        tile_args = cls.tile_args_map[tile_symbol]
        tile = tile_class(topleft, size, *tile_args)

        if tile_id:
            cls.store_tile_with_id(tile_id, tile)

        return tile
    


    @classmethod
    def parse_tile_symbol(cls, tile_symbol):
        symbol_parts = tile_symbol.split("-")
        if len(symbol_parts) == 1:
            return tile_symbol, None
        return symbol_parts[0], symbol_parts[1]
    


    @classmethod
    def store_tile_with_id(cls, tile_id, tile):
        key = "transmitters"
        if isinstance(tile, Receiver):
            key = "receivers"

        if tile_id not in cls.tiles_to_link:
            cls.tiles_to_link[tile_id] = {}
        if key not in cls.tiles_to_link[tile_id]:
            cls.tiles_to_link[tile_id][key] = []

        cls.tiles_to_link[tile_id][key].append(tile)



    @classmethod
    def link_tiles(cls):
        for id in cls.tiles_to_link:
            link_map = cls.tiles_to_link[id]
            
            for transmitter_tile in link_map["transmitters"]:
                for receiver_tile in link_map["receivers"]:
                    transmitter_tile.link_receiver(receiver_tile)
        
        cls.tiles_to_link = {}



    @classmethod
    def is_empty_space(cls, tile_symbol):
        return tile_symbol == cls.empty_symbol



    @classmethod
    def is_explorable_tile(cls, tile_symbol):
        tile_symbol = tile_symbol.split("-")[0]
        return tile_symbol in cls.tiles_to_explore