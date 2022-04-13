#ifndef SOLVER_H
#define SOLVER_H
#include <vector>
#include <map>
#include <cmath>
#include <bits/stdc++.h>
#include <algorithm>
#include <chrono>
#include <limits>
#include "point.h"
#include "instance.h"

#define M 32

using namespace std;

struct Path {
  vector<int> path;
  double cost;
};

struct No {
  double cost;
  int origin;
};

double getDistance(Point p1, Point p2);
vector<int> solveBottomUp(Instance &instance, int timelimit, chrono::high_resolution_clock::time_point &started);
Path getMinPath(Instance &instance, double **dist, double **mem, int pos, int mask);
vector<int> solveTopDown(Instance &instance, int timelimit, chrono::high_resolution_clock::time_point &started);
#endif // SOLVER_H
