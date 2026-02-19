import pygame
import sys
import time
from user_interface.elements.button import Button
from user_interface.elements.slider import Slider
from user_interface.elements.text_display import TextDisplay
from user_interface.elements.live_text_display import LiveTextDisplay


# menu elements will be in the form of either a slider object, a textdisplay object, 
# a live text display object, or a (btn object, btn callback) tuple. 
# ints can also be added to add an extra gap between objects
# cleanup_callback is used to do any clean up before menu exit. I.E. saving settings.

class GeneralMenu:
    def __init__(
        self, element_y_pos, element_gap, 
        background_img, mouse_manager, 
        screen_size, canvas_size, 
        cleanup_callback, *menu_elements
    ):
        self.screen_size = screen_size
        self.canvas_size = canvas_size

        self.background_img = background_img
        self.background_img_rect = self.get_background_img_rect()

        canvas_width, canvas_height = self.canvas_size
        menu_width, menu_height = self.background_img_rect.size
        self.fullscreen_menu = canvas_width == menu_width and canvas_height == menu_height

        self.mouse = mouse_manager
        self.cleanup_callback = cleanup_callback

        self.callback_map = {}
        self.menu_elements = self.parse_elements(menu_elements)
        self.position_elements(element_y_pos, element_gap)


    
    def parse_elements(self, menu_elements):
        btn_id = 0
        elements = []
        for element in menu_elements:
            if element.__class__ != tuple:
                elements.append(element)
                continue
                
            button, btn_callback = element
            button.id = btn_id
            self.callback_map[button.id] = btn_callback
            btn_id += 1
            elements.append(button)
        
        return elements
    


    def position_elements(self, start_y, gap):
        center_y = start_y
        canvas_width, _ = self.canvas_size
        center_x = canvas_width // 2

        for element in self.menu_elements:
            if element.__class__ == int:
                center_y += element
                continue

            ele_height = element.get_height()
            center_y += ele_height // 2
            element.set_center((center_x, center_y))
            center_y += (ele_height // 2) + gap

    

    def get_background_img_rect(self):
        rect = self.background_img.get_rect()
        canvas_width, canvas_height = self.canvas_size
        rect.centerx = canvas_width // 2
        rect.centery = canvas_height // 2
        return rect



    def cleanup(self):
        if self.cleanup_callback is None:
            return
        self.cleanup_callback()



    def run(self, framerate, canvas, screen):
        run = True
        clock = pygame.time.Clock()
        last_time = time.time()

        left_mouse_just_pressed = False
        left_mouse_just_released = False
        left_mouse_btn = 1

        backing = None
        if not self.fullscreen_menu:
            backing = canvas.copy()

        while run:
            delta_time = time.time() - last_time
            delta_time *= 60
            last_time = time.time()

            left_mouse_just_pressed = False
            left_mouse_just_released = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == left_mouse_btn:
                        left_mouse_just_pressed = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == left_mouse_btn:
                        left_mouse_just_released = True


            for element in self.menu_elements:
                if element.__class__ != Button:
                    continue
                if element.clicked:
                    element.clicked = False
                    btn_callback = self.callback_map[element.id]
                    exit_menu, info = btn_callback(framerate=framerate, canvas=canvas, screen=screen)
                    if exit_menu:
                        self.cleanup()
                        return info


            self.mouse.update()
            mouse_pos = self.mouse.get_pos()

            if not self.fullscreen_menu:
                canvas.blit(backing, (0, 0))
            canvas.blit(self.background_img, self.background_img_rect.topleft)

            for element in self.menu_elements:
                if element.__class__ == Button or element.__class__ == Slider:
                    element.update(canvas, mouse_pos, left_mouse_just_pressed, left_mouse_just_released)
                elif element.__class__ == TextDisplay or element.__class__ == LiveTextDisplay:
                    element.update(canvas)
            
            self.mouse.draw(canvas)

            screen.blit(pygame.transform.smoothscale(canvas, self.screen_size), (0, 0))
            pygame.display.update()
            clock.tick(framerate)