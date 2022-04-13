# keyboardAgents.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Directions
import game
import random

class KeyboardAgent(Agent):
    """
    An agent controlled by the keyboard.
    """
    # NOTE: Arrow keys also work.
    WEST_KEY  = 'a'
    EAST_KEY  = 'd'
    NORTH_KEY = 'w'
    SOUTH_KEY = 's'
    STOP_KEY = 'q'

    def __init__( self, index = 0 ):

        self.lastMove = Directions.STOP
        self.index = index
        self.keys = []

    def getAction( self, state):
        from graphicsUtils import keys_waiting
        from graphicsUtils import keys_pressed
        keys = list(keys_waiting()) + list(keys_pressed())
        if keys != []:
            self.keys = keys

        legal = state.getLegalActions(self.index)
        move = self.getMove(legal)

        # if move == Directions.STOP:
        #     # Try to move in the same direction as before
        #     if self.lastMove in legal:
        #         move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal: move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        legal.remove(Directions.STOP)
        distance_next = self.calcDistances(state, legal)
        for action in legal:
            d = distance_next[action]["Junction"]
            char = ""
            if action == game.Directions.EAST:
                char = "E: "
            elif action == game.Directions.NORTH:
                char = "N: "
            elif action == game.Directions.WEST:
                char = "W: "
            elif action == game.Directions.SOUTH:
                char = "S: "
            print(f"{char}{int(10*d)}", end=" ")
        print()

        self.lastMove = move
        return move

    def calcDistances(self, state, legal, max_depth_value=5, not_found_value=10, inc_value=0.1):
        explorers = []
        distances = {}
        for action in legal:
            distances[action] = {
                "Food": not_found_value,
                "Pill": not_found_value,
                "NonEdibleGhost": not_found_value,
                "EdibleGhost": not_found_value,
                "Ghost": not_found_value,
                "Junction": not_found_value
            }
            xv, yv = self.directionToVector(action)
            x, y = state.getPacmanPosition()
            explorers.append({
                "a": action,
                "x": x+xv,
                "y": y+yv,
                "d": 0
            })
        
        grid = state.data.layout.walls.copy()

        while len(explorers) > 0:
            k = 0
            while k < len(explorers):
                explorer = explorers[k]
                action = explorer["a"]
                if distances[action]["Food"] == not_found_value and self.hasFood(state, explorer["x"], explorer["y"]):
                    distances[action]["Food"] = explorer["d"]
                if distances[action]["Pill"] == not_found_value and self.hasPill(state, explorer["x"], explorer["y"]):
                    distances[action]["Pill"] = explorer["d"]
                if distances[action]["Ghost"] == not_found_value and self.hasGhost(state, explorer["x"], explorer["y"]):
                    distances[action]["Ghost"] = explorer["d"]
                if distances[action]["EdibleGhost"] == not_found_value and self.hasEdibleGhost(state, explorer["x"], explorer["y"]):
                    distances[action]["EdibleGhost"] = explorer["d"]
                if distances[action]["NonEdibleGhost"] == not_found_value and self.hasNonEdibleGhost(state, explorer["x"], explorer["y"]):
                    distances[action]["NonEdibleGhost"] = explorer["d"]
                if distances[action]["Junction"] == not_found_value and self.hasJunction(state, explorer["x"], explorer["y"]):
                    distances[action]["Junction"] = explorer["d"]
                
                grid[explorer["x"]][explorer["y"]] = True

                can_go = self.possiblePositions(grid, explorer)
                for i in range(len(can_go)):
                    x, y = can_go[i]
                    if i == 0:
                        explorer["x"] = x
                        explorer["y"] = y
                        explorer["d"] += inc_value
                    else:
                        explorers.append({
                            "x": x,
                            "y": y,
                            "d": explorer["d"],
                            "a": explorer["a"],
                        })
                if not len(can_go) or explorer["d"] > max_depth_value:
                    del explorers[k]
                else:
                    k += 1
        return distances


    def directionToVector(self, direction):
        return {
            game.Directions.NORTH: (0, 1),
            game.Directions.SOUTH: (0, -1),
            game.Directions.EAST: (1, 0),
            game.Directions.WEST: (-1, 0),
        }[direction]

    def hasWall(self, state, x, y):
        try:
            return state.hasWall(x, y)
        except:
            return True

    def hasFood(self, state, x, y):
        return state.hasFood(x, y)

    def hasPill(self, state, x, y):
        return (x, y) in state.getCapsules()

    def hasGhost(self, state, x, y):
        return (x, y) in [
            (int(ghostState.getPosition()[0]), int(ghostState.getPosition()[1]))
            for ghostState in state.getGhostStates()
        ]

    def hasNonEdibleGhost(self, state, x, y):
        return (x, y) in [
            (int(ghostState.getPosition()[0]), int(ghostState.getPosition()[1]))
            for ghostState in state.getGhostStates()
            if ghostState.scaredTimer <= 0
        ]

    def hasEdibleGhost(self, state, x, y):
        return (x, y) in [
            (int(ghostState.getPosition()[0]), int(ghostState.getPosition()[1]))
            for ghostState in state.getGhostStates()
            if ghostState.scaredTimer > 0
        ]

    def hasJunction(self, state, x, y):
        return (
            sum(
                [
                    self.hasWall(state, x + x1, y + y1)
                    for x1 in range(-1, 2)
                    for y1 in range(-1, 2)
                    if x1 ^ y1 and x1 + y1
                ]
            )
            < 2
        )

    def possiblePositions(self, grid, explorer):
        directions = []
        x, y = explorer["x"], explorer["y"]

        if x+1 < grid.width and not grid[x+1][y]:
            directions.append((x+1,y))
        if x-1 >= 0 and not grid[x-1][y]:
            directions.append((x-1,y))
        if y+1 < grid.height and not grid[x][y+1]:
            directions.append((x,y+1))
        if y-1 >= 0 and not grid[x][y-1]:
            directions.append((x,y-1))
        
        return directions

    def ghostBeforeJunction(self, distance_next, direction):
        return distance_next[direction]["Ghost"] < distance_next[direction]["Junction"]

    def pillBeforeGhost(self, distance_next, direction):
        return distance_next[direction]["Pill"] < distance_next[direction]["Ghost"]

    def count(self, state, direction, what):
        has = {
            "Wall": self.hasWall,
            "Food": self.hasFood,
            "Pill": self.hasPill,
            "NonEdibleGhost": self.hasNonEdibleGhost,
            "EdibleGhost": self.hasEdibleGhost,
            "Ghost": self.hasGhost,
            "Junction": self.hasJunction,
        }
        count = 0
        x, y = state.getPacmanPosition()
        while not state.hasWall(x, y):
            vector = self.directionToVector(direction)
            x, y = x + vector[0], y + vector[1]
            if has[what](state, x, y):
                count += 0.1
        return count

    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        if   (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move

class KeyboardAgent2(KeyboardAgent):
    """
    A second agent controlled by the keyboard.
    """
    # NOTE: Arrow keys also work.
    WEST_KEY  = 'j'
    EAST_KEY  = "l"
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'
    STOP_KEY = 'u'

    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        if   (self.SOUTH_KEY in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move
