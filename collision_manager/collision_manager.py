import pygame
from level_objects.dynamic_objects.pressure_plate.pressure_plate import PressurePlate
from level_objects.dynamic_objects.sticky_pressure_plate import StickyPressurePlate
from level_objects.agent_objects.box import Box
from level_objects.agent_objects.snake.snake import Snake
from level_objects.agent_objects.spike_ball import SpikeBall
from utils.color import Color



class CollisionManager:
    def __init__(self, play_area_size):
        width_index = 0
        height_index = 1
        self.pa_width = play_area_size[width_index]
        self.pa_height = play_area_size[height_index]
        self.pa_rect = pygame.rect.Rect((0, 0), play_area_size)
        self.compound_tiles = set([
            PressurePlate,
            StickyPressurePlate
        ])

    

    def check_collisions(self, player, level_object_fetcher):   
        static_tiles, dynamic_tiles, agents, interactables = level_object_fetcher()
        
        if player.just_moved():
            self.check_static_tiles(player, static_tiles)

            if not self.in_bounds(player.rect):
                ...

        self.check_dynamic_tiles(player, dynamic_tiles)
        self.check_agents(player, agents, static_tiles, dynamic_tiles)

        for agent in agents:
            self.check_agents(agent, agents, static_tiles, dynamic_tiles)
            self.check_dynamic_tiles(agent, dynamic_tiles)
            self.check_static_tiles(agent, static_tiles)
    


    def check_dynamic_tiles(self, collider, dynamic_tiles):
        for tile in dynamic_tiles:
            if tile.color == collider.color and tile.color != Color.NO_COLOR:
                continue
            if self.is_pressure_plate_tile(tile):
                for segment in tile.segments:
                    if collider.collide(segment.rect):
                        tile.hit_segments.add(segment)
            else:
                if collider.collide(tile.get_hitbox()):
                    ...



    def check_agents(self, collider, agents, static_tiles, dynamic_tiles):
        for agent in agents:
            if agent.color == collider.color and agent.color != Color.NO_COLOR:
                continue
            if agent == collider:
                continue
            if agent.__class__ == Box and collider.rect.colliderect(agent.rect):
                if collider.__class__ == Snake or collider.__class__ == SpikeBall:
                    agent.move(
                        collider, 
                        static_tiles, 
                        dynamic_tiles, 
                        agents, 
                        self.is_pressure_plate_tile,
                        self.in_bounds
                    )



    def check_static_tiles(self, collider, static_tiles):
        for tile in static_tiles:
            if collider.rect.colliderect(tile.rect):
                return True
        return False



    def is_pressure_plate_tile(self, tile):
        return tile.__class__ in self.compound_tiles
    


    def in_bounds(self, collider_rect):
        return self.pa_rect.contains(collider_rect)