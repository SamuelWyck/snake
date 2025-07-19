from level_objects.proto_objects.level_tile import LevelTile



class Box(LevelTile):
    def __init__(self, topleft, size, color, image):
        # width_index = 0
        # x_coord = 0
        # y_coord = 1

        # width = size[width_index]
        # corrected_width = width * .75
        # remaining_width = width - corrected_width
        # topleft_correction = remaining_width // 2

        # topleft = (
        #     topleft[x_coord] + topleft_correction,
        #     topleft[y_coord] + topleft_correction
        # )
        # size = (
        #     corrected_width,
        #     corrected_width
        # )

        super().__init__(topleft, size)

        self.image = image
        self.color = color

    

    def update(self, surface, delta_time):
        self.draw(surface)
    


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)