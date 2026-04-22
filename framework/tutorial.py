from user_interface.elements.text_display import TextDisplay



class Tutorial:
    def __init__(self, topleft, level_tutorial_map, font, color, wrap_length=0):
        self.tutorials_map = self.build_tutorial_displays(topleft, level_tutorial_map, font, color, wrap_length)


    def build_tutorial_displays(self, topleft, level_tutorials, font, color, wrap_length):
        tutorials_map = {}

        for level_num in level_tutorials:
            text_display = TextDisplay(topleft, font, color, level_tutorials[level_num], wrap_length=wrap_length)
            tutorials_map[level_num] = text_display

        return tutorials_map
    

    def draw(self, surface, level_num):
        if level_num not in self.tutorials_map:
            return 
        
        text_display = self.tutorials_map[level_num]
        text_display.update(surface)