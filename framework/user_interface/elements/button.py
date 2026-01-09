from framework.user_interface.elements.menu_element import MenuElement



class Button(MenuElement):
    def __init__(self, topleft, image, hover_image=None, id=None):
        self.image = image
        self.image_rect = image.get_rect()
        self.image_rect.topleft = topleft

        self.hover_image = hover_image
        self.hover_image_rect = self.hover_image.get_rect() if self.hover_image != None else None
        if self.hover_image_rect != None:
            self.hover_image_rect.center = self.image_rect.center

        self.active_image = self.image
        self.active_rect = self.image_rect

        self.id = id
        self.clicked = False
        self.mouse_button_pressed = False

    

    def update(self, surface, mouse_pos, mouse_btn_pressed, mouse_btn_released):
        self.active_image = self.image
        self.active_rect = self.image_rect
        self.clicked = False

        mouse_hovering = False
        if self.active_rect.collidepoint(mouse_pos):
            mouse_hovering = True
            self.active_image = self.hover_image if self.hover_image != None else self.image
            self.active_rect = self.hover_image_rect if self.hover_image != None else self.image_rect
        
        if mouse_btn_pressed and mouse_hovering:
            self.mouse_button_pressed = True
        elif mouse_btn_released and mouse_hovering and self.mouse_button_pressed:
            self.mouse_button_pressed = False
            self.clicked = True
        elif mouse_btn_released:
            self.mouse_button_pressed = False
        
        surface.blit(self.active_image, self.active_rect.topleft)
    

    # all following methods are definitions for methods declared in MenuElement class

    def set_center(self, center):
        self.image_rect.center = center
        if self.hover_image_rect != None:
            self.hover_image_rect.center = center
    
    def get_center(self):
        return self.image_rect.center
    
    def get_height(self):
        max_height = self.image_rect.height
        if self.hover_image_rect != None:
            max_height = max(max_height, self.hover_image_rect.height)
        return max_height
    
    def get_width(self):
        max_height = self.image_rect.height
        if self.hover_image_rect != None:
            max_height = max(max_height, self.hover_image_rect.height)
        return max_height

    def set_topleft(self, topleft):
        self.image_rect.topleft = topleft
        if self.hover_image_rect != None:
            self.hover_image_rect.center = self.image_rect.center
    
    def get_topleft(self):
        return self.image_rect.topleft
    
    def set_x(self, new_x):
        self.image_rect.x = new_x
        if self.hover_image_rect != None:
            self.hover_image_rect.center = self.image_rect.center
    
    def set_y(self, new_y):
        self.image_rect.y = new_y
        if self.hover_image_rect != None:
            self.hover_image_rect.center = self.image_rect.center