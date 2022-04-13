from fileinput import input
from classes import Graph
from methods.floydwarshall import do_floyd_warshall
from methods.tripmethods import calculate_max_incovenience, get_min_inconvenience
from sys import argv

def print_paths(trip_a, trip_b, inconvenience, indexes):
    if (trip_a in indexes):
        index_a = indexes.index(trip_a) + 1
    else:
        index_a = indexes.index(trip_a) + 1
    if (trip_b in indexes):
        index_b = indexes.index(trip_b) + 1
    else:
        index_b = indexes.index(trip_b) + 1
    (path, _) = inconvenience
    (a, b, c, d) = path
    print("passageiros: " + str(index_a) + " " + str(index_b) 
        + " percurso: " + str(a) + " " + str(b) + " " + str(c) + " " + str(d))

def print_path(trip, indexes):
    if (trip in indexes):
        index = indexes.index(trip) + 1
    else:
        index = indexes.index(trip) + 1
    (a, b) = trip
    print("passageiro: " + str(index) + " percurso: " + str(a) + " " + str(b))

def read_input():
    graph = Graph()
    reading_trips = False
    starting_trips = []
    ongoing_trips = []
    indexes = []
    if len(argv) > 1:
        f = open(argv[1], 'r')
        try:
            lines = iter(f.readlines())
            for line in lines:
                line = line.strip()
                words = line.split(" ")
                if len(words) > 1 and not reading_trips:
                    origin = int(words[0])
                    dest = int(words[1])
                    weight = float(words[2])
                    graph.add_edge(origin, dest, weight)
                elif len(words) == 3 and reading_trips:
                    origin = int(words[0])
                    dest = int(words[1])
                    current = int(words[2])
                    ongoing_trips.append((origin, dest, current))
                    indexes.append((origin, dest, current))
                elif len(words) == 2 and reading_trips:
                    origin = int(words[0])
                    dest = int(words[1])
                    starting_trips.append((origin, dest))
                    indexes.append((origin, dest))
                else:
                    reading_trips = True
        finally:
            f.close()
    return (graph, starting_trips, ongoing_trips, indexes)

try:
    (graph, starting_trips, ongoing_trips, indexes) = read_input()
    dist = do_floyd_warshall(graph)

    starting_trips_aux = starting_trips.copy()
    ongoing_trips_aux = ongoing_trips.copy()
    for trip in starting_trips_aux:
        if trip in starting_trips:
            min_inco = get_min_inconvenience(trip, ongoing_trips, starting_trips, dist)
            if (len(min_inco) == 2):
                (trip, _) = min_inco
                print_path(trip, indexes)
            else:
                (trip_a, trip_b, inconvenience) = min_inco
                print_paths(trip_a, trip_b, inconvenience, indexes)

    for trip in ongoing_trips:
        (_, dest, current) = trip
        index = indexes.index(trip) + 1
        print("passageiro: " + str(index) + " percurso: " + str(current) + " " + str(dest))

except Exception as e: 
    print(e)