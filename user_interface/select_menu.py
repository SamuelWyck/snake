import pygame
import time
import sys


# click_callback should take the id of the button clicked and package it in a way that makes sense to return it.
# FOr example, (False, id) or (True, (False, id)) depending on how nested the menu is.


class SelectMenu:
    def __init__(
            self, start_y_pos, num_cols, num_rows, col_gap, row_gap, 
            background_img, screen_size, canvas_size, mouse_manager,
            page_up_btn, page_down_btn, click_callback, buttons
        ):
        self.canvas_size = canvas_size
        self.screen_size = screen_size
        
        self.background_image = background_img
        self.background_img_rect = self.background_image.get_rect()
        background_width, background_height = self.background_img_rect.size
        canvas_width, canvas_height = self.canvas_size
        self.background_img_rect.center = (canvas_width // 2, canvas_height // 2)
        self.fullscreen_background = background_width == canvas_width and background_height == canvas_height

        self.mouse = mouse_manager
        self.click_callback = click_callback

        self.btn_index_min = 0
        self.btn_index_max = num_cols * num_rows
        self.btn_index_change = num_cols * num_rows
        self.page_up_btn = page_up_btn
        self.page_down_btn = page_down_btn
        self.page_buttons = [self.page_up_btn, self.page_down_btn]

        self.buttons = buttons
        self.position_buttons(start_y_pos, num_rows, num_cols, col_gap, row_gap)


    
    def position_buttons(self, starting_y, num_rows, num_cols, col_gap, row_gap):
        max_width, max_height = self.get_max_btn_size()

        row_width = max_width * num_cols + (col_gap * (num_cols - 1))
        col_height = max_height * num_rows + (row_gap * (num_rows - 1))
        canvas_width, _ = self.canvas_size
        starting_x = canvas_width // 2 - row_width // 2

        self.position_page_buttons(starting_y, col_height, row_gap)
        
        btn_index = 0
        while btn_index < len(self.buttons):
            x_pos = starting_x
            y_pos = starting_y
            for _ in range(num_rows):

                for _ in range(num_cols):
                    center_x = x_pos + max_width // 2
                    center_y = y_pos + max_height // 2
                    button = self.buttons[btn_index]
                    button.id = btn_index
                    button.set_center((center_x, center_y))

                    x_pos += max_width + col_gap
                    btn_index += 1
                    if btn_index == len(self.buttons):
                        return
                    
                x_pos = starting_x
                y_pos += max_height + row_gap



    def position_page_buttons(self, starting_y, col_height, row_gap):
        canvas_width, _ = self.canvas_size

        up_btn_height = self.page_up_btn.get_height()
        up_btn_y_pos = starting_y - up_btn_height // 2 - row_gap
        up_btn_x_pos = canvas_width // 2
        self.page_up_btn.set_center((up_btn_x_pos, up_btn_y_pos))

        down_btn_height = self.page_down_btn.get_height()
        down_btn_y_pos = starting_y + col_height + row_gap + down_btn_height // 2
        down_btn_x_pos = canvas_width // 2
        self.page_down_btn.set_center((down_btn_x_pos, down_btn_y_pos))



    def get_max_btn_size(self):
        max_width = 0
        max_height = 0

        for button in self.buttons:
            width = button.get_width()
            height = button.get_height()
            max_width = max(max_width, width)
            max_height = max(max_height, height)
        
        return max_width, max_height
    


    def scroll_buttons(self, move_up):
        btn_index_change = self.btn_index_change if not move_up else -1 * self.btn_index_change

        self.btn_index_min += btn_index_change
        self.btn_index_max += btn_index_change

        if self.btn_index_min < 0 or self.btn_index_min >= len(self.buttons):
            self.btn_index_min -= btn_index_change
            self.btn_index_max -= btn_index_change



    def run(self, framerate, canvas, screen):
        backing_img = None
        if not self.fullscreen_background:
            backing_img = canvas.copy()

        run = True
        left_mouse_just_pressed = False
        left_mouse_just_released = False
        left_mouse_button = 1
        exit_parent_menu = True

        clock = pygame.time.Clock()
        last_time = time.time()

        while run:
            delta_time = time.time() - last_time
            delta_time *= 60
            last_time = time.time()

            left_mouse_just_pressed = False
            left_mouse_just_released = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == left_mouse_button:
                        left_mouse_just_pressed = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == left_mouse_button:
                        left_mouse_just_released = True
            
            for index in range(self.btn_index_min, self.btn_index_max):
                if index == len(self.buttons):
                    break
                button = self.buttons[index]
                if button.clicked:
                    button.clicked = False
                    return self.click_callback(button.id)
            
            for page_button in self.page_buttons:
                if page_button.clicked:
                    page_button.clicked = False
                    move_up = page_button == self.page_up_btn
                    self.scroll_buttons(move_up)
                
            
            self.mouse.update()
            mouse_pos = self.mouse.get_pos()
            
            if backing_img != None:
                canvas.blit(backing_img, (0, 0))
            canvas.blit(self.background_image, self.background_img_rect.topleft)

            for page_button in self.page_buttons:
                page_button.update(canvas, mouse_pos, left_mouse_just_pressed, left_mouse_just_released)
            for index in range(self.btn_index_min, self.btn_index_max):
                if index == len(self.buttons):
                    break
                button = self.buttons[index]
                button.update(canvas, mouse_pos, left_mouse_just_pressed, left_mouse_just_released)
            
            self.mouse.draw(canvas)
            
            screen.blit(pygame.transform.smoothscale(canvas, self.screen_size), (0, 0))
            pygame.display.update()
            clock.tick(framerate)