from hud.border import Border



class Hud:
    def __init__(self, pa_topleft, pa_size):
        border_width = 30
        self.border = Border(
            topleft=(pa_topleft[0] - border_width, pa_topleft[1] - border_width),
            size=(pa_size[0] + (2 * border_width), pa_size[1] + (2 * border_width)),
            width=border_width,
            images=[None, None, None, None]
        )
    


    def draw(self, surface):
        self.border.draw(surface)