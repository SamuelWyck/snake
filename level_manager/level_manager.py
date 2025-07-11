import os
from level_manager.tile_config import TileConfig



class LevelManager:
    def __init__(self, level_size, single_tile_size):
        self.level_size = level_size
        self.single_tile_size = single_tile_size

        self.level_tiles = []
        self.dynamic_tiles = []
        self.static_tiles = []
        self.static_tile_map = {}

        self.level_files = [
            os.path.join("level_data_files", "level_1.txt")
        ]

        self.traversed_tile_positions = set()


    
    def load_level(self, level_num):
        level_index = level_num - 1
        file_path = self.level_files[level_index]

        level = self.read_level_file(file_path)
        self.parse_level_objects(level)
        TileConfig.link_tiles()



    def read_level_file(self, file_path):
        level = []
        with open(file_path, "r") as file:
            for line in file:
                level.append(line.split(TileConfig.tile_delimiter))
        
        return level



    def parse_level_objects(self, level):
        for row in range(len(level)):
            #the last col in each row is an unneeded newline character so subtract len by one to skip it
            for col in range(len(level[row]) - 1):
                symbol = level[row][col]
                if TileConfig.is_empty_space(symbol) or self.is_traversed_tile(row, col):
                    continue
                self.get_tile_object(row, col, symbol, level)
        
        self.traversed_tile_positions = set()


    
    def get_tile_object(self, row, col, symbol, level):
        tile_size = (
            self.single_tile_size,
            self.single_tile_size
        )
        topleft_positions = None

        if TileConfig.is_explorable_tile(symbol):
            topleft_positions = self.traverse_tiles(row, col, level, symbol)
        else:
            topleft_positions = self.calc_tile_topleft(row, col)

        tile = TileConfig.get_tile(topleft_positions, tile_size, symbol)
        self.store_tile(tile)

    

    def store_tile(self, tile):
        if TileConfig.is_static_tile(tile):
            self.static_tiles.append(tile)
            self.static_tile_map[tile.rect.center] = tile
        else:
            self.dynamic_tiles.append(tile)

    

    def traverse_tiles(self, row, col, level, symbol):
        topleft_positions = []
        self.traverse_tiles_rec(
            row, col, 
            level, symbol, 
            topleft_positions, set(),
            self.traversed_tile_positions
        )
        return topleft_positions
    


    def traverse_tiles_rec(self, row, col, level, symbol, topleft_positions, visited, explored_tiles):
        row_valid = 0 <= row < len(level)
        col_valid = 0 <= col < len(level[row]) - 1 #see line 43 to see reason for subtracting one
        if not row_valid or not col_valid:
            return
        key = (row, col)
        if key in visited:
            return
        visited.add(key)
        if level[row][col] != symbol:
            return
        if key in explored_tiles:
            return
        explored_tiles.add(key)
        
        topleft = self.calc_tile_topleft(row, col)
        topleft_positions.append(topleft)

        neighbors = [
            (row - 1, col), (row + 1, col),
            (row, col - 1), (row, col + 1)
        ]

        for neighbor in neighbors:
            if neighbor in visited or neighbor in explored_tiles:
                continue
            n_row = neighbor[0]
            n_col = neighbor[1]
            self.traverse_tiles_rec(n_row, n_col, level, symbol, topleft_positions, visited, explored_tiles)
            


    def calc_tile_topleft(self, row, col):
        return (
            self.single_tile_size * col,
            self.single_tile_size * row
        )



    def is_traversed_tile(self, row, col):
        return (row, col) in self.traversed_tile_positions
    


    def update(self, surface, delta_time):
        for tile in self.static_tiles:
            tile.update(surface, delta_time)
        
        for tile in self.dynamic_tiles:
            tile.update(surface, delta_time)
    


    def get_level_objects(self):
        return self.static_tile_map, self.dynamic_tiles