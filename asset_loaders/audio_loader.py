import pygame
import os



class Audio:

    music_path = "assets/music"

    menu_music_path = os.path.join(music_path, "menu_music.ogg")

    game_music_paths = [
        os.path.join(music_path, "game_track_0.ogg"),
        os.path.join(music_path, "game_track_1.ogg"),
        os.path.join(music_path, "game_track_2.ogg")
    ]