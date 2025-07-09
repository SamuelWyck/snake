import pygame
import os
from level_manager_objects.tile_config import TileConfig



class LevelManager:
    def __init__(self, level_size, single_tile_size):
        self.level_size = level_size
        self.single_tile_size = single_tile_size

        self.level_tiles = []

        self.level_files = [
            os.path.join("level_data_files", "level_1.txt")
        ]


    
    def load_level(self, level_num):
        level_index = level_num - 1
        file_path = self.level_files[level_index]

        level = self.read_level_file(file_path)
        self.parse_level_objects(level)



    def read_level_file(self, file_path):
        level = []
        with open(file_path, "r") as file:
            for line in file:
                level.append(line.split(","))
        
        return level



    def parse_level_objects(self, level):
        for row in range(len(level)):
            for col in range(len(level[0]) - 1):
                symbol = level[row][col]
                if TileConfig.is_empty_space(symbol):
                    continue
                self.get_tile_object(row, col, symbol, level)


    
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
        self.level_tiles.append(tile)

    

    def traverse_tiles(self, row, col, level, symbol):
        topleft_positions = []
        self.traverse_tiles_rec(
            row, col, 
            level, symbol, 
            topleft_positions, set()
        )
        return topleft_positions
    


    def traverse_tiles_rec(self, row, col, level, symbol, topleft_positions, visited):
        row_valid = 0 <= row < len(level)
        col_valid = 0 <= col < len(level[0]) - 1
        if not row_valid or not col_valid:
            return
        key = (row, col)
        if key in visited:
            return
        visited.add(key)
        if level[row][col] != symbol:
            return
        
        topleft = self.calc_tile_topleft(row, col)
        topleft_positions.append(topleft)

        neighbors = [
            (row - 1, col), (row + 1, col),
            (row, col - 1), (row, col + 1)
        ]

        for neighbor in neighbors:
            if neighbor in visited:
                continue
            nr = neighbor[0]
            nc = neighbor[1]
            self.traverse_tiles_rec(nr, nc, level, symbol, topleft_positions, visited)
            


    def calc_tile_topleft(self, row, col):
        return (
            self.single_tile_size * col,
            self.single_tile_size * row
        )
    


    def update(self, surface, delta_time):
        for tile in self.level_tiles:
            tile.update(surface, delta_time)

