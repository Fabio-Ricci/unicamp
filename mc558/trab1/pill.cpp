/** Fábio Camargo Ricci - 170781**/
#include <iostream>
#include <vector>
#include <queue>

using namespace std;

vector<vector<int> > readParams(int &n) {
    int m = 0;
    vector<vector<int> > v;
    cin >> n >> m;
    v.assign(n, vector<int>());
    int i, j;
    for (int k = 0; k < m; k++) {
        cin >> i >> j;
        v[i-1].push_back(j-1);
    }
    return v;
}

/**
 * Modified BFS algorithm
 * return true if Dotutama
 * return false if Dotutama or Doturacu
 * **/
bool verify_pill_visit(vector<vector<int> > &graph, int s, vector<int> &visited) {
    /**
     * -1 is unvisited
     * 0 is T or J
     * 1 is G or A
     */
    visited[s] = 0;
    queue<int> q;
    q.push(s);
    while (!q.empty()) {
        int vertex = q.front();
        for (vector<int>::iterator itr = graph[vertex].begin(); itr != graph[vertex].end(); ++itr) { // iterate over current vertex neighbours
            if (visited[*itr] == -1) { // unvisited
                visited[*itr] = !visited[vertex]; // vertex neighbours can't be the same color
                q.push(*itr);
            } else if (visited[*itr] == visited[vertex]) { // neighbour color is equal to current vertex color -> it's Dotutama (venom)
                return true;
            }
        }
        q.pop();
    }
    return false;
}

/**
 * Verify every connected component
 */
bool verify_pill(vector<vector<int> > graph) {
    vector<int> visited;
    visited.assign(graph.size(), -1);
    for (unsigned int u = 0; u < graph.size(); u++) {
        if (visited[u] == -1) {
            int venom = verify_pill_visit(graph, u, visited);
            if (venom) {
                return true;
            }
        }
    }
    return false;
}

int main() {
    int n = 0;
    vector<vector<int> > graph = readParams(n);
    if (graph.empty()) {
        return 1;
    }

    if (verify_pill(graph)) {
        cout << "dotutama" << endl;
    } else {
        cout << "doturacu ou dotutama" << endl;
    }

    return 0;
}