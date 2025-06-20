import pygame



class Snake_Segment:
    def __init__(self, size, center, joint_width, joint_side, color, life_span):
        self.rect = pygame.rect.Rect((0, 0), (size, size))
        self.rect.center = center

        #extend rect in the direction needed to cover joint gap
        self.grow(joint_width, joint_side)


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

    

    def grow(self, growth_amount, growth_direction):
        if growth_direction == "top":
            self.rect.height += growth_amount
            self.rect.centery -= growth_amount
        elif growth_direction == "right":
            self.rect.width += growth_amount
        elif growth_direction == "bottom":
            self.rect.height += growth_amount
        elif growth_direction == "left":
            self.rect.width += growth_amount
            self.rect.centerx -= growth_amount