import pygame



class Snake_Segment:
    def __init__(self, size, joint_width, center, color, life_span):
        self.rect = pygame.rect.Rect((0, 0), (size, size))
        self.rect.center = center

        #set up joint rects to cover gaps
        top_rect = pygame.rect.Rect((0, 0), (size, joint_width))
        top_rect.midbottom = self.rect.midtop
        right_rect = pygame.rect.Rect((0, 0), (joint_width, size))
        right_rect.midleft = self.rect.midright
        bottom_rect = pygame.rect.Rect((0, 0), (size, joint_width))
        bottom_rect.midtop = self.rect.midbottom
        left_rect = pygame.rect.Rect((0, 0), (joint_width, size))
        left_rect.midright = self.rect.midleft

        self.joint_rects = {
            "top": top_rect,
            "right": right_rect,
            "bottom": bottom_rect,
            "left": left_rect
        }

        self.life_span = life_span
        self.color = color

        self.remove = False
    


    def update(self, surface, delta_time, join_rect_key):
        if not self.remove:
            self.draw(surface, join_rect_key)
            life_span_change = 1 * delta_time
            self.life_span -= life_span_change
            if self.life_span <= 0:
                self.remove = True
    


    def draw(self, surface, joint_rect_key):
        pygame.draw.rect(surface, self.color, self.rect)
        
        joint_rect = self.joint_rects[joint_rect_key]
        pygame.draw.rect(surface, self.color, joint_rect)