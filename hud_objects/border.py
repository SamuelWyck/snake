import pygame 



class Border:
    def __init__(self, topleft, size, width, images):
        border_width = size[0]
        border_height = size[1] - (width * 2)
        rect_width = width

        top_rect = pygame.rect.Rect(
            topleft, 
            (border_width, rect_width)
        )
        right_rect = pygame.rect.Rect(
            (topleft[0] + border_width - rect_width, topleft[1] + rect_width),
            (rect_width, border_height)
        )
        bottom_rect = pygame.rect.Rect(
            (topleft[0], topleft[1] + rect_width + border_height),
            (border_width, rect_width)
        )
        left_rect = pygame.rect.Rect(
            (topleft[0], topleft[1] + rect_width),
            (rect_width, border_height)
        )

        self.sides = [
            (top_rect, images[0]),
            (right_rect, images[1]),
            (bottom_rect, images[2]),
            (left_rect, images[3])
        ]
    


    def draw(self, surface):
        for side in self.sides:
            rect = side[0]
            image = side[1]
            if image == None:
                pygame.draw.rect(surface, (255, 0, 0), rect)
                continue
            surface.blit(image, rect.topleft)