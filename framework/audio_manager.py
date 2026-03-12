import pygame
import os



class AudioManager:
    pygame.mixer.init()

    menu_music_path = os.path.join("assets/music/", "menu_music.ogg")



    @classmethod
    def play_menu_music_loop(cls):
        if pygame.mixer.music.get_busy():
            return
        
        pygame.mixer.music.load(cls.menu_music_path)
        pygame.mixer.music.play(loops=-1)



    @classmethod
    def stop_menu_music(cls):
        pygame.mixer.music.stop()