from level_objects.proto_objects.level_tile import LevelTile



class Box(LevelTile):
    def __init__(self, topleft, size, color, image):
        super().__init__(topleft, size)

        self.image = image
        self.color = color
        self.move_distance = self.rect.width

    

    def update(self, surface, delta_time):
        self.draw(surface)
    


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    

    def collide(self, rect):
        return self.rect.colliderect(rect)

    

    def move(self, player, static_tiles, dynamic_tiles, agents, tile_to_skip, in_bounds):
        old_position = self.move_self(player)

        if self.rect.center in static_tiles:
            self.rect.center = old_position
            return False
        if not in_bounds(self.rect):
            self.rect.center = old_position
            return False
        if player.collide(self.rect):
            self.rect.center = old_position
            return False
        
        for tile in dynamic_tiles:
            if tile_to_skip(tile):
                continue
            if tile.collide(self.rect):
                self.rect.center = old_position
                return False

        for agent in agents:
            if agent == self:
                continue
            if agent.collide(self.rect):
                self.rect.center = old_position
                return False
        
        return True
    


    def move_self(self, player):
        old_position = self.rect.center
        direction = player.get_direction_as_str()

        if direction == "right":
            self.rect.x += self.move_distance
        elif direction == "left":
            self.rect.x -= self.move_distance
        elif direction == "up":
            self.rect.y -= self.move_distance
        else:
            self.rect.y += self.move_distance

        return old_position