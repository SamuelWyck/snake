from static_level_objects.wall import Wall



class TileConfig:
    tile_map = {
        "W": Wall
    }
    empty_symbol = "O"

    tiles_to_explore = set(["P"])
    tiles_to_link = {}



    @classmethod
    def get_tile(cls, topleft, size, tile_symbol):
        tile_symbol, tile_id = cls.get_id(tile_symbol)

        tile_class = cls.tile_map[tile_symbol]
        tile = tile_class(topleft, size)

        if tile_id and tile_id in cls.tiles_to_link:
            cls.tiles_to_link[tile_id].append(tile)
        elif tile_id:
            cls.tiles_to_link[tile_id] = [tile]

        return tile
    


    @classmethod
    def get_id(cls, tile_symbol):
        symbol_parts = tile_symbol.split("-")
        if len(symbol_parts) == 1:
            return tile_symbol, None
        return symbol_parts[0], symbol_parts[1]



    @classmethod
    def is_empty_space(cls, tile_symbol):
        return tile_symbol == cls.empty_symbol



    @classmethod
    def is_explorable_tile(cls, tile_symbol):
        tile_symbol = tile_symbol.split("-")[0]
        return tile_symbol in cls.tiles_to_explore
