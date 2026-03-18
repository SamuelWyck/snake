import pygame



class AudioManager:
    pygame.mixer.init()

    def __init__(self, menu_music_path, game_music_path_list, sound_map, channel_map):
        self.menu_music_path = menu_music_path
        self.game_music_path_list = game_music_path_list

        self.sound_map = sound_map
        self.channel_map = channel_map



    def play_menu_music_loop(self):
        if pygame.mixer.music.get_busy():
            return
        
        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.play(loops=-1)



    def stop_menu_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()