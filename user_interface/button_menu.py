import pygame
import time
import sys


# title_text_display will be a TextDisplay object
# buttons_with_callbacks will be tuples in the form (Button object, button_callback)


class ButtonMenu:
    def __init__(
            self, buttons_topleft, button_gap, 
            background_img, screen_size, canvas_size, 
            mouse_manager, buttons_with_callbacks, title_text_display=None
        ):
        self.screen_width, self.screen_height = screen_size
        self.canvas_width, self.canvas_height = canvas_size

        self.background_image = background_img

        self.title_text_display = title_text_display
        if self.title_text_display != None:
            self.title_text_display.set_topleft(self.get_title_topleft())

        self.mouse = mouse_manager

        self.buttons = [] 
        self.callback_map = {}
        self.parse_buttons(buttons_with_callbacks)
        self.position_buttons(buttons_topleft, button_gap)
    


    def get_title_topleft(self):
        x_pos = (self.canvas_width // 2) - (self.title_text_display.get_width() // 2)
        y_pos = self.canvas_height // 10
        return (x_pos, y_pos)



    def parse_buttons(self, buttons_with_callbacks):
        for i in range(len(buttons_with_callbacks)):
            button, callback = buttons_with_callbacks[i]
            button.id = i
            self.callback_map[button.id] = callback
            self.buttons.append(button)


    
    def position_buttons(self, topleft, gap):
        x_pos, y_pos = topleft
        for button in self.buttons:
            button.set_topleft((x_pos, y_pos))
            button_height = button.get_height()
            y_pos += (gap + button_height)



    def run(self, framerate, canvas, screen):
        run = True
        last_time = time.time()
        clock = pygame.time.Clock()

        mouse_btn_just_pressed = False
        mouse_btn_just_released = False
        left_mouse_btn = 1

        while run:
            delta_time = time.time() - last_time
            delta_time *= 60
            last_time = time.time()

            mouse_btn_just_pressed = False
            mouse_btn_just_released = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == left_mouse_btn:
                        mouse_btn_just_pressed = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == left_mouse_btn:
                        mouse_btn_just_released = True
            
            for button in self.buttons:
                if button.clicked:
                    button.clicked = False
                    callback = self.callback_map[button.id]
                    exit_menu, info = callback(canvas=canvas, screen=screen, framerate=framerate)
                    if exit_menu:
                        return info
            
            self.mouse.update()
            mouse_position = self.mouse.get_pos()

            canvas.blit(self.background_image, (0, 0))
            
            if self.title_text_display != None:
                self.title_text_display.update(canvas)

            for button in self.buttons:
                button.update(canvas, mouse_position, mouse_btn_just_pressed, mouse_btn_just_released)

            self.mouse.draw(canvas)

            screen.blit(pygame.transform.smoothscale(canvas, (self.screen_width, self.screen_height)), (0, 0))
            pygame.display.update()
            clock.tick(framerate)