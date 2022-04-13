from classes import Edge

class Graph:
    def __init__(self):
        self.edges = []
        self.num_edges = 0

    def add_edge(self, origin, dest, weight):
        edge = Edge(origin, dest, weight)
        if edge not in self.edges:
            self.numvertices = self.num_edges + 1
            self.edges.append(edge)

    def get_edges(self):
        return self.edges

    def get_num_edges(self):
        return self.num_edges
    
    def get_num_vertices(self):
        vertices = []
        for edge in self.edges:
            if edge.get_origin() not in vertices:
                vertices.append(edge.get_origin())
            if edge.get_dest() not in vertices:
                vertices.append(edge.get_dest())            
        return len(vertices)