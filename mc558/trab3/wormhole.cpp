/** Fábio Camargo Ricci - 170781**/
#include <iostream>
#include <vector>
#include <limits.h>

using namespace std;

struct edge {
  unsigned int origin;
  unsigned int dest;
  int weight;
  edge(unsigned int x, unsigned int y, int w) : origin(x), dest(y), weight(w) {}
};

struct graph {
  unsigned int size;
  vector<edge> edges;
  graph(unsigned int n) : size(n) {}
};

/**
 * returns the weighted graph
 * */
graph readGraph() {
    unsigned int n, m;
    cin >> n >> m;
    graph g(n);
    unsigned int x, y;
    int w;
    for (unsigned int k = 0; k < m; k++) {
        cin >> x >> y >> w;
        g.edges.push_back(edge(x, y, w));
    }
    return g;
}

/**
 * Bellman-Ford algorithm
 * Returns true if past is reachable from earth (there is a negative cycle)
 * Returns false otherwise
 */
bool reachable(graph g, unsigned int s) {
    vector<int> distance(g.size, INT_MAX); // distance vector to every vertex
    distance[s] = 0; // origin earth
    // Calculate minimum distances from earth
    for (unsigned int i = 0; i < g.size - 1; i++) { // vertices
        for (unsigned int j = 0; j < g.edges.size(); j++) { // edges
            unsigned int u = g.edges[j].origin;
            unsigned int v = g.edges[j].dest;
            int w = g.edges[j].weight;
            if (distance[u] != INT_MAX && distance[v] > distance[u] + w) { // new path is shorter than previous estimated
                distance[v] = distance[u] + w;
            }
        }
    }
    // Check for negative cycles
    for (unsigned int i = 0; i < g.edges.size(); i++) {
        unsigned int u = g.edges[i].origin;
        unsigned int v = g.edges[i].dest;
        int w = g.edges[i].weight;
        if (distance[u] != INT_MAX && distance[v] > distance[u] + w) { // if true, found negative cycle
            return true;
        }
    }
    return false;
}

int main() {
    graph g = readGraph();
    if (reachable(g, 0)) {
        cout << "Possivel" << endl;
    } else {
        cout << "Impossivel" << endl;
    }
    return 0;
}