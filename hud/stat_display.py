class StatDisplay:
    def __init__(self, topleft, stat_gap, title, font, color, outline_width=0, outline_color=None):
        self.topleft = topleft
        self.stat_gap = stat_gap
        self.font = font
        
        self.color = color
        self.outline_width = outline_width
        self.outline_color = outline_color

        self.title_image = self.get_image(title)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.topleft = self.topleft

        self.stat_image = None
        self.stat_rect = None
        self.update_stat(0)



    def get_image(self, text):
        image = None

        if self.outline_color == None:
            image = self.font.render(text, antialias=True, color=self.color)
        else:
            self.font.outline = self.outline_width
            title_outline_img = self.font.render(text, antialias=True, color=self.outline_color)
            self.font.outline = 0

            title_img = self.font.render(text, antialias=True, color=self.color)
            title_outline_img.blit(title_img, (self.outline_width, self.outline_width))
            image = title_outline_img

        return image
    


    def update_stat(self, number):
        num_str = str(number)
        self.stat_image = self.get_image(num_str)

        self.stat_rect = self.stat_image.get_rect()

        self.stat_rect.y = self.title_rect.y
        self.stat_rect.x = self.title_rect.x + self.title_rect.width + self.stat_gap



    def update(self, surface):
        surface.blit(self.title_image, self.title_rect.topleft)
        surface.blit(self.stat_image, self.stat_rect.topleft)