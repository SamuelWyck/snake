from level_objects.proto_objects.receiver import Receiver
from asset_loaders.image_loader import Images
from level_objects.static_objects.wall import Wall
from level_objects.static_objects.door import Door
from level_objects.static_objects.pressure_plate.pressure_plate import PressurePlate



class TileConfig:
    empty_symbol = "O"

    tile_delimiter = ","
    tile_id_delimiter = "-"

    transmitter_key = "transmitters"
    receiver_key = "receivers"

    tile_map = {
        "W": Wall,
        "D": Door,
        "P": PressurePlate
    }
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
        symbol_parts = tile_symbol.split(cls.tile_id_delimiter)
        if len(symbol_parts) == 1:
            return tile_symbol, None
        
        symbol_index = 0
        id_index = 1
        return symbol_parts[symbol_index], symbol_parts[id_index]
    


    @classmethod
    def store_tile_with_id(cls, tile_id, tile):
        tile_type = cls.transmitter_key
        if isinstance(tile, Receiver):
            tile_type = cls.receiver_key

        if tile_id not in cls.tiles_to_link:
            cls.tiles_to_link[tile_id] = {}
        if tile_type not in cls.tiles_to_link[tile_id]:
            cls.tiles_to_link[tile_id][tile_type] = []

        cls.tiles_to_link[tile_id][tile_type].append(tile)



    @classmethod
    def link_tiles(cls):
        for id in cls.tiles_to_link:
            link_map = cls.tiles_to_link[id]
            
            for transmitter_tile in link_map[cls.transmitter_key]:
                for receiver_tile in link_map[cls.receiver_key]:
                    transmitter_tile.link_receiver(receiver_tile)
        
        cls.tiles_to_link = {}



    @classmethod
    def is_empty_space(cls, tile_symbol):
        return tile_symbol == cls.empty_symbol



    @classmethod
    def is_explorable_tile(cls, tile_symbol):
        tile_symbol_index = 0
        symbol_parts = tile_symbol.split(cls.tile_id_delimiter)
        tile_symbol = symbol_parts[tile_symbol_index]
        return tile_symbol in cls.tiles_to_explore