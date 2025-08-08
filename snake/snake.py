import pygame
from snake.snake_segment import SnakeSegment



class Snake:
    def __init__(self, segment_positions, size, step_size, step_interval, color, controller):
        head_position = segment_positions[0]
        self.rect = pygame.rect.Rect(head_position, (size, size))
        self.vector = pygame.math.Vector2(self.rect.center)

        self.size = size
        self.joint_size = (step_size - size) if (step_size - size) > 0 else 0

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
        self.movement = None
        self.last_movement = None
    
        self.increase_length = False
        self.decrease_length = False

        #setup the starting body
        self.min_body_length = 2
        self.body_length = len(segment_positions) - 1 #subtract by one to ignore head
        self.body = []
        self.initialize_body(segment_positions)


    
    def initialize_body(self, segment_postions):
        last_segment_pos = self.rect.topleft
        aligned_segments = []
        vertical = None

        for i in range(1, len(segment_postions)): #start at index 1 to skip head
            segment_pos = segment_postions[i]

            aligned, vertical = self.segments_aligned(segment_pos, last_segment_pos, vertical)
            if aligned:
                aligned_segments.append(segment_pos)
                continue
   
            segment = self.create_body_segment(aligned_segments, last_segment_pos)
            self.body.append(segment)
            last_segment_pos = aligned_segments[-1]
            aligned_segments = [segment_pos] 
        
        if aligned_segments:
            segment = self.create_body_segment(aligned_segments, last_segment_pos)
            self.body.append(segment)
        self.body.reverse()
        
        #correct center position to sit in the middle of the tile
        self.rect.centerx += self.joint_size//2
        self.rect.centery += self.joint_size//2
        self.vector = pygame.math.Vector2(self.rect.center)

        self.set_movement_direction()



    def set_movement_direction(self):
        x_coord = 0
        y_coord = 1

        first_segment_center = self.body[-1].rect.center
        head_center = self.rect.center

        if first_segment_center[x_coord] < head_center[x_coord]:
            self.movement = self.move_right
        elif first_segment_center[x_coord] > head_center[x_coord]:
            self.movement = self.move_left
        elif first_segment_center[y_coord] < head_center[y_coord]:
            self.movement = self.move_down
        elif first_segment_center[y_coord] > head_center[y_coord]:
            self.movement = self.move_up
        
        self.last_movement = self.movement

        

    def segments_aligned(self, first_seg_pos, second_seg_pos, vertical):
        x_coord = 0
        y_coord = 1

        if vertical is None:
            if first_seg_pos[x_coord] == second_seg_pos[x_coord]:
                return True, True
            elif first_seg_pos[y_coord] == second_seg_pos[y_coord]:
                return True, False
            return False, None
            
        if vertical and first_seg_pos[x_coord] == second_seg_pos[x_coord]:
            return True, True
        
        if not vertical and first_seg_pos[y_coord] == second_seg_pos[y_coord]:
            return True, True

        return False, None
    


    def create_body_segment(self, aligned_segments, last_segment_pos):
        x_coord = 0
        first_segment_pos = aligned_segments[0]
        second_segment_pos = aligned_segments[1] if len(aligned_segments) > 1 else aligned_segments[0]


        vertical = first_segment_pos[x_coord] == second_segment_pos[x_coord]

        long_side_length = len(aligned_segments) * self.size
        long_side_length += (len(aligned_segments) - 1) * self.joint_size
        short_side_length = self.size
        size = (long_side_length, short_side_length)
        if vertical:
            size = (short_side_length, long_side_length)

        center = self.get_segment_center(first_segment_pos, last_segment_pos, size)
        joint_side = self.get_joint_side(first_segment_pos, last_segment_pos)

        segment = SnakeSegment(size, center, self.joint_size, joint_side)
        return segment
        


    def get_segment_center(self, segment_pos, last_segment_pos, size):
        x_coord = 0
        y_coord = 1
        width_index = 0
        height_index = 1

        current_x_pos = segment_pos[x_coord]
        current_y_pos = segment_pos[y_coord]
        last_x_pos = last_segment_pos[x_coord]
        last_y_pos = last_segment_pos[y_coord]

        center_x = current_x_pos + size[width_index]//2
        center_y = current_y_pos + size[height_index]//2
        if current_y_pos < last_y_pos:
            center_y = current_y_pos - size[height_index]//2
        elif current_x_pos < last_x_pos:
            center_x = current_x_pos - size[width_index]//2

        return (center_x + self.joint_size//2, center_y + self.joint_size//2)



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
            
            if not self.increase_length:
                self.shrink_back_segment()
            else:
                self.increase_length = False

            if self.decrease_length:
                self.shrink_back_segment()
                self.decrease_length = False
        
        self.draw(surface)
        remove = self.draw_body(surface)

        if remove:
            self.handle_segment_removal()
            


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.circle(surface, (255, 0, 0), self.vector, 10)



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
        if pressed_inputs["GROW"]:
            self.grow_snake()
        if pressed_inputs["SHRINK"]:
            self.shrink_snake()
    


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
            body_part.draw(surface, self.color)
        
        return remove
    


    def get_joint_side(self, segment_pos, next_segment_pos):
        x_coord = 0 
        y_coord = 1

        same_y_coord = segment_pos[y_coord] == next_segment_pos[y_coord]
        if same_y_coord:
            return "left" if segment_pos[x_coord] > next_segment_pos[x_coord] else "right"
        return "top" if segment_pos[y_coord] > next_segment_pos[y_coord] else "bottom"



    def get_change_direction(self, segment_pos, next_segment_pos):
        return self.get_joint_side(segment_pos, next_segment_pos)
    


    def grow_front_segment(self):
        front_body_part = self.body[-1]
        change_direction = self.get_change_direction(front_body_part.rect.center, self.rect.center)
        front_body_part.grow(self.step_size, change_direction)

    

    def shrink_back_segment(self):
        # back_body_part = self.body[0]
        # next_index = 1
        back_body_part = None
        next_index = None
        for index, part in enumerate(self.body):
            if not part.remove:
                back_body_part = part
                next_index = index + 1
                break

        next_body_part_pos = self.body[next_index].back_pos if len(self.body) > next_index else self.rect.center
        change_direction = self.get_change_direction(back_body_part.rect.center, next_body_part_pos)
        back_body_part.shrink(self.step_size, change_direction)

    

    def handle_segment_removal(self):
        self.body = [item for item in self.body if not item.remove]
    


    def add_body_segment(self, prev_head_pos):
        joint_side = self.get_joint_side(prev_head_pos, self.rect.center)

        body_segment = SnakeSegment(
            (self.size, self.size),
            prev_head_pos,
            self.joint_size,
            joint_side
        )
        self.body.append(body_segment)
    


    def grow_snake(self):
        if not self.decrease_length and not self.increase_length:
            self.increase_length = True
            self.body_length += 1

    

    def shrink_snake(self):
        long_enough = self.body_length > self.min_body_length
        if long_enough and not self.increase_length and not self.decrease_length:
            self.decrease_length = True
            self.body_length -= 1
    


    def just_moved(self):
        return self.step_interval == self.max_step_interval
    


    def body_collide(self):
        hit_segment = self.rect.collideobjects(
            self.body, 
            key=lambda segment: segment.rect
        )
        return hit_segment != None
    


    def collide(self, collider_rect):
        if collider_rect.colliderect(self.rect):
            return True
        
        hit_segment = collider_rect.collideobjects(
            self.body,
            key=lambda segment : segment.rect
        )
        return hit_segment != None
    


    def get_direction_as_str(self):
        if self.last_movement == self.move_up:
            return "up"
        if self.last_movement == self.move_down:
            return "down"
        if self.last_movement == self.move_left:
            return "left"
        return "right"