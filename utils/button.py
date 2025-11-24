class Button:
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