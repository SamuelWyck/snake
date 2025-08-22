import pygame
from level_objects.proto_objects.level_tile import LevelTile



class SpikeBall(LevelTile):
    def __init__(self, target_points, tile_size, spike_size, velocity, color, image):
        super().__init__((0, 0), (spike_size, spike_size))

        # Get the center coords for each target_point
        self.target_points = []
        x_index = 0
        y_index = 1
        tile_width_index = 0
        half_tile_size = tile_size[tile_width_index] // 2
        for point in target_points:
            x_pos = point[x_index]
            x_pos += half_tile_size
            y_pos = point[y_index]
            y_pos += half_tile_size
            self.target_points.append((x_pos, y_pos))
        self.sort_target_points()
        self.rect.center = self.target_points[0]
        
        self.color = color
        self.image = image
        self.velocity = velocity
        self.target_index = 0
        self.target_index_change = 1
        self.vector = pygame.math.Vector2(self.rect.center)

    

    def update(self, surface, delta_time):
        velocity = self.velocity * delta_time
        target_point = self.target_points[self.target_index]
        
        old_x = self.vector.x
        old_y = self.vector.y
        self.vector = self.vector.move_towards(target_point, velocity)
        if old_x == self.vector.x and old_y == self.vector.y:
            self.update_target_index()
        self.rect.centerx = self.vector.x
        self.rect.centery = self.vector.y

        self.draw(surface)


    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    


    def collide(self, rect):
        return self.rect.colliderect(rect)

    

    def update_target_index(self):
        new_index = self.target_index + self.target_index_change

        if new_index < 0:
            self.target_index_change = 1
        elif new_index >= len(self.target_points):
            self.target_index_change = -1

        self.target_index += self.target_index_change

    

    def sort_target_points(self):
        edge_list = self.build_edge_list()
        graph = self.build_graph(edge_list)
        
        target_connection_length = len(self.target_points)
        for node in graph:
            connections = self.find_longest_path(node, graph, set())
            if len(connections) == target_connection_length:
                self.target_points = connections
                break



    def find_longest_path(self, node, graph, visited):
        if node in visited:
            return []
        visited.add(node)

        longest_path = []
        for neighbor in graph[node]:
            neighbor_path = self.find_longest_path(neighbor, graph, visited)
            if len(neighbor_path) > len(longest_path):
                longest_path = longest_path + neighbor_path
        
        return [node, *longest_path]

    

    def build_edge_list(self):
        x_index = 0
        y_index = 1
        edge_list = []
        found_edges = set()
        for point in self.target_points:
            for other_point in self.target_points:
                if point == other_point:
                    continue
                
                x_equal = point[x_index] == other_point[x_index]
                y_equal = point[y_index] == other_point[y_index]
                edge = (point, other_point)
                if (x_equal or y_equal) and edge not in found_edges:
                    self.append_edge(edge, edge_list)
                    found_edges.add((point, other_point))
                    found_edges.add((other_point, point))
        
        return edge_list
    


    def append_edge(self, new_edge, edge_list):
        x_index = 0
        y_index = 1
        first_new_point = new_edge[0]
        second_new_point = new_edge[1]
        for edge in edge_list:
            first_point = edge[0]
            second_point = edge[1]
            if first_point != first_new_point and second_point != second_new_point:
                continue

            edge_point = first_point if first_point != first_new_point else second_point
            new_edge_point = first_new_point if first_point != first_new_point else second_new_point
            if edge_point[x_index] != new_edge_point[x_index] and edge_point[y_index] != new_edge_point[y_index]:
                continue
            
            differing_index = x_index if edge_point[x_index] != new_edge_point[x_index] else y_index
            same_edge_point = first_point if edge_point != first_point else second_point
            old_diff = abs(same_edge_point[differing_index] - edge_point[differing_index])
            new_diff = abs(same_edge_point[differing_index] - new_edge_point[differing_index])
            if old_diff < new_diff:
                return
            else:
                edge_list.remove(edge)
                break
            
        edge_list.append(new_edge)      
    


    def build_graph(self, edge_list):
        graph = {}
        for edge in edge_list:
            first_point = edge[0]
            second_point = edge[1]

            if first_point not in graph:
                graph[first_point] = []
            if second_point not in graph:
                graph[second_point] = []
            
            graph[first_point].append(second_point)
            graph[second_point].append(first_point)

        return graph