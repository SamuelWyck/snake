import pygame



class SnakeSegment:
    def __init__(self, size, center, joint_width, joint_side):
        self.rect = pygame.rect.Rect((0, 0), size)
        self.rect.center = center

        #keep track of the back-middle of the segment
        self.back_pos = self.get_back_pos(joint_side)

        #keep track of front side of segment
        self.front_pos = self.get_front_pos(joint_side)

        #extend rect in the direction needed to cover joint gap
        self.grow(joint_width)

        self.remove = False

    

    def get_front_pos(self, joint_side):
        front_pos = None

        if joint_side == "top":
            front_pos = list(self.rect.midtop)
        elif joint_side == "left":
            front_pos = list(self.rect.midleft)
        elif joint_side == "bottom":
            front_pos = list(self.rect.midbottom)
        elif joint_side == "right":
            front_pos = list(self.rect.midright)

        return front_pos



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

    

    def grow(self, growth_amount):
        x_index = 0
        y_index = 1

        front_x, front_y = self.front_pos
        midtop_X, midtop_y = self.rect.midtop
        midright_x, midright_y = self.rect.midright
        midbottom_x, midbottom_y = self.rect.midbottom
        midleft_x, midleft_y = self.rect.midleft

        if front_x == midtop_X and front_y == midtop_y:
            self.rect.height += growth_amount
            self.rect.centery -= growth_amount
            self.front_pos[y_index] -= growth_amount
        elif front_x == midright_x and front_y == midright_y:
            self.rect.width += growth_amount
            self.front_pos[x_index] += growth_amount
        elif front_x == midbottom_x and front_y == midbottom_y:
            self.rect.height += growth_amount
            self.front_pos[y_index] += growth_amount
        elif front_x == midleft_x and front_y == midleft_y:
            self.rect.width += growth_amount
            self.rect.centerx -= growth_amount
            self.front_pos[x_index] -= growth_amount
    


    def shrink(self, shrink_amount):
        x_index = 0
        y_index = 1

        front_x, front_y = self.front_pos
        midtop_X, midtop_y = self.rect.midtop
        midright_x, midright_y = self.rect.midright
        midbottom_x, midbottom_y = self.rect.midbottom
        midleft_x, midleft_y = self.rect.midleft

        if front_x == midtop_X and front_y == midtop_y:
            self.rect.height -= shrink_amount
            self.back_pos[y_index] -= shrink_amount
        elif front_x == midright_x and front_y == midright_y:
            self.rect.width -= shrink_amount
            self.rect.centerx += shrink_amount
            self.back_pos[x_index] += shrink_amount
        elif front_x == midbottom_x and front_y == midbottom_y:
            self.rect.height -= shrink_amount
            self.rect.centery += shrink_amount
            self.back_pos[y_index] += shrink_amount
        elif front_x == midleft_x and front_y == midleft_y:
            self.rect.width -= shrink_amount
            self.back_pos[x_index] -= shrink_amount

        if self.rect.width <= 0 or self.rect.height <= 0:
            self.remove = True