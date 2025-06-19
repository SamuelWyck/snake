import pygame



class Snake_Segment:
    def __init__(self, size, center, color, life_span):
        self.rect = pygame.rect.Rect((0, 0), (size, size))
        self.rect.center = center

        self.life_span = life_span
        self.color = color

        self.remove = False
    


    def update(self, surface, delta_time):
        if not self.remove:
            self.draw(surface)
            life_span_change = 1 * delta_time
            self.life_span -= life_span_change
            if self.life_span <= 0:
                self.remove = True
    


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)