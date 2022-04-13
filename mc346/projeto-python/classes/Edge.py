class Edge:
    def __init__(self, o, d, w):
        self.origin = o
        self.dest = d
        self.weight = w

    def get_origin(self):
        return self.origin

    def get_dest(self):
        return self.dest

    def get_weight(self):
        return self.weight