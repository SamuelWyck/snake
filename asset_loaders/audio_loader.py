import pygame
import os
from framework.sound_effect import SoundEffect



class Audio:
    pygame.mixer.init()


    music_path = "assets/music"
    sound_path = "assets/sounds"

    menu_music_path = os.path.join(music_path, "menu_music.ogg")

    game_music_paths = [
        os.path.join(music_path, "game_track_0.ogg"),
        os.path.join(music_path, "game_track_1.ogg"),
        os.path.join(music_path, "game_track_2.ogg"),
        os.path.join(music_path, "game_track_3.ogg"),
        os.path.join(music_path, "game_track_4.ogg"),
        os.path.join(music_path, "game_track_5.ogg"),
        os.path.join(music_path, "game_track_6.ogg"),
        os.path.join(music_path, "game_track_7.ogg")
    ]


    sounds_map = {
        "eat_pickup": pygame.mixer.Sound(os.path.join(sound_path, "eat.wav"))
    }

    channels_map = {
        "player": pygame.mixer.Channel(0)
    }



    @classmethod
    def get_sound_effect(cls, sound_key, channel_key):
        return SoundEffect(cls.sounds_map[sound_key], cls.channels_map[channel_key])