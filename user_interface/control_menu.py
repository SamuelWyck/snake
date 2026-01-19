import pygame
import time
import sys
from user_interface.elements.button import Button
from user_interface.elements.text_display import TextDisplay
from utils.color import Color



class ControlMenu:
    def __init__(
            self, y_pos, num_rows, row_gap, col_gap,
            controls_map, background_img, font, 
            color, hover_color, canvas_size, screen_size, 
            mouse_manager, save_callback
        ):
        self.canvas_size = canvas_size
        self.screen_size = screen_size

        self.row_gap = row_gap
        self.col_gap = col_gap
        self.row_height = 0

        self.background_img = background_img
        self.font = font
        self.color = color
        self.hover_color = hover_color

        self.mouse = mouse_manager
        self.controls_map = controls_map
        self.save_callback = save_callback
        self.exit_info = (False, None)

        self.display_index_min = 0
        self.display_index_max = num_rows
        self.starting_display_index_max = num_rows


        self.back_btn = Button(
            topleft=(0, 0),
            image=self.font.render("BACK", antialias=True, color=self.color),
            hover_image=self.font.render("BACK", antialias=True, color=self.hover_color)
        )
        self.page_up_btn = Button(
            topleft=(0, 0), 
            image=self.font.render("PAGE UP", antialias=True, color=self.color),
            hover_image=self.font.render("PAGE UP", antialias=True, color=self.hover_color)
        )
        self.page_down_btn = Button(
            topleft=(0, 0), 
            image=self.font.render("PAGE DOWN", antialias=True, color=self.color),
            hover_image=self.font.render("PAGE DOWN", antialias=True, color=self.hover_color)
        )
        self.page_buttons = [self.page_up_btn, self.page_down_btn]

        self.control_displays = []
        max_label_width, max_btn_width = self.build_control_displays()
        self.position_control_displays(y_pos, row_gap, col_gap, max_label_width, max_btn_width)
        col_height = (self.row_height * num_rows) + (row_gap * (num_rows - 1))
        self.position_nav_buttons(y_pos, col_height, row_gap, col_gap)
        self.create_title_display()
        self.create_editing_popup()
        self.create_error_msgs()



    def get_key_name(self, key):
        key_name = pygame.key.name(key)
        if key_name == "":
            key_name = f"m{key}"
        return key_name



    
    def build_control_displays(self):
        max_label_width = 0
        max_btn_width = 0
        max_row_height = 0
        for control_name in self.controls_map:
            control_label = TextDisplay(topleft=(0, 0), font=self.font, color=self.color, text=control_name)
            key_name = self.get_key_name(self.controls_map[control_name])
            control_btn = Button(
                topleft=(0, 0), 
                image=self.font.render(key_name, antialias=True, color=self.color),
                hover_image=self.font.render(key_name, antialias=True, color=self.hover_color),
                id=control_name
            )
            self.control_displays.append((control_label, control_btn))

            max_label_width = max(max_label_width, control_label.get_width())
            max_btn_width = max(max_btn_width, control_btn.get_width())
            max_row_height = max(max_row_height, control_btn.get_height(), control_label.get_height())
        
        self.row_height = max_row_height
        return max_label_width, max_btn_width



    def position_control_displays(self, starting_y, row_gap, col_gap, label_width, max_btn_width):
        canvas_width, _ = self.canvas_size
        y_pos = starting_y
        label_x_pos = (canvas_width//2) - label_width - (col_gap//2)
        btn_x_pos = (canvas_width//2) + (col_gap//2) + max_btn_width//2
        for control_display in self.control_displays:
            label, button = control_display
            label.set_topleft((label_x_pos, y_pos))
            button.set_center((btn_x_pos, y_pos + self.row_height//2))

            y_pos += self.row_height + row_gap
        
        return y_pos
    


    def position_nav_buttons(self, y_pos, col_height, row_gap, col_gap):
        canvas_width, canvas_height = self.canvas_size
        center_x = canvas_width//2
        
        page_up_center_y = y_pos - self.page_up_btn.get_height()//2 - row_gap
        self.page_up_btn.set_center((center_x, page_up_center_y))

        page_down_center_y = y_pos + col_height + row_gap + self.page_down_btn.get_height()//2
        self.page_down_btn.set_center((center_x, page_down_center_y))

        self.back_btn.set_center(
            (self.back_btn.get_width()//2 + col_gap, canvas_height - self.back_btn.get_height() - row_gap)
        )

    

    def create_title_display(self):
        self.title_display = TextDisplay(
            topleft=(0, 0), font=self.font, color=self.color, text="SELECT A KEYBIND TO EDIT"
        )
        canvas_width, _ = self.canvas_size
        _, page_up_btn_y = self.page_up_btn.get_topleft()
        title_height = self.title_display.get_height()
        y_pos = page_up_btn_y - ((2*self.row_gap) + title_height//2)
        self.title_display.set_center((canvas_width//2, y_pos))

    

    def create_editing_popup(self):
        self.input_msg = TextDisplay(
            topleft=(0, 0), font=self.font, color=self.color, text="ENTER INPUT"
        )
        self.cancel_msg = TextDisplay(
            topleft=(0, 0), font=self.font, color=self.color, text="PRESS ESC TO CANCEL"
        )

        width = max(self.input_msg.get_width(), self.cancel_msg.get_width())
        height = self.input_msg.get_height() + self.row_gap + self.cancel_msg.get_height()

        border_width = 10
        popup_size = (width + (border_width * 2.5), height + (border_width * 2.5))
        self.popup_background = pygame.Surface(popup_size)
        self.popup_background.fill(Color.BLACK)
        border_rect = pygame.rect.Rect((0, 0), popup_size)

        pygame.draw.rect(self.popup_background, self.color, border_rect, width=border_width//2)

        self.popup_rect = self.popup_background.get_rect()
        canvas_width, canvas_height = self.canvas_size
        self.popup_rect.center = (canvas_width//2, canvas_height//2)

        input_center_y = canvas_height//2 - self.row_gap//2 - self.input_msg.get_height()//2
        self.input_msg.set_center((canvas_width//2, input_center_y))
        cancel_center_y = canvas_height//2 + self.row_gap//2 + self.cancel_msg.get_height()//2
        self.cancel_msg.set_center((canvas_width//2, cancel_center_y))


    
    def create_error_msgs(self):
        self.error_msg = TextDisplay(
            topleft=(0, 0), font=self.font, color=self.color, text="ERROR"
        )
        self.error_explaination_msg = TextDisplay(
            topleft=(0, 0), font=self.font, color=self.color, text="DUPLICATE KEYBINDS"
        )
        
        canvas_width, canvas_height = self.canvas_size
        error_msg_center_y = canvas_height//2 - self.row_gap//2 - self.error_msg.get_height()//2
        self.error_msg.set_center((canvas_width//2, error_msg_center_y))
        
        explaination_msg_center_y = canvas_height//2 + self.row_gap//2 + self.error_explaination_msg.get_height()//2
        self.error_explaination_msg.set_center((canvas_width//2, explaination_msg_center_y))



    def draw_edit_popup(self, surface):
        surface.blit(self.popup_background, self.popup_rect.topleft)
        self.input_msg.update(surface)
        self.cancel_msg.update(surface)



    def draw_error_popup(self, surface):
        surface.blit(self.popup_background, self.popup_rect.topleft)
        self.error_msg.update(surface)
        self.error_explaination_msg.update(surface)



    def save(self):
        self.display_index_min = 0
        self.display_index_max = self.starting_display_index_max
        self.save_callback(self.controls_map)

    

    def key_conflicts(self):
        seen_keys = set()
        for control_name in self.controls_map:
            key = self.controls_map[control_name]
            if key in seen_keys:
                return True
            seen_keys.add(key)
        return False

    

    def update_keybinds(self, old_button, key):
        control_name = old_button.id
        self.controls_map[control_name] = key

        key_name = self.get_key_name(key)

        new_button = Button(
            topleft=(0, 0), 
            image=self.font.render(key_name, antialias=True, color=self.color), 
            hover_image=self.font.render(key_name, antialias=True, color=self.hover_color),
            id=old_button.id
        )
        new_button.set_topleft(old_button.get_topleft())

        # remove old_button from list and calc new max_btn_width
        max_btn_width = 0
        for idx in range(len(self.control_displays)):
            display = self.control_displays[idx]
            control_label, control_btn = display
            if control_btn == old_button:
                self.control_displays[idx] = (control_label, new_button)
                control_btn = new_button
            max_btn_width = max(control_btn.get_width(), max_btn_width)

        # shift btns on x axis to reflect possible new max_btn_width
        canvas_width, _ = self.canvas_size
        btn_center_x = canvas_width//2 + self.col_gap//2 + max_btn_width//2
        for display in self.control_displays:
            _, control_btn = display    
            _, btn_center_y = control_btn.get_center()
            control_btn.set_center((btn_center_x, btn_center_y))



    def scroll_displays(self, move_down):
        index_change = 1 if move_down else -1
        
        self.display_index_min += index_change
        self.display_index_max += index_change
        if self.display_index_min < 0 or self.display_index_max > len(self.control_displays):
            self.display_index_min += index_change * -1
            self.display_index_max += index_change * -1
            return

        
        height_change = self.row_height + self.row_gap
        height_change = height_change * -1 if move_down else height_change
        for display in self.control_displays:
            label, button = display
            _, label_y = label.get_topleft()
            label.set_y(label_y + height_change)

            _, button_y = button.get_topleft()
            button.set_y(button_y + height_change)



    def run(self, framerate, canvas, screen):
        clock = pygame.time.Clock()
        last_time = time.time()

        left_mouse_just_pressed = False
        left_mouse_just_released = False
        editing_keybind = False
        keybind_button = None
        keybind_errors = False
        run = True
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
                    if event.button == pygame.BUTTON_LEFT:
                        left_mouse_just_pressed = True
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        left_mouse_just_released = True
                        keybind_errors = False
                    if editing_keybind:
                        editing_keybind = False
                        self.update_keybinds(keybind_button, event.button)
                        keybind_button = None

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE and editing_keybind:
                        editing_keybind = False
                        keybind_button = None
                    elif editing_keybind:
                        editing_keybind = False
                        self.update_keybinds(keybind_button, event.key)
                        keybind_button = None
            

            self.mouse.update()
            mouse_pos = self.mouse.get_pos()

            if not editing_keybind and not keybind_errors:
                for index in range(self.display_index_min, self.display_index_max):
                    display = self.control_displays[index]
                    _, button = display
                    if button.clicked:
                        button.clicked = False
                        keybind_button = button
                        editing_keybind = True

                for button in self.page_buttons:
                    if button.clicked:
                        button.clicked = False
                        move_down = button == self.page_down_btn
                        self.scroll_displays(move_down)

                if self.back_btn.clicked:
                    self.back_btn.clicked = False
                    conflicts = self.key_conflicts()
                    if not conflicts:
                        self.save()
                        return self.exit_info
                    else:
                        keybind_errors = True
            

            canvas.blit(self.background_img, (0, 0))

            self.title_display.update(canvas)

            for index in range(self.display_index_min, self.display_index_max):
                display = self.control_displays[index]
                label, button = display
                label.update(canvas)
                button.update(canvas, mouse_pos, left_mouse_just_pressed, left_mouse_just_released)

            for button in self.page_buttons:
                button.update(canvas, mouse_pos, left_mouse_just_pressed, left_mouse_just_released)
            self.back_btn.update(canvas, mouse_pos, left_mouse_just_pressed, left_mouse_just_released)

            if editing_keybind:
                self.draw_edit_popup(canvas)
            if keybind_errors:
                self.draw_error_popup(canvas)
            
            self.mouse.draw(canvas)

            screen.blit(pygame.transform.smoothscale(canvas, self.screen_size), (0, 0))
            pygame.display.update()
            clock.tick(framerate)