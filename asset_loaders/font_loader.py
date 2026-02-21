import pygame
import os



class Fonts:
    pygame.font.init()

    fonts_dir_path = "./assets/fonts"

    pickup_font = pygame.font.Font(os.path.join(fonts_dir_path, "pickupFont.ttf"), 34)
    pickup_outline_font = pygame.font.Font(os.path.join(fonts_dir_path, "pickupFont.ttf"), 40)
    goal_font = pygame.font.Font(os.path.join(fonts_dir_path, "goalFont.ttf"), 20)

    title_font = pygame.font.Font(os.path.join(fonts_dir_path, "pickupFont.ttf"), 120)
    menu_font = pygame.font.Font(os.path.join(fonts_dir_path, "pickupFont.ttf"), 48)
    level_win_font = pygame.font.Font(os.path.join(fonts_dir_path, "pickupFont.ttf"), 60)