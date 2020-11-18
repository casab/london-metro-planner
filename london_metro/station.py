class Station:
    def __init__(self, name, line):
        self.name = name
        self.lines = [line]
        self.neighbors = {}

    def __str__(self):
        return f"{self.name}\nNeighbors: {[x.name for x in self.neighbors]}\nLines: {[x for x in self.lines]}"

    def add_neighbor(self, neighbor, eta):
        self.neighbors[neighbor] = eta

    def get_neighbors(self):
        return self.neighbors

    def add_line(self, line):
        self.lines.append(line)

    def get_connections(self):
        return self.neighbors.keys()

    def get_name(self):
        return self.name

    def get_eta(self, neighbor):
        return self.neighbors[neighbor]
