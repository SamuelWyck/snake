import pygame
import time
import sys



class SelectMenu:
    def __init__(
            self, start_y_pos, num_cols, num_rows, col_gap, row_gap, 
            background_img, screen_size, canvas_size, *buttons
        ):
        self.canvas_size = canvas_size
        self.screen_size = screen_size
        
        self.background_image = background_img

        self.btn_index_min = 0
        self.btn_index_max = num_cols * num_rows
        self.btn_index_change = num_cols

        self.buttons = buttons
        self.position_buttons(start_y_pos, num_rows, num_cols, col_gap, row_gap)


    
    def position_buttons(self, starting_y, num_rows, num_cols, col_gap, row_gap):
        max_width, max_height = self.get_max_btn_size()

        row_width = max_width * num_cols + (col_gap * (num_cols - 1))
        canvas_width, _ = self.canvas_size
        starting_x = canvas_width // 2 - row_width // 2
        
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



    def get_max_btn_size(self):
        max_width = 0
        max_height = 0

        for button in self.buttons:
            width = button.get_width()
            height = button.height()
            max_width = max(max_width, width)
            max_height = max(max_height, height)
        
        return max_width, max_height
    


    def run(self, framerate, canvas, screen):
        run = True

        left_mouse_just_pressed = False
        left_mouse_just_released = False
        left_mouse_button = 1

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
            
            