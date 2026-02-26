from user_interface.elements.menu_element import MenuElement


class ImageDisplay(MenuElement):
    def __init__(self, topleft, image):
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    
    def update(self, surface):
        surface.blit(self.image, self.rect.topleft)


    def change_image(self, image):
        self.image = image
        
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center



    # all following methods are definitions for methods declared in MenuElement class

    def get_height(self):
        return self.rect.height
    
    def get_width(self):
        return self.rect.width
    
    def set_center(self, center):
        self.rect.center = center

    def get_center(self):
        return self.rect.center
    
    def set_topleft(self, topleft):
        self.rect.topleft = topleft

    def get_topleft(self):
        return self.rect.topleft
    
    def set_x(self, new_x):
        self.rect.x = new_x

    def set_y(self, new_y):
        self.rect.y = new_y
