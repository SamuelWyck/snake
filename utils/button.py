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

    

    def update(self, surface, mouse_pos, mouse_btn_clicked):
        self.active_image = self.image
        self.active_rect = self.image_rect
        self.clicked = False

        mouse_hovering = False
        if self.active_rect.collidepoint(mouse_pos):
            mouse_hovering = True
            self.active_image = self.hover_image if self.hover_image != None else self.image
            self.active_rect = self.hover_image_rect if self.hover_image != None else self.image_rect
        
        if mouse_btn_clicked and mouse_hovering:
            self.clicked = True
        
        surface.blit(self.active_image, self.active_rect.topleft)