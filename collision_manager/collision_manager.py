import pygame



class CollisionManager:
    def __init__(self, play_area_size):
        width_index = 0
        height_index = 1
        self.pa_width = play_area_size[width_index]
        self.pa_height = play_area_size[height_index]

    

    def check_collisions(self, player, level_object_fetcher):   
        static_tile_map, dynamic_tiles = level_object_fetcher()
        
        if player.just_moved():
            if player.rect.center in static_tile_map:
                tile = static_tile_map[player.rect.center]
                if tile.collide(player):
                    ...
            
            if player.body_collide():
                ...