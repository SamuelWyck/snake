import pygame
from copy import deepcopy
from static_level_objects.wall import Wall



class TileConfig:

    init_topleft = (0, 0)
    init_size = (0, 0)

    tile_map = {
        "W": Wall(init_topleft, init_size)
    }


    @classmethod
    def get_tile(cls, topleft, size, tile_symbol):
        tile = deepcopy(cls.tile_map[tile_symbol])
        tile.set_topleft(topleft)
        tile.set_size(size)

        return tile

