from math import inf

def do_floyd_warshall(graph):
    size = graph.get_num_vertices()
    dist = [[inf for x in range(size)] for y in range(size)]
    for edge in graph.get_edges():
        dist[edge.get_origin()][edge.get_dest()] = edge.get_weight()
    for i in range(size):
        dist[i][i] = 0
    for k in range(size):
        for i in range(size):
            for j in range(size):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist