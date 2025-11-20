import pygame
import os



class Fonts:
    pygame.font.init()

    fonts_dir_path = "./assets/fonts"

    pickup_font = pygame.font.Font(os.path.join(fonts_dir_path, "pickupFont.ttf"), 34)
    pickup_outline_font = pygame.font.Font(os.path.join(fonts_dir_path, "pickupFont.ttf"), 40)
    goal_font = pygame.font.Font(os.path.join(fonts_dir_path, "goalFont.ttf"), 20)
    # goal_font = pygame.font.Font(os.path.join(fonts_dir_path, "pickupFont.ttf"), 25)