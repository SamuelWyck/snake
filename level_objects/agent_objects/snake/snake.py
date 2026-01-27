import pygame
from level_objects.agent_objects.snake.snake_segment import SnakeSegment
from utils.color import Color



class Snake:
    def __init__(self, segment_positions, size, step_size, step_interval, head_img, eyes_img, color, controller):
        head_position = segment_positions[0]
        self.rect = pygame.rect.Rect(head_position, (size, size))
        self.vector = pygame.math.Vector2(self.rect.center)

        self.size = size
        self.joint_size = (step_size - size) if (step_size - size) > 0 else 0

        self.step_interval = step_interval
        self.max_step_interval = step_interval
        self.step_size = step_size
        self.start_color = color
        self.color = color
        
        self.controller = controller

        #movement variables
        self.move_up = 0
        self.move_right = 1
        self.move_down = 2
        self.move_left = 3
        self.stopped = 4
        self.movement = None
        self.last_movement = None
    
        self.length_increase = 0
        self.length_decrease = 0

        #setup the starting body
        self.starting_segments = segment_positions
        self.eaten_pickups = []
        self.pickups_to_drop = []
        self.min_body_length = 2
        self.body_length = len(segment_positions) - 1 #subtract by one to ignore head
        self.body = []
        self.initialize_body(segment_positions)

        #setup image and image cache
        self.head_img = head_img
        self.eyes_img = eyes_img
        self.image = self.get_head_image()
        
        self.image_cache = {
            0: {self.color: self.image},
            180: {},
            -90: {},
            90: {}
        }
        self.image_angles = {
            self.move_up: 0,
            self.move_down: 180,
            self.move_right: -90,
            self.move_left: 90
        }


    
    def get_head_image(self):
        head_img = self.head_img.copy()
        head_img.fill(self.color, special_flags=pygame.BLEND_MIN)
        head_img.blit(self.eyes_img, (0, 0))
        return head_img


    
    def reset(self):
        head_position = self.starting_segments[0]
        self.rect = pygame.rect.Rect(head_position, (self.size, self.size))
        self.vector = pygame.math.Vector2(self.rect.center)

        self.length_increase = 0
        self.length_decrease = 0
        self.color = self.start_color
        self.step_interval = self.max_step_interval
        
        self.body_length = len(self.starting_segments) - 1
        self.body = []
        self.initialize_body(self.starting_segments)
        self.image = self.image_cache[0][self.color]


    
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
            center_y = current_y_pos - size[height_index]//2 + self.size
        elif current_x_pos < last_x_pos:
            center_x = current_x_pos - size[width_index]//2 + self.size

        return (center_x + self.joint_size//2, center_y + self.joint_size//2)



    def update(self, surface, delta_time):
        self.handle_input()

        interval_change = 1 * delta_time
        self.step_interval -= interval_change
        if self.step_interval < 0:
            self.step_interval = 0
            
        if self.step_interval <= 0 and self.movement != self.stopped:
            self.step_interval = self.max_step_interval
            prev_head_pos, same_direction = self.move()
            if not same_direction:
                self.add_body_segment(prev_head_pos)
            else:
                self.grow_front_segment()
            
            if self.length_increase == 0:
                self.shrink_back_segment()
            else:
                self.length_increase -= 1
                self.body_length += 1

            if self.length_decrease != 0 and self.length_increase == 0:
                self.shrink_back_segment()
                self.length_decrease -= 1
                self.body_length -= 1
        
        remove = self.draw_body(surface)
        self.draw(surface)

        if remove:
            self.handle_segment_removal()
            


    def draw(self, surface):
        image_angle = self.image_angles[self.last_movement]

        if self.color in self.image_cache[image_angle]:
            image_rot = self.image_cache[image_angle][self.color]
        else:
            image_rot = pygame.transform.rotate(self.image, image_angle).convert_alpha()
            self.image_cache[image_angle][self.color] = image_rot
        image_rect = image_rot.get_rect()
        image_rect.center = self.rect.center

        surface.blit(image_rot, image_rect.topleft)



    def handle_input(self):
        pressed_inputs = self.controller.get_inputs()
        
        self.movement = self.stopped
        if pressed_inputs["UP"] and self.last_movement != self.move_down:
            self.movement = self.move_up
        if pressed_inputs["DOWN"] and self.last_movement != self.move_up:
            self.movement = self.move_down
        if pressed_inputs["LEFT"] and self.last_movement != self.move_right:
            self.movement = self.move_left
        if pressed_inputs["RIGHT"] and self.last_movement != self.move_left:
            self.movement = self.move_right
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
        back_index = 0 if not self.body[0].remove else 1
        next_index = back_index + 1
        back_body_part = self.body[back_index]

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

    

    def shrink_snake(self):
        if len(self.eaten_pickups) == 0:
            return
        
        snake_back_position = self.get_snake_back_pos()
        pickup = self.eaten_pickups.pop()

        pickup.set_center_position(snake_back_position)
        pickup.remove = False
        if pickup.value < 0:
            self.length_increase += abs(pickup.value)
        else:
            self.length_decrease += pickup.value
        self.pickups_to_drop.append(pickup)
        
        last_pickup_idx = len(self.eaten_pickups) - 1
        new_color = self.eaten_pickups[last_pickup_idx].color if len(self.eaten_pickups) != 0 else self.start_color
        new_color = new_color if new_color != Color.NO_COLOR else self.start_color
        self.color = new_color
        if self.color not in self.image_cache[0]:
            self.image = self.get_head_image()
        else:
            self.image = self.image_cache[0][self.color]



    def get_snake_back_pos(self):
        back_seg_index = 0
        back_seg = self.body[back_seg_index] if not self.body[back_seg_index].remove else self.body[back_seg_index + 1]
        return tuple(back_seg.back_pos)



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
    


    def collide_laser(self, laser):
        if laser.color == self.color and self.color != Color.NO_COLOR:
            return
        
        if self.rect.colliderect(laser.rect):
            laser.shorten_laser(self.rect)
        
        for segment in self.body:
            if segment.rect.colliderect(laser.rect):
                laser.shorten_laser(segment.rect)
    


    def get_direction_as_str(self):
        if self.last_movement == self.move_up:
            return "up"
        if self.last_movement == self.move_down:
            return "down"
        if self.last_movement == self.move_left:
            return "left"
        return "right"



    @property
    def real_length(self):
        return self.body_length + (-1 * self.length_decrease) + self.length_increase



    def eat_pickup(self, pickup):
        if pickup.color == self.color and pickup.color != Color.NO_COLOR:
            return False
        if self.real_length + pickup.value < self.min_body_length:
            return False
        
        increase_length = pickup.value >= 0
        if increase_length:
            self.length_increase += pickup.value
        else:
            self.length_decrease += abs(pickup.value)

        if pickup.color != Color.NO_COLOR:
            self.color = pickup.color
            self.image = self.get_head_image()
        self.eaten_pickups.append(pickup)
        return True
