cmake_minimum_required(VERSION 3.14)
project(lab01)

set(CMAKE_CXX_STANDARD 14)

include_directories(src)

add_executable(lab01
        src/instance.h
        src/main.cpp
        src/main.h
        src/point.h
        src/solver.cpp
        src/solver.h)
