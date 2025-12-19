import os
from level_manager.tile_config import TileConfig



class LevelManager:
    def __init__(self, level_size, single_tile_size):
        self.level_size = level_size
        self.single_tile_size = single_tile_size

        self.dynamic_tiles = []
        self.static_tiles = []
        self.agent_tiles = []
        self.small_interactables = []
        self.player = None

        self.level_files = [
            {
                "level": os.path.join("level_data_files/level_1", "level_1.txt"),
                "agents": os.path.join("level_data_files/level_1", "agents_interactables_1.txt")
            }
        ]

        self.traversed_tile_positions = set()
        self.found_island_tiles = set()
        self.found_wall_tiles = set()
    


    def reset_level(self):
        for agent in self.agent_tiles:
            agent.reset()
        for tile in self.dynamic_tiles:
            if hasattr(tile, "reset"):
                tile.reset()
        for interactable in self.small_interactables:
            if not TileConfig.is_pickup(interactable):
                continue
            interactable.set_center_position(interactable.original_position)

        while self.player.eaten_pickups:
            pickup = self.player.eaten_pickups.pop()
            pickup.set_center_position(pickup.original_position)
            pickup.remove = False
            self.small_interactables.append(pickup)
        while self.player.pickups_to_drop:
            pickup = self.player.pickups_to_drop.pop()
            pickup.set_center_position(pickup.original_position)
            pickup.remove = False
            self.small_interactables.append(pickup)

        self.player.reset()


    
    def load_level(self, level_num):
        level_index = level_num - 1
        file_paths = self.level_files[level_index]

        level = self.read_file(file_paths["level"])
        self.parse_level_objects(level)
        TileConfig.link_tiles()

        agents = self.read_file(file_paths["agents"])
        self.parse_level_objects(agents)
        return self.player



    def read_file(self, file_path):
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
                TileConfig.is_snake_segment_tile(symbol)) or (
                self.is_found_island_tile(row, col)) or (self.is_found_wall_tile(row, col)):
                    continue
                self.get_tile_object(row, col, symbol, level)
        
        self.traversed_tile_positions = set()
        self.found_island_tiles = set()
        self.found_wall_tiles = set()


    
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
        elif TileConfig.is_wall_tile(symbol):
            topleft_positions, tile_size = self.explore_wall(row, col, level, symbol)
        else:
            topleft_positions = self.calc_tile_topleft(row, col)

        tile = TileConfig.get_tile(topleft_positions, tile_size, symbol, self.small_interactables)
        self.store_tile(tile)

    

    def store_tile(self, tile):
        if TileConfig.is_static_tile(tile):
            self.static_tiles.append(tile)
        elif TileConfig.is_dynamic_tile(tile):
            self.dynamic_tiles.append(tile)
        elif TileConfig.is_player(tile):
            self.player = tile
        elif TileConfig.is_interactable(tile):
            self.small_interactables.append(tile)
        else:
            self.agent_tiles.append(tile)

    

    def explore_wall(self, row, col, level, symbol):
        topleft = self.calc_tile_topleft(row, col)

        vertical_positions = []
        horizontal_postions = []
        vertical_pos_change = (1, 0)
        horizontal_pos_change = (0, 1)

        self.explore_wall_rec(row, col, level, symbol, vertical_pos_change, self.found_wall_tiles, set(), vertical_positions)
        self.explore_wall_rec(row, col, level, symbol, horizontal_pos_change, self.found_wall_tiles, set(), horizontal_postions)
        
        longer_direction = vertical_positions
        vertical_longer = True
        if len(horizontal_postions) > len(vertical_positions):
            longer_direction = horizontal_postions
            vertical_longer = False
        
        for pos in longer_direction:
            self.found_wall_tiles.add(pos)
        
        tile_size = (
            self.single_tile_size, 
            self.single_tile_size * len(longer_direction)
        ) if vertical_longer else (self.single_tile_size * len(longer_direction), self.single_tile_size)

        return topleft, tile_size


    
    def explore_wall_rec(self, row, col, level, target_symbol, pos_change, prev_visited, new_visited, found_tiles):
        row_valid = 0 <= row < len(level)
        col_valid = 0 <= col < len(level[0])
        key = (row, col)
        if not row_valid or not col_valid:
            return
        if key in prev_visited or key in new_visited:
            return
        symbol = level[row][col]
        if symbol != target_symbol:
            return
        
        new_visited.add(key)
        found_tiles.append(key)

        row_change_index = 0
        col_change_index = 1
        row_change = pos_change[row_change_index]
        col_change = pos_change[col_change_index]

        new_row = row + row_change
        new_col = col + col_change
        self.explore_wall_rec(new_row, new_col, level, target_symbol, pos_change, prev_visited, new_visited, found_tiles)



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
    


    def link_isolated_tiles(self, start_row, level, start_symbol):
        found_topleft_positions = []
        symbol_index = 0

        target_symbol, _, target_id = TileConfig.parse_spike_ball(start_symbol)
        for row in range(start_row, len(level)):
            for col in range(len(level[row])):
                tile_data = level[row][col]
                symbol_parts = tile_data.split(TileConfig.tile_data_delimiter)
                symbol = symbol_parts[symbol_index]
                if symbol != target_symbol:
                    continue
                symbol, _, id, order = TileConfig.parse_spike_ball(tile_data, include_order=True)
                if id != target_id:
                    continue

                self.found_island_tiles.add((row, col))
                topleft = self.calc_tile_topleft(row, col)
                found_topleft_positions.append((topleft, order))

        sorted_positions = self.merge_sort(found_topleft_positions)
        topleft_positions = []
        for data in sorted_positions:
            pos, order = data
            topleft_positions.append(pos)
        return topleft_positions
    


    def merge_sort(self, list):
        if len(list) <= 1:
            return list

        mid = len(list) // 2
        left = self.merge_sort(list[:mid])
        right = self.merge_sort(list[mid:])

        return self.merge(left, right)
    


    def merge(self, left, right):
        order_index = 1
        merged_list = []
        i = 0
        j = 0
        while i < len(left) or j < len(right):
            left_val = left[i] if i < len(left) else (None, float("inf"))
            right_val = right[j] if j < len(right) else (None, float("inf"))
            if float(left_val[order_index]) <= float(right_val[order_index]):
                merged_list.append(left_val)
                i += 1
            else:
                merged_list.append(right_val)
                j += 1
        
        return merged_list



    def is_traversed_tile(self, row, col):
        return (row, col) in self.traversed_tile_positions
    


    def is_found_island_tile(self, row, col):
        return (row, col) in self.found_island_tiles
    


    def is_found_wall_tile(self, row, col):
        return (row, col) in self.found_wall_tiles
    


    def update(self, surface, delta_time):
        for tile in self.dynamic_tiles:
            tile.update(surface, delta_time)

        remove = False
        for interactable in self.small_interactables:
            interactable.update(surface, delta_time)
            if interactable.remove:
                remove = True

        if remove:
            self.small_interactables[:] = [item for item in self.small_interactables if not item.remove]

        for tile in self.static_tiles:
            tile.update(surface, delta_time)

        for tile in self.agent_tiles:
            tile.update(surface, delta_time)



    def get_level_objects(self):
        return self.static_tiles, self.dynamic_tiles, self.agent_tiles, self.small_interactables