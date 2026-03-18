import pygame



class AudioManager:
    pygame.mixer.init()

    def __init__(self, menu_music_path, game_music_path_list, sound_map, channel_map, save_file_path=None):
        self.menu_music_path = menu_music_path
        self.save_file_path = save_file_path

        self.game_music_path_list = game_music_path_list

        self.sound_map = sound_map
        self.channel_map = channel_map


        self.set_music_volume(.5)
        self.load_volume_settings()



    def play_menu_music_loop(self):
        if pygame.mixer.music.get_busy():
            return
        
        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.play(loops=-1)



    def stop_menu_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()


    
    def set_music_volume(self, volume):
        if volume < 0:
            volume = 0
        elif volume > 1:
            volume = 1

        pygame.mixer.music.set_volume(volume)



    def get_music_volume(self):
        return pygame.mixer.music.get_volume()
    


    def save_volume_settings(self):
        if self.save_file_path == None:
            return
        
        try:
            music_volume = str(self.get_music_volume())
            with open(self.save_file_path, "w") as file:
                file.write(music_volume)
        except:
            pass

    

    def load_volume_settings(self):
        if self.save_file_path == None:
            return
        
        try:
            music_volume = None
            with open(self.save_file_path, "r") as file:
                volume_info = file.readline()
                music_volume = float(volume_info)

            self.set_music_volume(music_volume)
        except:
            pass