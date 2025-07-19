from level_objects.proto_objects.receiver import Receiver
from asset_loaders.image_loader import Images
from level_objects.static_objects.wall import Wall
from level_objects.dynamic_objects.door import Door
from level_objects.dynamic_objects.pressure_plate.pressure_plate import PressurePlate
from level_objects.dynamic_objects.sticky_pressure_plate import StickyPressurePlate
from level_objects.agent_objects.box import Box
from utils.color import Color



class TileConfig:
    empty_symbol = "O"

    tile_delimiter = ","
    tile_data_delimiter = "-"

    transmitter_key = "transmitters"
    receiver_key = "receivers"

    start_door_open = True

    tile_map = {
        "W": Wall,
        "DO": Door,
        "DC": Door,
        "P": PressurePlate,
        "SP": StickyPressurePlate,
        "B": Box
    }
    tile_args_map = {
        "W": {
            "b": [Color.BLUE, Images.wall_img],
            "o": [Color.ORANGE, Images.wall_img],
            "g": [Color.GREEN, Images.wall_img],
            "r": [Color.RED, Images.wall_img],
            "NOCOLOR": [Color.NO_COLOR, Images.wall_img]   
        },
        "DO": {
            "NOCOLOR": [Color.NO_COLOR, Images.door_img, start_door_open]
        },
        "DC": {
            "NOCOLOR": [Color.NO_COLOR, Images.door_img, not start_door_open]
        },
        "P": {
            "NOCOLOR": [Color.NO_COLOR, [Images.pressure_plate_img, Images.pressure_plate_pressed_img]]
        },
        "SP": {
            "NOCOLOR": [Color.NO_COLOR, [Images.pressure_plate_img, Images.pressure_plate_pressed_img]]
        },
        "B": {
            "NOCOLOR": [Color.NO_COLOR, Images.box_img]
        }
    }

    static_tiles = set([Wall])
    dynamic_tiles = set([
        StickyPressurePlate,
        PressurePlate,
        Door
    ])


    tiles_to_explore = set(["P", "SP"])
    tiles_to_link = {}



    @classmethod
    def get_tile(cls, topleft, size, tile_symbol):
        tile_symbol, tile_color, tile_id = cls.parse_tile_symbol(tile_symbol)

        tile_class = cls.tile_map[tile_symbol]
        tile_args = cls.tile_args_map[tile_symbol][tile_color]
        tile = tile_class(topleft, size, *tile_args)

        if tile_id:
            cls.store_tile_with_id(tile_id, tile)

        return tile
    


    @classmethod
    def parse_tile_symbol(cls, tile_symbol):
        symbol_index = 0
        color_index = 1
        id_index = 2
        symbol_parts = tile_symbol.split(cls.tile_data_delimiter)

        symbol = symbol_parts[symbol_index]
        id = None
        color = "NOCOLOR"

        if len(symbol_parts) == 2:
            if symbol_parts[1] in cls.tile_args_map[symbol]:
                color = symbol_parts[1]
            else:
                id = symbol_parts[1]
        elif len(symbol_parts) == 3:
            id = symbol_parts[id_index]
            color = symbol_parts[color_index]

        
        return symbol, color, id
    


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
        symbol_parts = tile_symbol.split(cls.tile_data_delimiter)
        tile_symbol = symbol_parts[tile_symbol_index]
        return tile_symbol in cls.tiles_to_explore
    


    @classmethod
    def is_static_tile(cls, tile):
        return tile.__class__ in cls.static_tiles
    


    @classmethod
    def is_dynamic_tile(cls, tile):
        return tile.__class__ in cls.dynamic_tiles