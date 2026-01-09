import pygame
import time
import sys
from framework.user_interface.button import Button
from utils.color import Color
from asset_loaders.font_loader import Fonts


# Btn_imgs_with_callbacks will be a list of tuples. If the tuple is length 2 the first item is a btn image and the 
# second is the btn's callback. If the tuple is length 3 the first two items withh be btn imgs (hover and non-hover)
# and the third item will be the callback. 
# The callback is expected to return a tuple of length 2. The first item being a bool indicating if the menu should exit.
# The second item will be some information that the callback wants passed along.


class Menu:
    def __init__(self, btn_imgs_with_callbacks, background_img, screen_size, canvas_size, mouse_manager, btns_topleft, title):
        self.screen_width, self.screen_height = screen_size
        self.canvas_width, self.canvas_height = canvas_size
        self.btns_start_x, self.btns_start_y = btns_topleft

        self.background_image = background_img
        self.title_img = Fonts.title_font.render(title, True, Color.GREEN)
        self.title_rect = self.title_img.get_rect()
        self.title_rect.topleft = self.get_title_topleft()

        self.mouse = mouse_manager

        self.buttons, self.callback_map = self.build_buttons(btn_imgs_with_callbacks)
    


    def get_title_topleft(self):
        x_pos = (self.canvas_width // 2) - (self.title_rect.width // 2)
        y_pos = self.canvas_height // 10
        return (x_pos, y_pos)



    def build_buttons(self, btn_imgs_with_callbacks):
        button_list = []
        callback_map = {}

        button_spacing = 20
        total_btns_height = self.btns_start_y
        for index in range(len(btn_imgs_with_callbacks)):
            btn_info = btn_imgs_with_callbacks[index]
            btn_img, btn_hover_img, btn_callback = self.unpack_button_info(btn_info)

            img_height = btn_img.get_rect().height
            hover_img_height = btn_hover_img.get_rect().height if btn_hover_img != None else 0
            max_image_height = max(img_height, hover_img_height)

            btn_topleft = self.get_button_topleft(total_btns_height, img_height, max_image_height)
            total_btns_height += max_image_height
            total_btns_height += button_spacing

            button = Button(btn_topleft, btn_img, btn_hover_img, id=index)
            button_list.append(button)
            callback_map[index] = btn_callback
        
        return button_list, callback_map

    

    def unpack_button_info(self, button_info):
        img_index = 0 
        hover_img_index = 1
        callback_index = 2

        if len(button_info) == 2:
            callback_index = 1
            return button_info[img_index], None, button_info[callback_index]
        
        return button_info[img_index], button_info[hover_img_index], button_info[callback_index]



    def get_button_topleft(self, total_btns_height, image_height, max_image_height):
        y_position = total_btns_height
        height_difference = max_image_height - image_height
        y_position += height_difference // 2
        return (self.btns_start_x, y_position)



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
            canvas.blit(self.title_img, self.title_rect.topleft)

            for button in self.buttons:
                button.update(canvas, mouse_position, mouse_btn_just_pressed, mouse_btn_just_released)

            self.mouse.draw(canvas)

            screen.blit(pygame.transform.smoothscale(canvas, (self.screen_width, self.screen_height)), (0, 0))
            pygame.display.update()

            clock.tick(framerate)