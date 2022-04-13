#include "solver.h"

double getDistance(Point p1, Point p2){
	double delta_x = p1.x - p2.x;
	double delta_y = p1.y - p2.y;

	return sqrt(delta_x * delta_x + delta_y * delta_y);
}

vector<int> solveBottomUp(Instance &instance, int timelimit, chrono::high_resolution_clock::time_point &started){
    double **dist = new double *[instance.n];
    for (int i = 0; i < instance.n; i++) {
        dist[i] = new double[instance.n];
        for (int j = 0; j < instance.n; j++) {
            dist[i][j] = getDistance(instance.points[i], instance.points[j]);
        }
    }

    No **dp = new No *[(1 << instance.n)];
    for (int i = 0; i < (1 << instance.n); i++) {
        dp[i] = new No[instance.n];
    }

    for (int i = 0; i < instance.n; i++) {
        dp[0][i].cost = dist[0][i];
        dp[0][i].origin = 0;
    }

    for (int mask = 1; mask < (1<<instance.n); mask++) { // montar a tabela dp
        for (int i = 0; i < instance.n; i++) {
            double minCost = numeric_limits<double>::max();
            int minOrigin = 0;
            int currentOrigin = 0;
            for (int origin = mask; origin > 0; origin = (origin>>1)) { // testa todas as possibilidade de origem para o set atual
                if (origin % 2) { // o primeiro foi visitado (bit menos significativo da mascara)
                    int w = (mask & (INT_MAX - (1<<currentOrigin)));
                    double newCost = dist[i][currentOrigin] + dp[w][currentOrigin].cost;
                    if (newCost < minCost) {
                        minCost = newCost;
                        minOrigin = currentOrigin;
                    }
                }
                currentOrigin++;
            }
            dp[mask][i].cost = minCost;
            dp[mask][i].origin = minOrigin;
        }
    }

    // recuperar o caminho
    vector<int> path;
    int visited = ~((1<<(instance.n)) - 1); // preenche com zeros até a posicao 2^n
    visited++; // marca primeiro ponto como visitado
    for (int i = 0, origin = instance.n - 1; i < instance.n - 1; i++) {
        origin = dp[~visited][origin].origin;
        path.push_back(origin);
        visited += (1<<origin);
    }

    reverse(path.begin(), path.end());
    path.pop_back(); // remover o ultimo

    return path;
}

Path getMinPath(Instance &instance, double **dist, Path **mem, int pos, int mask) {
    Path minPath;
    if (mask == (((1 << instance.n) - 1) - (1 << instance.n - 1))) {
        minPath.cost = dist[pos][instance.n - 1];
        minPath.path.push_back(pos);
        return minPath;
    }

    if (mem[mask][pos].cost != -1) {
        return mem[mask][pos];
    }

    minPath.cost = numeric_limits<double>::max();
    for (int i = 1; i < instance.n - 1; i++) {
        if ((mask & (1 << i)) == 0) { // nao visitado
            Path path = getMinPath(instance, dist, mem, i, mask | (1 << i));
            double newCost = dist[pos][i] + path.cost;
            if (newCost < minPath.cost) {
                minPath.path = path.path;
                minPath.path.push_back(pos);
                minPath.cost = newCost;
            }
        }
    }

    return mem[mask][pos] = minPath;
}

vector<int> solveTopDown(Instance &instance, int timelimit, chrono::high_resolution_clock::time_point &started){
    double **dist = new double *[instance.n];
    for (int i = 0; i < instance.n; i++) {
        dist[i] = new double[instance.n];
        for (int j = 0; j < instance.n; j++) {
            dist[i][j] = getDistance(instance.points[i], instance.points[j]);
        }
    }

    Path **mem = new Path *[(1 << instance.n)];
    for (int i = 0; i < (1 << instance.n); i++) {
        mem[i] = new Path[instance.n];
        for (int j = 0; j < instance.n; j++) {
            Path path;
            path.cost = -1;
            mem[i][j] = path;
        }
    }

    Path minPath = getMinPath(instance, dist, mem, 0, 1);

    minPath.path.pop_back(); // remover o 0
    reverse(minPath.path.begin(), minPath.path.end());

    return minPath.path;
}
