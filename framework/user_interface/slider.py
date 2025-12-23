import pygame



class Slider:
    def __init__(self, topleft, size, callback, slide_bar_color, slide_color, border_radius=0):
        self.slide_bar_color = slide_bar_color
        self.slide_color = slide_color
        self.border_radius = border_radius

        self.callback = callback
        self.mouse_btn_pressed = False
        self.value_precision = 4 # round slider value to 4 decimal places

        self.slide_bar = pygame.rect.Rect(topleft, size)
        self.side_padding = self.slide_bar.height * .1 # Padding to keep a uniform gap at edge of slide
        self.bar_left_end = self.slide_bar.x + self.side_padding
        self.bar_right_end = self.slide_bar.x + self.slide_bar.width - self.side_padding

        slide_width = self.slide_bar.height * .8 # Ensure slide is smaller than the slide bar
        self.slide = pygame.rect.Rect((0, 0), (slide_width, slide_width))
        self.slide.centery = self.slide_bar.centery
        self.slide.centerx = self.slide_bar.x + (self.slide_bar.width // 2)

    

    def update(self, surface, mouse_pos, mouse_btn_pressed, mouse_btn_released):
        hovering = self.slide.collidepoint(mouse_pos)
        if hovering and mouse_btn_pressed:
            self.mouse_btn_pressed = True
        elif mouse_btn_released:
            self.mouse_btn_pressed = False
        
        if self.mouse_btn_pressed:
            mouse_x, _ = mouse_pos
            self.move_slide(mouse_x)
            self.callback(self.value)
        
        pygame.draw.rect(surface, self.slide_bar_color, self.slide_bar, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.slide_color, self.slide, border_radius=self.border_radius)
    


    def move_slide(self, mouse_x):
        self.slide.centerx = mouse_x
        if self.slide.x < self.bar_left_end:
            self.slide.x = self.bar_left_end
        elif self.slide.x + self.slide.width > self.bar_right_end:
            self.slide.x = self.bar_right_end - self.slide.width



    def set_value(self, value):
        value = round(value, self.value_precision)
        corrected_right_end = self.bar_right_end - self.slide.width

        slide_x = value * (corrected_right_end - self.bar_left_end) + self.bar_left_end
        slide_centerx = slide_x + (self.slide.width // 2)
        self.move_slide(slide_centerx)
        

    
    @property
    def value(self):
        corrected_right_end = self.bar_right_end - self.slide.width
        slider_val = (self.slide.x - self.bar_left_end) / (corrected_right_end - self.bar_left_end)
        return round(slider_val, self.value_precision)