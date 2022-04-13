cmake_minimum_required(VERSION 3.7)
project(Trabalho_1)

set(CMAKE_C_STANDARD 99)

set(SOURCE_FILES src/main.c src/processarEntrada.c src/token.c src/emitirMapaDeMemoria.c)
add_executable(Trabalho_1 ${SOURCE_FILES})