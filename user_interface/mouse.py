import pygame



class Mouse:
    def __init__(self, canvas_size, display_size, mouse_img):
        pygame.mouse.set_relative_mode(True)

        width_index = 0
        height_index = 1
        self.canvas_width = canvas_size[width_index]
        self.canvas_height = canvas_size[height_index]
        self.display_width = display_size[width_index]
        self.display_height = display_size[height_index]

        self.image = mouse_img
        self.rect = self.image.get_rect()
        self.rect.topleft = self.get_start_pos()
        
        pygame.mouse.get_rel()
        self.sensitivity = 1


    def get_start_pos(self):
        position = pygame.mouse.get_pos()
        position = self.remap_point(position)
        return position


    def remap_point(self, point):
        x_index = 0
        y_index = 1

        remapped_x = round(pygame.math.remap(
            0, self.display_width,
            0, self.canvas_width,
            point[x_index]
        ))
        remapped_y = round(pygame.math.remap(
            0, self.display_height,
            0, self.canvas_height,
            point[y_index]
        ))

        return (remapped_x, remapped_y)


    def update(self):
        x_index = 0
        y_index = 1

        relative_movement = pygame.mouse.get_rel()
        relative_x = relative_movement[x_index]
        relative_y = relative_movement[y_index]

        remapped_movement = self.remap_point((relative_x, relative_y))
        relative_x = remapped_movement[x_index]
        relative_y = remapped_movement[y_index]

        relative_x *= self.sensitivity
        relative_y *= self.sensitivity

        self.rect.x += relative_x
        self.rect.y += relative_y

        self.clamp_pos()

    
    def clamp_pos(self):
        self.rect.x = pygame.math.clamp(self.rect.x, 0, self.canvas_width)
        self.rect.y = pygame.math.clamp(self.rect.y, 0, self.canvas_height)
        

    def get_pos(self):
        return tuple(self.rect.topleft)
    

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)