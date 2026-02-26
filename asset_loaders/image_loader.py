import pygame
import os



class Images:
    static_tile_images_path = "assets/images/static_tile_images"
    dynamic_tile_images_path = "assets/images/dynamic_tile_images"
    agent_images_path = "assets/images/agent_images"
    interactables_images_path = "assets/images/interactables_images"
    other_images_path = "assets/images/other_images"
    menu_images_path = "assets/images/menu_images"


    # static tile images
    goal_img = pygame.image.load(os.path.join(static_tile_images_path, "goal.png")).convert_alpha()
    cannon_img = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_0.png")).convert_alpha()
    cannon_img_0 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_0.png")).convert_alpha()
    cannon_img_1 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_1.png")).convert_alpha()
    cannon_img_2 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_2.png")).convert_alpha()
    cannon_img_3 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_3.png")).convert_alpha()
    cannon_img_4 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_4.png")).convert_alpha()
    cannon_img_5 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_5.png")).convert_alpha()
    cannon_img_6 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_6.png")).convert_alpha()
    cannon_img_7 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_7.png")).convert_alpha()
    cannon_img_8 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_8.png")).convert_alpha()
    cannon_img_9 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_9.png")).convert_alpha()
    cannon_img_10 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_10.png")).convert_alpha()
    cannon_img_11 = pygame.image.load(os.path.join(static_tile_images_path, "cannon_frames/cannon_fr_11.png")).convert_alpha()
    smoke_img_0 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_0.png")).convert_alpha()
    smoke_img_1 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_1.png")).convert_alpha()
    smoke_img_2 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_2.png")).convert_alpha()
    smoke_img_3 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_3.png")).convert_alpha()
    smoke_img_4 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_4.png")).convert_alpha()
    smoke_img_5 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_5.png")).convert_alpha()
    smoke_img_6 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_6.png")).convert_alpha()
    smoke_img_7 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_7.png")).convert_alpha()
    smoke_img_8 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_8.png")).convert_alpha()
    smoke_img_9 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_9.png")).convert_alpha()
    smoke_img_10 = pygame.image.load(os.path.join(static_tile_images_path, "smoke_frames/smoke_fr_10.png")).convert_alpha()



    # dynamic tile images
    door_img_1 = pygame.image.load(os.path.join(dynamic_tile_images_path, "door_frames/door_frame_1.png")).convert_alpha()
    door_img_2 = pygame.image.load(os.path.join(dynamic_tile_images_path, "door_frames/door_frame_2.png")).convert_alpha()
    door_img_3 = pygame.image.load(os.path.join(dynamic_tile_images_path, "door_frames/door_frame_3.png")).convert_alpha()
    lava_img = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/lava.png")).convert_alpha()
    bubble_img_0 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_0.png")).convert_alpha()
    bubble_img_1 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_1.png")).convert_alpha()
    bubble_img_2 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_2.png")).convert_alpha()
    bubble_img_3 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_3.png")).convert_alpha()
    bubble_img_4 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_4.png")).convert_alpha()
    bubble_img_5 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_5.png")).convert_alpha()
    bubble_img_6 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_6.png")).convert_alpha()
    bubble_img_7 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_7.png")).convert_alpha()
    bubble_img_8 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_8.png")).convert_alpha()
    bubble_img_9 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_9.png")).convert_alpha()
    bubble_img_10 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_10.png")).convert_alpha()
    bubble_img_11 = pygame.image.load(os.path.join(dynamic_tile_images_path, "acid_frames/bubble_frame_11.png")).convert_alpha()
    pressure_plate_img = pygame.image.load(os.path.join(dynamic_tile_images_path, "pressure_plate.png")).convert_alpha()
    pressure_plate_pressed_img = pygame.image.load(os.path.join(dynamic_tile_images_path, "pressure_plate_pressed.png")).convert_alpha()
    s_pressure_plate_img = pygame.image.load(os.path.join(dynamic_tile_images_path, "pressure_plate_s.png")).convert_alpha()
    s_pressure_plate_pressed_img = pygame.image.load(os.path.join(dynamic_tile_images_path, "pressure_plate_s_pressed.png")).convert_alpha()

    # agent images
    box_img = pygame.image.load(os.path.join(agent_images_path, "box.png")).convert_alpha()
    spike_ball_fg_img = pygame.image.load(os.path.join(agent_images_path, "spike_ball_foreground.png")).convert_alpha()
    spike_ball_bg_img = pygame.image.load(os.path.join(agent_images_path, "spike_ball_background.png")).convert_alpha()
    snake_head_img = pygame.image.load(os.path.join(agent_images_path, "snake_head.png")).convert_alpha()
    snake_eyes_img = pygame.image.load(os.path.join(agent_images_path, "snake_eyes.png")).convert_alpha()
    laser_base_img = pygame.image.load(os.path.join(agent_images_path, "laser.png")).convert_alpha()
    moveable_laser_img = pygame.image.load(os.path.join(agent_images_path, "laser_moveable.png")).convert_alpha()
    laser_barrel_img = pygame.image.load(os.path.join(agent_images_path, "laser_barrel.png")).convert_alpha()
    laser_switch_img = pygame.image.load(os.path.join(static_tile_images_path, "laser_switch.png")).convert_alpha()
    moveable_mirror_img = pygame.image.load(os.path.join(agent_images_path, "mirror_moveable.png")).convert_alpha()
    mirror_color_img = pygame.image.load(os.path.join(agent_images_path, "mirror_color.png")).convert_alpha()
    mirror_img = pygame.image.load(os.path.join(agent_images_path, "mirror.png")).convert_alpha()


    # other images
    bullet_img = pygame.image.load(os.path.join(interactables_images_path, "bullet.png")).convert_alpha()
    background_img = pygame.image.load(os.path.join(other_images_path, "background.png")).convert_alpha()
    canvas_background_img = pygame.image.load(os.path.join(other_images_path, "canvas_background.png")).convert_alpha()
    wall_texture_img = pygame.image.load(os.path.join(other_images_path, "wall_texture.png")).convert_alpha()
    horizontal_border_img = pygame.image.load(os.path.join(other_images_path, "horizontal_border.png")).convert()
    vertical_border_img = pygame.image.load(os.path.join(other_images_path, "vertical_border.png")).convert_alpha()
    mouse_img = pygame.image.load(os.path.join(other_images_path, "mouse.png")).convert_alpha()
    length_display = pygame.image.load(os.path.join(other_images_path, "length_display_bg.png")).convert_alpha()
    eaten_pickups_border = pygame.image.load(os.path.join(other_images_path, "pickups_border.png")).convert_alpha()

    # menu images
    main_menu_bg_img = pygame.image.load(os.path.join(menu_images_path, "main_menu_bg.png")).convert_alpha()
    settings_menu_bg_img = pygame.image.load(os.path.join(menu_images_path, "settings_menu_bg.png")).convert_alpha()
    audio_menu_bg_img = pygame.image.load(os.path.join(menu_images_path, "audio_menu_bg.png")).convert_alpha()
    mouse_menu_bg_img = pygame.image.load(os.path.join(menu_images_path, "mouse_menu_bg.png")).convert_alpha()
    controls_menu_bg_img = pygame.image.load(os.path.join(menu_images_path, "controls_menu_bg.png")).convert_alpha()
    pause_bg_img = pygame.image.load(os.path.join(menu_images_path, "pause_bg.png")).convert_alpha()
    level_menu_bg_img = pygame.image.load(os.path.join(menu_images_path, "level_menu_bg.png")).convert_alpha()

    sound_effects_title_img = pygame.image.load(os.path.join(menu_images_path, "sound_effects_title.png")).convert_alpha()
    music_title_img = pygame.image.load(os.path.join(menu_images_path, "music_title.png")).convert_alpha()
    sensitivity_title = pygame.image.load(os.path.join(menu_images_path, "sensitivity_title.png")).convert_alpha()

    slider_bar_img = pygame.image.load(os.path.join(menu_images_path, "slider_bar.png")).convert_alpha()
    slider_slide_img = pygame.image.load(os.path.join(menu_images_path, "slider_slide.png")).convert_alpha()

    play_btn_img = pygame.image.load(os.path.join(menu_images_path, "play_btn.png")).convert_alpha()
    play_btn_hvr_img = pygame.image.load(os.path.join(menu_images_path, "play_btn_hover.png")).convert_alpha()
    settings_btn_img = pygame.image.load(os.path.join(menu_images_path, "settings_btn.png")).convert_alpha()
    settings_btn_hvr_img = pygame.image.load(os.path.join(menu_images_path, "settings_btn_hover.png")).convert_alpha()
    exit_btn_img = pygame.image.load(os.path.join(menu_images_path, "exit_btn.png")).convert_alpha()
    exit_btn_hvr_img = pygame.image.load(os.path.join(menu_images_path, "exit_btn_hover.png")).convert_alpha()
    audio_btn_img = pygame.image.load(os.path.join(menu_images_path, "audio_btn.png")).convert_alpha()
    audio_btn_hvr_img = pygame.image.load(os.path.join(menu_images_path, "audio_btn_hover.png")).convert_alpha()
    controls_btn_img = pygame.image.load(os.path.join(menu_images_path, "controls_btn.png")).convert_alpha()
    controls_btn_hvr_img = pygame.image.load(os.path.join(menu_images_path, "controls_btn_hover.png")).convert_alpha()
    mouse_btn_img = pygame.image.load(os.path.join(menu_images_path, "mouse_btn.png")).convert_alpha()
    mouse_btn_hvr_img = pygame.image.load(os.path.join(menu_images_path, "mouse_btn_hover.png")).convert_alpha()
    back_btn_img = pygame.image.load(os.path.join(menu_images_path, "back_btn.png")).convert_alpha()
    back_btn_hvr_img = pygame.image.load(os.path.join(menu_images_path, "back_btn_hover.png")).convert_alpha()