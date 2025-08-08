import pygame



class SnakeSegment:
    def __init__(self, size, center, joint_width, joint_side):
        self.rect = pygame.rect.Rect((0, 0), size)
        self.rect.center = center

        #keep track of the back-middle of the segment
        self.back_pos = self.get_back_pos(joint_side)

        #extend rect in the direction needed to cover joint gap
        self.grow(joint_width, joint_side)

        self.remove = False

    

    def get_back_pos(self, joint_side):
        x_coord = 0
        y_coord = 1

        if joint_side == "top":
            back_pos = list(self.rect.midbottom)
            back_pos[y_coord] -= self.rect.width//2
        elif joint_side == "bottom":
            back_pos = list(self.rect.midtop)
            back_pos[y_coord] += self.rect.width//2
        elif joint_side == "left": 
            back_pos = list(self.rect.midright)
            back_pos[x_coord] -= self.rect.height//2
        else:
            back_pos = list(self.rect.midleft)
            back_pos[x_coord] += self.rect.height//2
        
        return back_pos
    


    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.rect)

    

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
    


    def shrink(self, shrink_amount, next_segment_direction):
        if next_segment_direction == "top":
            self.rect.height -= shrink_amount
        elif next_segment_direction == "right":
            self.rect.width -= shrink_amount
            self.rect.centerx += shrink_amount
        elif next_segment_direction == "bottom":
            self.rect.height -= shrink_amount
            self.rect.centery += shrink_amount
        elif next_segment_direction == "left":
            self.rect.width -= shrink_amount

        if self.rect.width <= 0 or self.rect.height <= 0:
            self.remove = True