from framework.user_interface.menu_element import MenuElement



class TextDisplay(MenuElement):
    def __init__(self, topleft, font, color, text):
        self.font = font
        self.color = color
        self.text = text

        self.rendered_text = self.font.render(self.text, antialias=True, color=self.color)
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.topleft = topleft

    
    def update(self, surface):
        surface.blit(self.rendered_text, self.text_rect.topleft)


    def change_text(self, new_text):
        self.text = new_text
        self.rendered_text = self.font.render(self.text, antialias=True, color=self.color)
        old_topleft = self.text_rect.topleft
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.topleft = old_topleft

    
    # all following methods are definitions for methods declared in MenuElement class

    def set_center(self, center):
        self.text_rect.center = center
    
    def get_center(self):
        return self.text_rect.center
    
    def get_height(self):
        return self.text_rect.height
    
    def get_width(self):
        return self.text_rect.width

    def set_topleft(self, topleft):
        self.text_rect.topleft = topleft
    
    def get_topleft(self):
        return self.text_rect.topleft
    
    def set_x(self, new_x):
        self.text_rect.x = new_x
    
    def set_y(self, new_y):
        self.text_rect.y = new_y