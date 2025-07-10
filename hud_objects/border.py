import pygame 



class Border:
    def __init__(self, topleft, size, width, images):
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

        self.sides = []
        for i in range(len(rects)):
            self.sides.append(
                (rects[i], images[i])
            )

        self.color = (255, 0, 0)
    


    def draw(self, surface):
        for side in self.sides:
            side_rect, side_image = side
            if not side_image:
                pygame.draw.rect(surface, self.color, side_rect)
                continue
            surface.blit(side_image, side_rect.topleft)