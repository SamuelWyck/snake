import pygame



class Animation:
    def __init__(self, frames):
        self.frame_list = []
        self.image_cache = {}

        total_duration = 0
        for i in range(len(frames)):
            frame = frames[i]
            image, duration = frame
            total_duration += duration
            self.frame_list.append((image, total_duration))
            self.image_cache[i] = {}
        
        self.total_duration = total_duration
        self.frame_index = 0
        self.time_passed = 0

    

    def get_frame(self, delta_time, angle=0):
        self.time_passed += delta_time
        _, current_duration = self.frame_list[self.frame_index]
        if self.time_passed > current_duration: 
            self.frame_index += 1
            if self.frame_index == len(self.frame_list):
                self.frame_index = 0
                self.time_passed = 0
        
        return self.get_rotated_image(angle)



    def get_rotated_image(self, angle):
        angle = round(angle)
        if angle not in self.image_cache[self.frame_index]:
            image, _ = self.frame_list[self.frame_index]
            rotated_image = pygame.transform.rotozoom(image, angle, 1)
            self.image_cache[self.frame_index][angle] = rotated_image
        
        return self.image_cache[self.frame_index][angle]