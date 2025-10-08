import pygame
from level_objects.proto_objects.receiver import Receiver
from asset_loaders.image_loader import Images
from level_objects.static_objects.wall import Wall
from level_objects.static_objects.cannon import Cannon
from level_objects.dynamic_objects.lava import Lava
from level_objects.dynamic_objects.door import Door
from level_objects.dynamic_objects.pressure_plate.pressure_plate import PressurePlate
from level_objects.dynamic_objects.sticky_pressure_plate import StickyPressurePlate
from level_objects.agent_objects.box import Box
from level_objects.agent_objects.spike_ball import SpikeBall
from level_objects.agent_objects.snake.snake import Snake
from controllers.player_controller import PlayerController
from utils.color import Color



class TileConfig:
    player_controls = {
        "UP": pygame.K_w,
        "DOWN": pygame.K_s,
        "RIGHT": pygame.K_d,
        "LEFT": pygame.K_a,
        "GROW": pygame.K_SPACE,
        "SHRINK": pygame.K_LSHIFT
    }
    player_controller = PlayerController(
        player_controls, 
        holdable_inputs=set(["GROW", "SHRINK"])
    )

    snake_size = 30
    snake_step_size = 40
    snake_step_interval = 25
    snake_args = [
        snake_size,
        snake_step_size,
        snake_step_interval
    ]

    spike_ball_size = 30
    spike_ball_vel = 2

    empty_symbol = "O"
    wall_symbol = "W"

    tile_delimiter = ","
    tile_data_delimiter = "-"

    transmitter_key = "transmitters"
    receiver_key = "receivers"

    start_door_open = True
    circular_path = True
    angle_up = 180
    angle_down = 0
    angle_left = -90
    angle_right = 90

    tile_map = {
        "W": Wall,
        "DO": Door,
        "DC": Door,
        "P": PressurePlate,
        "SP": StickyPressurePlate,
        "B": Box,
        "SH": Snake,
        "PSH": Snake,
        "S": SpikeBall,
        "SC": SpikeBall,
        "CU": Cannon,
        "CD": Cannon,
        "CL": Cannon,
        "CR": Cannon,
        "L": Lava
    }
    tile_args_map = {
        "W": {
            "b": [Color.BLUE, Color.COLOR_KEY],
            "o": [Color.ORANGE, Color.COLOR_KEY],
            "g": [Color.GREEN, Color.COLOR_KEY],
            "r": [Color.RED, Color.COLOR_KEY],
            "NOCOLOR": [Color.NO_COLOR, Color.COLOR_KEY]   
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
        },
        "PSH": {
            "b": [*snake_args, Color.BLUE, player_controller],
            "o": [*snake_args, Color.ORANGE, player_controller],
            "g": [*snake_args, Images.green_snake_img, Color.GREEN, player_controller],
            "r": [*snake_args, Color.RED, player_controller],
            "NOCOLOR": [*snake_args, Images.green_snake_img, Color.GREEN, player_controller]
        },
        "S": {
            "b": [spike_ball_size, spike_ball_vel, Color.BLUE, Images.spike_ball_img, not circular_path],
            "o": [spike_ball_size, spike_ball_vel, Color.ORANGE, Images.spike_ball_img, not circular_path],
            "g": [spike_ball_size, spike_ball_vel, Color.GREEN, Images.spike_ball_img, not circular_path],
            "r": [spike_ball_size, spike_ball_vel, Color.RED, Images.spike_ball_img, not circular_path],
            "NOCOLOR": [spike_ball_size, spike_ball_vel, Color.NO_COLOR, Images.spike_ball_img, not circular_path]
        },
        "SC": {
            "b": [spike_ball_size, spike_ball_vel, Color.BLUE, Images.spike_ball_img, circular_path],
            "o": [spike_ball_size, spike_ball_vel, Color.ORANGE, Images.spike_ball_img, circular_path],
            "g": [spike_ball_size, spike_ball_vel, Color.GREEN, Images.spike_ball_img, circular_path],
            "r": [spike_ball_size, spike_ball_vel, Color.RED, Images.spike_ball_img, circular_path],
            "NOCOLOR": [spike_ball_size, spike_ball_vel, Color.NO_COLOR, Images.spike_ball_img, circular_path]
        },
        "CU": {
            "b": [Images.pressure_plate_img, Images.bullet_img, Color.BLUE, angle_up],
            "o": [Images.pressure_plate_img, Images.bullet_img, Color.ORANGE, angle_up],
            "g": [Images.pressure_plate_img, Images.bullet_img, Color.GREEN, angle_up],
            "r": [Images.pressure_plate_img, Images.bullet_img, Color.RED, angle_up],
            "NOCOLOR": [Images.pressure_plate_img, Images.bullet_img, Color.NO_COLOR, angle_up]
        },
        "CD": {
            "b": [Images.pressure_plate_img, Images.bullet_img, Color.BLUE, angle_down],
            "o": [Images.pressure_plate_img, Images.bullet_img, Color.ORANGE, angle_down],
            "g": [Images.pressure_plate_img, Images.bullet_img, Color.GREEN, angle_down],
            "r": [Images.pressure_plate_img, Images.bullet_img, Color.RED, angle_down],
            "NOCOLOR": [Images.pressure_plate_img, Images.bullet_img, Color.NO_COLOR, angle_down]
        },
        "CL": {
            "b": [Images.pressure_plate_img, Images.bullet_img, Color.BLUE, angle_left],
            "o": [Images.pressure_plate_img, Images.bullet_img, Color.ORANGE, angle_left],
            "g": [Images.pressure_plate_img, Images.bullet_img, Color.GREEN, angle_left],
            "r": [Images.pressure_plate_img, Images.bullet_img, Color.RED, angle_left],
            "NOCOLOR": [Images.pressure_plate_img, Images.bullet_img, Color.NO_COLOR, angle_left]
        },
        "CR": {
            "b": [Images.pressure_plate_img, Images.bullet_img, Color.BLUE, angle_right],
            "o": [Images.pressure_plate_img, Images.bullet_img, Color.ORANGE, angle_right],
            "g": [Images.pressure_plate_img, Images.bullet_img, Color.GREEN, angle_right],
            "r": [Images.pressure_plate_img, Images.bullet_img, Color.RED, angle_right],
            "NOCOLOR": [Images.pressure_plate_img, Images.bullet_img, Color.NO_COLOR, angle_right]
        },
        "L": {
            "b": [Color.BLUE, Images.lava_img],
            "o": [Color.ORANGE, Images.lava_img],
            "g": [Color.GREEN, Images.lava_img],
            "r": [Color.RED, Images.lava_img],
            "NOCOLOR": [Color.NO_COLOR, Images.lava_img]
        }
    }

    static_tiles = set([Wall, Cannon])
    dynamic_tiles = set([
        StickyPressurePlate,
        PressurePlate,
        Door,
        Lava
    ])
    tiles_needing_interactables = set([Cannon])


    tiles_to_explore = set(["P", "SP"])
    island_tiles_to_find = set(["S", "SC"])
    snake_head_symbols = set(["SH", "PSH"])
    snake_segment_symbol = "SS"
    tiles_to_link = {}



    @classmethod
    def get_tile(cls, topleft, size, tile_symbol, interactable_list):
        tile_symbol, tile_color, tile_id = cls.parse_tile_symbol(tile_symbol)

        tile_class = cls.tile_map[tile_symbol]
        tile_args = cls.tile_args_map[tile_symbol][tile_color]
        if tile_class in cls.tiles_needing_interactables:
            tile_args.append(interactable_list)

        if tile_symbol in cls.snake_head_symbols:
            tile = tile_class(topleft, *tile_args)
        else:
            tile = tile_class(topleft, size, *tile_args)

        if tile_id and tile_symbol not in cls.island_tiles_to_find:
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
            if symbol_parts[color_index] in cls.tile_args_map[symbol]:
                color = symbol_parts[color_index]
            else:
                id = symbol_parts[color_index]
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
    def is_explorable_island_tile(cls, tile_symbol):
        tile_symbol_index = 0
        symbol_parts = tile_symbol.split(cls.tile_data_delimiter)
        tile_symbol = symbol_parts[tile_symbol_index]
        return tile_symbol in cls.island_tiles_to_find
    


    @classmethod
    def is_snake_head_tile(cls, tile_symbol):
        return tile_symbol in cls.snake_head_symbols
    


    @classmethod
    def is_snake_segment_tile(cls, tile_symbol):
        return tile_symbol == cls.snake_segment_symbol



    @classmethod
    def is_static_tile(cls, tile):
        return tile.__class__ in cls.static_tiles
    


    @classmethod
    def is_dynamic_tile(cls, tile):
        return tile.__class__ in cls.dynamic_tiles
    


    @classmethod
    def is_wall_tile(cls, tile_symbol):
        tile_symbol_index = 0
        symbol_parts = tile_symbol.split(cls.tile_data_delimiter)
        tile_symbol = symbol_parts[tile_symbol_index]
        return tile_symbol == cls.wall_symbol
    


    @classmethod
    def is_player(cls, tile):
        if tile.__class__ != Snake:
            return False
        
        controller = tile.controller
        if controller.__class__ == PlayerController:
            return True
        
        return False