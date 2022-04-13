/** Fábio Camargo Ricci - 170781**/
#include <iostream>
#include <vector>
#include <algorithm>
#include <limits>

using namespace std;

struct edge {
    unsigned int origin;
    unsigned int dest;
    unsigned int weight;
    edge(unsigned int x, unsigned int y, unsigned int w) : origin(x), dest(y), weight(w) {}
};

struct graph {
    unsigned int size;
    vector<edge> edges;
    graph(unsigned int n) : size(n) {}
};

struct sets {
  unsigned int *ancestor, *rank;
  unsigned int size;
  // Constructor
  sets(unsigned int n) {
      this->size = n;
      ancestor = new unsigned int[n + 1];
      rank = new unsigned int[n + 1];
      // Initially all sets have only one vertex
      for (unsigned int i = 0; i <= n; i++) {
          rank[i] = 0;
          ancestor[i] = i;
      }
  }
  // Find with path Compression
  int find(unsigned int x) {
      if (x != ancestor[x]) {
          // Path compression
          ancestor[x] = find(ancestor[x]);
      }
      return ancestor[x];
  }
  // Merge wit union by rank
  void join(unsigned int x, unsigned int y) {
      x = find(x);
      y = find(y);
      // Tree with smaller height becomes subtree
      if (rank[x] > rank[y]) {
          // y becomes subtree
          ancestor[y] = x;
      } else {
          // x becomes subtree
          ancestor[x] = y;
      }
      if (rank[x] == rank[y]) {
          rank[y]++;
      }
  }
};

/**
 * returns the weighted graph
 * */
graph readGraph() {
    unsigned int n, m;
    cin >> n >> m;
    graph g(n);
    unsigned int x, y, w;
    for (unsigned int k = 0; k < m; k++) {
        cin >> x >> y >> w;
        g.edges.push_back(edge(x, y, w));
    }
    return g;
}

/**
 * returns all pairs <s, t>
 * */
vector<pair<unsigned int, unsigned int> > readPairs() {
    unsigned int k;
    cin >> k;
    vector<pair<unsigned int, unsigned int> > pairs;
    unsigned int s, t;
    for (unsigned int i = 0; i < k; i++) {
        cin >> s >> t;
        pairs.push_back(make_pair(s, t));
    }
    return pairs;
}

bool compareEdges(edge e1, edge e2) {
    return e1.weight < e2.weight;
}

/**
 * returns the minimum spanning tree of the graph g
 */
vector<vector<pair<unsigned int, unsigned int> > > kruskal(graph g) {
    sets dSets(g.size); // Creates a disjoint set for every vertex
    sort(g.edges.begin(), g.edges.end(), compareEdges); // Sort all edges in non-decreasing order
    vector<vector<pair<unsigned int, unsigned int> > > v(g.size);

    for (vector<edge>::iterator it = g.edges.begin(); it != g.edges.end(); it++) {
        unsigned int x = it->origin;
        unsigned int y = it->dest;
        unsigned int set_x = dSets.find(x);
        unsigned int set_y = dSets.find(y);
        if (set_x != set_y) {
            dSets.join(set_x, set_y);
            v[x].push_back(make_pair(y, it->weight));
            v[y].push_back(make_pair(x, it->weight));
        }
    }
    return v;
}

/**
 * Modified DFS algorithm
 * returns highest edge weight in path from s to t
 * returns unsigned int max value if t in unreachable from s
 */
unsigned int findMaxEdge(vector<vector<pair<unsigned int, unsigned int> > > mst, unsigned int s, unsigned int t, vector<int> &visited) {
    visited[s] = 1; // s is visited
    if (s == t) { // found t
        return 0;
    }
    for (vector<pair<unsigned int, unsigned int> >::iterator it = mst[s].begin(); it != mst[s].end(); it++) {
        if (visited[(*it).first] == 0) {
            unsigned int m = findMaxEdge(mst, (*it).first, t, visited); // first is destiny, second is weight
            if (m < numeric_limits<unsigned int>::max()) { // if is on correct path
                return max(m, (*it).second);
            }
        }
    }

    visited[s] = 0; // s is unvisited for future paths
    return numeric_limits<unsigned int>::max(); // didn't found vertex t on current path
}

int main() {
    graph g = readGraph();
    vector<pair<unsigned int, unsigned int> > pairs = readPairs();
    vector<vector<pair<unsigned int, unsigned int> > > mst = kruskal(g);

    for (unsigned int i = 0; i < pairs.size(); i++) {
        vector<int> visited(g.size, 0);
        cout << findMaxEdge(mst, pairs[i].first, pairs[i].second, visited) << endl;
    }

    return 0;
}