import math
import pygame


class Circle:
    def __init__(self, center, radius):
        self._center = list(center)
        self._radius = radius


    @property
    def radius(self):
        return self._radius
    

    @radius.setter
    def radius(self, new_radius):
        if new_radius < 0:
            new_radius = 0
        self._radius = new_radius
    

    @property
    def center(self):
        return self._center
    

    @center.setter
    def center(self, new_center):
        try:
            new_x, new_y = new_center
            self._center = [new_x, new_y]
        except:
            pass


    @property
    def centerx(self):
        return self._center[0]
    

    @centerx.setter
    def centerx(self, new_x):
        self._center[0] = new_x


    @property
    def centery(self):
        return self._center[1]
    

    @centery.setter
    def centery(self, new_y):
        self._center[1] = new_y


    def collide_circle(self, circle):
        otherx, othery = circle.center
        centerx, centery = self.center

        adjacent = otherx - centerx
        opposite = othery - centery
        distance = math.sqrt((adjacent * adjacent) + (opposite * opposite))

        return distance <= self.radius + circle.radius
    

    def collide_rect(self, rect):
        ...

    
    def closest_edge_to_point(self, point):
        pointx, pointy = point
        centerx, centery = self.center

        x = pointx - centerx
        y = pointy - centery
        angle = math.atan(y / x)
        if x < 0:
            angle += math.pi

        edgex = math.cos(angle) * self.radius
        edgey = math.sin(angle) * self.radius
        return [edgex + centerx, edgey + centery]
    




def main():
    pygame.display.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    rect = pygame.rect.Rect((400, 400), (300, 40))

    hitCircle = Circle((200, 200), 20)

    mouseCircle = Circle((0, 0), 10)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    run = False

        mousePos = pygame.mouse.get_pos()
        mouseCircle.center = mousePos

        color = (255, 0, 0)
        if mouseCircle.collide_circle(hitCircle):
            color = (0, 255, 0)

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), rect)
        pygame.draw.circle(screen, color, hitCircle.center, hitCircle.radius)
        pygame.draw.circle(screen, (0, 0, 255), mouseCircle.center, mouseCircle.radius)
        pygame.display.update()
            


main()
    