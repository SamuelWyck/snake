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
        close_rect_point = self.closest_rect_point(rect)
        distance_to_rect_point = self.distance_to_point(close_rect_point)
        return distance_to_rect_point <= self.radius
    


    def distance_to_point(self, point):
        pointx, pointy = point
        x = pointx - self.centerx
        y = pointy - self.centery

        return math.sqrt((x * x) + (y * y))

        

    def closest_rect_point(self, rect):
        pointx, pointy = self.center

        if pointx < rect.x:
            pointx = rect.x
        elif pointx > rect.x + rect.width:
            pointx = rect.right

        if pointy < rect.y:
            pointy = rect.y
        elif pointy > rect.bottom:
            pointy = rect.bottom

        return (pointx, pointy)


    
    def edge_point_closest_to(self, point):
        pointx, pointy = point
        centerx, centery = self.center

        x = pointx - centerx
        y = pointy - centery
        angle = 0
        if x != 0:
            angle = math.atan(y / x)
            if x < 0:
                angle += math.pi
        else:
            angle = math.pi / 2 if y > 0 else (3 * math.pi) / 2

        edgex = math.cos(angle) * self.radius
        edgey = math.sin(angle) * self.radius
        return [edgex + centerx, edgey + centery]