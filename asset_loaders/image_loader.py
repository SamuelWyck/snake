import pygame
import os



class Images:

    tile_images_path = "assets/images/tile_images"


    #tile images
    wall_img = pygame.image.load(os.path.join(tile_images_path, "wall.png")).convert_alpha()
    door_img = pygame.image.load(os.path.join(tile_images_path, "door.png")).convert_alpha()
    pressure_plate_img = pygame.image.load(os.path.join(tile_images_path, "pressure_plate.png")).convert_alpha()
    pressure_plate_pressed_img = pygame.image.load(os.path.join(tile_images_path, "pressure_plate_pressed.png")).convert_alpha()
    box_img = pygame.image.load(os.path.join(tile_images_path, "box.png")).convert_alpha()