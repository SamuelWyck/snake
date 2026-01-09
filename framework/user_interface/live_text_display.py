from framework.user_interface.menu_element import MenuElement


# object_ref is the object to pull the live text from. 
# text_getter is a callback that understands how to get the text from the object_ref. 
# for example: text_getter() will must reutrn the text to be rendered

class LiveTextDisplay(MenuElement):
    def __init__(self, topleft, font, color, object_ref, text_getter):
        self.topleft = topleft
        self.center = None
        self.font = font
        self.color = color

        self.text_getter = text_getter
        self.object_ref = object_ref

        self.rendered_text = None
        self.text_rect = None
        self.update_text()


    def update_text(self):
        text = self.text_getter(self.object_ref)
        self.rendered_text = self.font.render(text, antialias=True, color=self.color)
        self.text_rect = self.rendered_text.get_rect()
        self.text_rect.topleft = self.topleft
        if self.center != None:
            self.text_rect.center = self.center


    def set_center(self, center):
        self.center = center

    
    def unset_center(self):
        self.center = None

    
    def update(self, surface):
        self.update_text()
        surface.blit(self.rendered_text, self.text_rect.topleft)

    
    # all following methods are definitions for methods declared in MenuElement class
    
    def get_center(self):
        return self.center
    
    def get_height(self):
        return self.text_rect.height
    
    def get_width(self):
        return self.text_rect.width

    def set_topleft(self, topleft):
        self.topleft = topleft
        self.unset_center()
    
    def get_topleft(self):
        return self.text_rect.topleft
    
    def set_x(self, new_x):
        _, old_y = self.topleft
        self.topleft = (new_x, old_y)
        self.unset_center()
    
    def set_y(self, new_y):
        old_x, _ = self.topleft
        self.topleft = (old_x, new_y)
        self.unset_center()