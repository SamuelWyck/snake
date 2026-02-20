import pygame
from level_objects.dynamic_objects.pressure_plate.pressure_plate import PressurePlate
from level_objects.dynamic_objects.sticky_pressure_plate import StickyPressurePlate
from level_objects.agent_objects.box import Box
from level_objects.agent_objects.snake.snake import Snake
from level_objects.agent_objects.spike_ball import SpikeBall
from level_objects.dynamic_objects.lava import Lava
from level_objects.static_objects.goal import Goal
from level_objects.agent_objects.laser_cannon import LaserCannon
from level_objects.agent_objects.mirror import Mirror
from level_objects.interactables.pickup import Pickup
from utils.color import Color
from level_objects.interactables.bullet import Bullet
from level_objects.interactables.laser import Laser



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
        static_tiles, dynamic_tiles, agents, interactables, lasers, laser_switches = level_object_fetcher()

        if player.just_moved():
            if self.check_static_tiles(player, static_tiles):
                return True

            if not self.in_bounds(player.rect):
                return True

        if self.check_dynamic_tiles(player, dynamic_tiles):
            return True
        if self.check_agents(player, agents, static_tiles, dynamic_tiles):
            return True

        for agent in agents:
            if self.check_agents(agent, agents, static_tiles, dynamic_tiles):
                return True
            if self.check_dynamic_tiles(agent, dynamic_tiles):
                return True
            if self.check_static_tiles(agent, static_tiles):
                return True
        
        if self.check_interactables(interactables, player, static_tiles, dynamic_tiles, agents, lasers, laser_switches):
            return True

        if len(player.pickups_to_drop) != 0:
            pickup = player.pickups_to_drop.pop()
            interactables.append(pickup)

        return False
    


    def check_dynamic_tiles(self, collider, dynamic_tiles):
        for tile in dynamic_tiles:
            if tile.__class__ == Goal:
                if collider.__class__ == Snake and tile.collide(collider):
                    ... # handle win
                continue
            if tile.color == collider.color and tile.color != Color.NO_COLOR:
                continue
            if self.is_pressure_plate_tile(tile):
                for segment in tile.segments:
                    if collider.collide(segment.rect):
                        tile.hit_segments.add(segment)
            else:
                if collider.__class__ == Snake and collider.collide(tile.get_hitbox()):
                    return True
        return False



    def check_agents(self, collider, agents, static_tiles, dynamic_tiles):
        for agent in agents:
            if agent.color == collider.color and agent.color != Color.NO_COLOR:
                if agent.__class__ != LaserCannon and collider.__class__ == Snake:
                    continue
            if agent == collider:
                continue
            if agent.__class__ == Box or agent.__class__ == LaserCannon or agent.__class__ == Mirror:
                if collider.__class__ == Snake and collider.rect.colliderect(agent.rect) and not agent.move(
                        collider, static_tiles, dynamic_tiles, agents, self.is_box_skippable, self.in_bounds
                    ):
                        return True
                elif collider.__class__ == Snake and collider.color != Color.NO_COLOR and collider.collide(agent.rect):
                    return True
            elif agent.__class__ == SpikeBall and collider.__class__ == Snake:
                if collider.collide(agent.rect):
                    return True
            if collider.__class__ == SpikeBall and agent.rect.colliderect(collider.rect):
                collider.reverse_direction()
        return False



    def check_static_tiles(self, collider, static_tiles):
        for tile in static_tiles:
            if collider.rect.colliderect(tile.rect):
                return True
        return False



    def check_interactables(self, interactables, player, static_tiles, dynamic_tiles, agents, lasers, laser_switches):
        for interactable in interactables:
            if interactable.remove:
                continue
            if interactable.__class__ == Pickup:
                if interactable.collide(player) and player.eat_pickup(interactable):
                    interactable.remove = True
                continue
            if not self.in_bounds(interactable.rect):
                if interactable.__class__ == Bullet:
                    interactable.dead = True
                    continue
            if interactable.__class__ == Bullet and player.collide(interactable.rect):
                interactable.dead = True
                return True
            elif interactable.__class__ == Laser:
                player.collide_laser(interactable)
            
            for tile in static_tiles:
                if interactable.__class__ == Bullet and tile == interactable.parent:
                    continue
                if interactable.__class__ == Bullet and interactable.rect.colliderect(tile.rect):
                    interactable.dead = True
                    break
                elif interactable.__class__ == Laser and interactable.rect.colliderect(tile.rect):
                    interactable.shorten_laser(tile.rect)
            
            for agent in agents:
                if not interactable.rect.colliderect(agent.rect):
                    continue
                if interactable.__class__ == Bullet:
                    interactable.dead = True
                    continue
                elif interactable.__class__ == Laser:
                    interactable.shorten_laser(agent.rect)

            for tile in dynamic_tiles:
                if tile.__class__ == Goal:
                    continue
                if tile.__class__ == Lava or self.is_pressure_plate_tile(tile):
                    continue
                if tile.collide(interactable.rect):
                    if interactable.__class__ == Bullet:
                        interactable.dead = True
                        break
                    elif interactable.__class__ == Laser:
                        interactable.shorten_laser(tile.rect)
        
        for laser in lasers:
            for laser_switch in laser_switches:
                laser_switch.test_laser(laser)

        return False



    def is_pressure_plate_tile(self, tile):
        return tile.__class__ in self.compound_tiles
    


    def is_box_skippable(self, tile):
        return tile.__class__ in self.compound_tiles or tile.__class__ == Lava or tile.__class__ == Goal
    


    def in_bounds(self, collider_rect):
        return self.pa_rect.contains(collider_rect)