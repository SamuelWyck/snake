from static_level_objects.wall import Wall



class TileConfig:
    tile_map = {
        "W": Wall
    }
    empty_symbol = "O"

    tiles_to_explore = set(["L"])



    @classmethod
    def get_tile(cls, topleft, size, tile_symbol):
        tile_class = cls.tile_map[tile_symbol]
        tile = tile_class(topleft, size)

        return tile



    @classmethod
    def is_empty_space(cls, tile_symbol):
        return tile_symbol == cls.empty_symbol



    @classmethod
    def is_explore_tile(cls, tile_symbol):
        return tile_symbol in cls.tiles_to_explore
