import pygame 



class Border:
    def __init__(self, topleft, size, width, images):
        horizontal_img_index = 0
        vertical_img_index = 1
        width_index = 0
        height_index = 1
        x_index = 0
        y_index = 1

        x_coord = topleft[x_index]
        y_coord = topleft[y_index]

        border_width = size[width_index]
        border_height = size[height_index] - (width * 2)
        rect_width = width

        top_rect = pygame.rect.Rect(
            topleft, 
            (border_width, rect_width)
        )
        right_rect = pygame.rect.Rect(
            (x_coord + border_width - rect_width, y_coord + rect_width),
            (rect_width, border_height)
        )
        bottom_rect = pygame.rect.Rect(
            (x_coord, y_coord + rect_width + border_height),
            (border_width, rect_width)
        )
        left_rect = pygame.rect.Rect(
            (x_coord, y_coord + rect_width),
            (rect_width, border_height)
        )

        rects = [top_rect, right_rect, bottom_rect, left_rect]
        horizontal_img = images[horizontal_img_index]
        vertical_img = images[vertical_img_index]

        self.sides = []
        for i in range(len(rects)):
            image = horizontal_img if i % 2 == 0 else vertical_img
            self.sides.append(
                (rects[i], image)
            )
    


    def draw(self, surface):
        for side in self.sides:
            side_rect, side_image = side
            surface.blit(side_image, side_rect.topleft)