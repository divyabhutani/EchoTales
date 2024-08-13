class TetrahedronNavigator:
    def __init__(self, neighbors):
        self.neighbors = neighbors
        self.current_index = 0
        self.iteration_count = 0

    def update_barycentric_coordinates(self, g1, g2, g3):
        g4 = 1 - g1 - g2 - g3
        self.coordinates = [g1, g2, g3, g4]

    def is_valid(self):
        return all(coord >= 0 for coord in self.coordinates) or self.iteration_count >= 20000

    def update_current_index(self):
        if not self.is_valid():
            return False
        smallest_coord_index = self.coordinates.index(min(self.coordinates))
        self.current_index = self.neighbors[self.current_index][smallest_coord_index]
        self.iteration_count += 1
        return True