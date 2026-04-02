


class SoundEffect:
    def __init__(self, sound, channel):
        self.sound = sound
        self.channel = channel

        self.played = False

    
    def hard_play(self):
        self.channel.play(self.sound)


    def soft_play(self):
        if not self.channel.get_busy():
            self.channel.play(self.sound)

    
    def play_once(self):
        if not self.played:
            self.channel.play(self.sound)
            self.played = True