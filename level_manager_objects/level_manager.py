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
                
                tile = None
                tile_size = (
                    self.single_tile_size,
                    self.single_tile_size
                )

                if TileConfig.is_explore_tile(symbol):
                    ...
                else:
                    tile_topleft = (
                        self.single_tile_size * col,
                        self.single_tile_size * row
                    )
                    tile = TileConfig.get_tile(tile_topleft, tile_size, symbol)

                self.level_tiles.append(tile)
    


    def update(self, surface, delta_time):
        for tile in self.level_tiles:
            tile.update(surface, delta_time)

