import pygame
from snake_objects.snake_segment import Snake_Segment
import random



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
        self._increase_length = False

        #setup the starting body
        self.body_length = 2
        self.body = []
        body_segment = Snake_Segment(
            self.size,
            (self.rect.centerx - self.size - self.joint_size, self.rect.centery),
            self.joint_size,
            "right",
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
        body_segment.rect.centerx -= self.step_size
        body_segment.grow(self.step_size, "right")
        self.body.append(body_segment)



    def update(self, surface, delta_time):
        self.handle_input()

        interval_change = 1 * delta_time
        self.step_interval -= interval_change
        if self.step_interval <= 0:
            self.step_interval = self.max_step_interval
            prev_head_pos, same_direction = self.move()
            if not same_direction:
                self.add_body_segment(prev_head_pos)
            else:
                self.grow_front_segment()
            self.shrink_back_segment()
            
            if self._increase_length:
                self.increase_length()
                self._increase_length = False
        
        self.draw(surface)
        remove = self.draw_body(surface)

        if remove:
            self.handle_segment_removal()
            


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.circle(surface, (255, 0, 0), self.collide_point, 10)



    def handle_input(self):
        pressed_inputs = self.controller.get_inputs()
        
        if pressed_inputs["UP"] and self.last_movement != self.move_down:
            self.movement = self.move_up
        if pressed_inputs["DOWN"] and self.last_movement != self.move_up:
            self.movement = self.move_down
        if pressed_inputs["LEFT"] and self.last_movement != self.move_right:
            self.movement = self.move_left
        if pressed_inputs["RIGHT"] and self.last_movement != self.move_left:
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

        same_direction = self.last_movement == self.movement
        self.last_movement = self.movement
        return prev_head_pos, same_direction



    def draw_body(self, surface):
        remove = False
        for body_part in self.body:
            if body_part.remove:
                remove = True
                continue
            body_part.draw(surface)
        
        return remove
    


    def get_joint_side(self, segment_pos, next_segment_pos):
        same_y_coord = segment_pos[1] == next_segment_pos[1]
        if same_y_coord:
            return "left" if segment_pos[0] > next_segment_pos[0] else "right"
        return "top" if segment_pos[1] > next_segment_pos[1] else "bottom"



    def get_change_direction(self, segment_pos, next_segment_pos):
        return self.get_joint_side(segment_pos, next_segment_pos)
    


    def grow_front_segment(self):
        front_body_part = self.body[-1]
        change_direction = self.get_change_direction(front_body_part.rect.center, self.rect.center)
        front_body_part.grow(self.step_size, change_direction)

    

    def shrink_back_segment(self):
        back_body_part = self.body[0]
        next_body_part_pos = self.body[1].back_pos if len(self.body) > 1 else self.rect.center
        change_direction = self.get_change_direction(back_body_part.rect.center, next_body_part_pos)
        back_body_part.shrink(self.step_size, change_direction)

    

    def handle_segment_removal(self):
        self.body = [item for item in self.body if not item.remove]
    


    def add_body_segment(self, prev_head_pos):
        joint_side = self.get_joint_side(prev_head_pos, self.rect.center)

        body_segment = Snake_Segment(
            self.size,
            prev_head_pos,
            self.joint_size,
            joint_side,
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
        self.body.append(body_segment)
    


    def grow_snake(self):
        self._increase_length = True



    def increase_length(self):
        back_segment = self.body[0]

        back_side_is_left = back_segment.back_pos[0] < back_segment.rect.centerx
        back_side_is_bottom = back_segment.back_pos[1] > back_segment.rect.centery
        width_is_long_side = back_segment.rect.width > back_segment.rect.height

        grow_direction = None
        if width_is_long_side:
            grow_direction = "left" if back_side_is_left else "right"
        else:
            grow_direction = "bottom" if back_side_is_bottom else "top"
        
        back_segment.grow(self.step_size, grow_direction)
        self.body_length += 1