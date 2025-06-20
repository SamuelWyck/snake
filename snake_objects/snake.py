import pygame
from snake_objects.snake_segment import Snake_Segment



class Snake:
    def __init__(self, topleft, size, step_size, step_interval, color, controller):
        self.rect = pygame.rect.Rect(topleft, (size, size))
        self.size = size
        self.joint_size = (step_size - size) if (step_size - size) > 0 else 0
        self.vector = pygame.math.Vector2(self.rect.center)

        self.step_interval = step_interval
        self.max_step_interval = step_interval
        self.step_size = step_size
        self.color = color
        
        self.controller = controller

        #movement variables
        self.move_up = 0
        self.move_right = 1
        self.move_down = 2
        self.move_left = 3
        self.movement = self.move_right
        self.last_movement = self.move_right
    
        self.collide_point = self.rect.center

        #setup the starting body
        self.body_length = 2
        self.body = []
        for i in range(self.body_length):
            body_segment = Snake_Segment(
                self.size,
                (self.rect.centerx - (self.step_size * (i + 1)), self.rect.centery),
                self.joint_size,
                "right",
                self.color, self.max_step_interval * self.body_length - (i * self.max_step_interval)
            )
            self.body.append(body_segment)
        self.body.reverse()
        
        #variables to handle batching body segment removals
        self.body_remove_interval = 60 * 3
        self.max_body_remove_interval = 60 * 3



    def update(self, surface, delta_time):
        self.handle_movement_input()

        interval_change = 1 * delta_time
        self.step_interval -= interval_change
        if self.step_interval <= 0:
            self.step_interval = self.max_step_interval
            prev_head_pos = self.move()
            self.add_body_segment(prev_head_pos)
        
        self.draw(surface)
        remove = self.draw_body(surface, delta_time)

        self.handle_segment_removal(remove, delta_time)



    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.circle(surface, (255, 0, 0), self.collide_point, 10)



    def handle_movement_input(self):
        keys = pygame.key.get_just_pressed()
        
        if keys[pygame.K_w] and self.last_movement != self.move_down:
            self.movement = self.move_up
        if keys[pygame.K_s] and self.last_movement != self.move_up:
            self.movement = self.move_down
        if keys[pygame.K_a] and self.last_movement != self.move_right:
            self.movement = self.move_left
        if keys[pygame.K_d] and self.last_movement != self.move_left:
            self.movement = self.move_right
    


    def move(self):
        prev_head_pos = list(self.rect.center)

        if self.movement == self.move_up:
            self.rect.centery -= self.step_size
        elif self.movement == self.move_down:
            self.rect.centery += self.step_size
        elif self.movement == self.move_left:
            self.rect.centerx -= self.step_size
        elif self.movement == self.move_right:
            self.rect.centerx += self.step_size

        self.collide_point = self.rect.center
        self.vector.x, self.vector.y = self.rect.centerx, self.rect.centery
        self.last_movement = self.movement
        return prev_head_pos



    def draw_body(self, surface, delta_time):
        remove = False
        for body_part in self.body:
            body_part.update(surface, delta_time)
            if body_part.remove:
                remove = True
        
        return remove
    


    def get_joint_side(self, segment_pos):
        same_y_coord = segment_pos[1] == self.rect.centery
        if same_y_coord:
            return "left" if segment_pos[0] > self.rect.centerx else "right"
        return "top" if segment_pos[1] > self.rect.centery else "bottom"

    

    def handle_segment_removal(self, remove, delta_time):
        if remove and self.body_remove_interval <= 0:
            self.body = [item for item in self.body if not item.remove]
            self.body_remove_interval = self.max_body_remove_interval
        elif self.body_remove_interval <= 0:
            self.body_remove_interval = self.max_body_remove_interval
        else:
            self.body_remove_interval -= (1 * delta_time)
    


    def add_body_segment(self, prev_head_pos):
        joint_side = self.get_joint_side(prev_head_pos)

        body_segment = Snake_Segment(
            self.size,
            prev_head_pos,
            self.joint_size,
            joint_side,
            self.color,
            self.max_step_interval * self.body_length
        )
        self.body.append(body_segment)