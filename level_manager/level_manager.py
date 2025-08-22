import os
from level_manager.tile_config import TileConfig



class LevelManager:
    def __init__(self, level_size, single_tile_size):
        self.level_size = level_size
        self.single_tile_size = single_tile_size

        self.dynamic_tiles = []
        self.static_tiles = []
        self.static_tile_map = {}
        self.agent_tiles = []
        self.player = None

        self.level_files = [
            os.path.join("level_data_files", "level_1.txt")
        ]

        self.traversed_tile_positions = set()
        self.found_island_tiles = set()


    
    def load_level(self, level_num):
        level_index = level_num - 1
        file_path = self.level_files[level_index]

        level = self.read_level_file(file_path)
        self.parse_level_objects(level)
        TileConfig.link_tiles()
        return self.player



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
                if TileConfig.is_empty_space(symbol) or (
                self.is_traversed_tile(row, col)) or (
                TileConfig.is_snake_segment_tile(symbol)) or (self.is_found_island_tile(row, col)):
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
        elif TileConfig.is_explorable_island_tile(symbol):
            topleft_positions = self.link_isolated_tiles(row, level, symbol)
        elif TileConfig.is_snake_head_tile(symbol):
            topleft_positions = self.get_snake_positions(row, col, level)
        else:
            topleft_positions = self.calc_tile_topleft(row, col)

        tile = TileConfig.get_tile(topleft_positions, tile_size, symbol)
        self.store_tile(tile)

    

    def store_tile(self, tile):
        if TileConfig.is_static_tile(tile):
            self.static_tiles.append(tile)
            self.static_tile_map[tile.rect.center] = tile
        elif TileConfig.is_dynamic_tile(tile):
            self.dynamic_tiles.append(tile)
        elif TileConfig.is_player(tile):
            self.player = tile
        else:
            self.agent_tiles.append(tile)



    def get_snake_positions(self, row, col, level):
        starting_row, starting_col = self.get_first_snake_seg_pos(row, col, level)

        topleft_positions = self.traverse_tiles(starting_row, starting_col, level, TileConfig.snake_segment_symbol)

        head_position = self.calc_tile_topleft(row, col)
        topleft_positions.insert(0, head_position)

        return topleft_positions


    
    def get_first_snake_seg_pos(self, row, col, level):
        neighbors = [
            (row - 1, col), (row + 1, col),
            (row, col - 1), (row, col + 1)
        ]

        for neighbor in neighbors:
            n_row, n_col = neighbor

            row_valid = 0 <= n_row < len(level)
            col_valid = 0 <= n_col < len(level[0])
            if not row_valid or not col_valid:
                continue

            symbol = level[n_row][n_col]
            if symbol == TileConfig.snake_segment_symbol:
                return n_row, n_col
        
        return None

    

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
        #the last col in each row is an unneeded newline character so subtract len by one to ignore it
        col_valid = 0 <= col < len(level[row]) - 1
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
    


    def link_isolated_tiles(self, start_row, level, target_symbol):
        found_topleft_positions = []
        for row in range(start_row, len(level)):
            for col in range(len(level[row])):
                symbol = level[row][col]
                if symbol != target_symbol:
                    continue
                
                self.found_island_tiles.add((row, col))
                topleft = self.calc_tile_topleft(row, col)
                found_topleft_positions.append(topleft)

        return found_topleft_positions



    def is_traversed_tile(self, row, col):
        return (row, col) in self.traversed_tile_positions
    


    def is_found_island_tile(self, row, col):
        return (row, col) in self.found_island_tiles
    


    def update(self, surface, delta_time):
        for tile in self.static_tiles:
            tile.update(surface, delta_time)
        
        for tile in self.dynamic_tiles:
            tile.update(surface, delta_time)

        for tile in self.agent_tiles:
            tile.update(surface, delta_time)
    


    def get_level_objects(self):
        return self.static_tile_map, self.dynamic_tiles, self.agent_tiles