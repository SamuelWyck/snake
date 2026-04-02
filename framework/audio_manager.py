import pygame
import random



class AudioManager:
    def __init__(self, menu_music_path, game_music_path_list, sound_map, channel_map, save_file_path=None):
        self.menu_music_path = menu_music_path
        self.save_file_path = save_file_path

        self.game_music_path_list = game_music_path_list
        self.game_music_index = random.randint(0, len(self.game_music_path_list) - 1)

        self.music_end_event = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.music_end_event)

        self.sound_map = sound_map
        self.channel_map = channel_map

        self.precision = 3
        self.set_music_volume(.5)
        self.load_volume_settings()



    def play_menu_music_loop(self):
        if pygame.mixer.music.get_busy():
            return
        
        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.play(loops=-1)



    def stop_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()



    def play_game_music(self):
        track_file_path = self.game_music_path_list[self.game_music_index]

        pygame.mixer.music.load(track_file_path)
        pygame.mixer.music.play(fade_ms=1000)

        self.game_music_index += 1
        if self.game_music_index >= len(self.game_music_path_list):
            self.game_music_index = 0



    def pause_music(self):
        pygame.mixer.music.pause()



    def resume_music(self):
        pygame.mixer.music.unpause()


    
    def set_music_volume(self, volume):
        if volume < 0:
            volume = 0
        elif volume > 1:
            volume = 1

        volume = round(volume, self.precision)
        pygame.mixer.music.set_volume(volume)



    def get_music_volume(self):
        volume = pygame.mixer.music.get_volume()
        volume = round(volume, self.precision)
        return volume
    


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