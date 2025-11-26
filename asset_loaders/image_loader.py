import pygame
import os



class Images:
    static_tile_images_path = "assets/images/static_tile_images"
    dynamic_tile_images_path = "assets/images/dynamic_tile_images"
    agent_images_path = "assets/images/agent_images"
    interactables_images_path = "assets/images/interactables_images"
    other_images_path = "assets/images/other_images"


    # static tile images
    goal_img = pygame.image.load(os.path.join(static_tile_images_path, "goal.png")).convert_alpha()



    # dynamic tile images
    door_img_1 = pygame.image.load(os.path.join(dynamic_tile_images_path, "door_frame_1.png")).convert_alpha()
    door_img_2 = pygame.image.load(os.path.join(dynamic_tile_images_path, "door_frame_2.png")).convert_alpha()
    door_img_3 = pygame.image.load(os.path.join(dynamic_tile_images_path, "door_frame_3.png")).convert_alpha()
    pressure_plate_img = pygame.image.load(os.path.join(dynamic_tile_images_path, "pressure_plate.png")).convert_alpha()
    pressure_plate_pressed_img = pygame.image.load(os.path.join(dynamic_tile_images_path, "pressure_plate_pressed.png")).convert_alpha()
    lava_img = pygame.image.load(os.path.join(dynamic_tile_images_path, "lava.png")).convert_alpha()

    # agent images
    box_img = pygame.image.load(os.path.join(agent_images_path, "box.png")).convert_alpha()
    spike_ball_fg_img = pygame.image.load(os.path.join(agent_images_path, "spike_ball_foreground.png")).convert_alpha()
    spike_ball_bg_img = pygame.image.load(os.path.join(agent_images_path, "spike_ball_background.png")).convert_alpha()
    snake_head_img = pygame.image.load(os.path.join(agent_images_path, "snake_head.png")).convert_alpha()
    snake_eyes_img = pygame.image.load(os.path.join(agent_images_path, "snake_eyes.png")).convert_alpha()

    # other images
    bullet_img = pygame.image.load(os.path.join(interactables_images_path, "bullet.png")).convert_alpha()
    background_img = pygame.image.load(os.path.join(other_images_path, "background.png")).convert_alpha()
    wall_texture_img = pygame.image.load(os.path.join(other_images_path, "wall_texture.png")).convert_alpha()
    horizontal_border_img = pygame.image.load(os.path.join(other_images_path, "horizontal_border.png")).convert()
    vertical_border_img = pygame.image.load(os.path.join(other_images_path, "vertical_border.png")).convert_alpha()
    mouse_img = pygame.image.load(os.path.join(other_images_path, "mouse.png")).convert_alpha()