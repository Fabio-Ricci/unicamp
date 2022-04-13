from pacman import Directions
from game import Agent
import random
import game
import util
from copy import copy
import pdb

class AgentUtils:
    @staticmethod
    def calcDistances(state, legal, max_depth_value=5, not_found_value=10, inc_value=0.1):
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
            xv, yv = AgentUtils.directionToVector(action)
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
                if distances[action]["Food"] == not_found_value and AgentUtils.hasFood(state, explorer["x"], explorer["y"]):
                    distances[action]["Food"] = explorer["d"]
                if distances[action]["Pill"] == not_found_value and AgentUtils.hasPill(state, explorer["x"], explorer["y"]):
                    distances[action]["Pill"] = explorer["d"]
                if distances[action]["Ghost"] == not_found_value and AgentUtils.hasGhost(state, explorer["x"], explorer["y"]):
                    distances[action]["Ghost"] = explorer["d"]
                if distances[action]["EdibleGhost"] == not_found_value and AgentUtils.hasEdibleGhost(state, explorer["x"], explorer["y"]):
                    distances[action]["EdibleGhost"] = explorer["d"]
                if distances[action]["NonEdibleGhost"] == not_found_value and AgentUtils.hasNonEdibleGhost(state, explorer["x"], explorer["y"]):
                    distances[action]["NonEdibleGhost"] = explorer["d"]
                if distances[action]["Junction"] == not_found_value and AgentUtils.hasJunction(state, explorer["x"], explorer["y"]):
                    distances[action]["Junction"] = explorer["d"]
                
                grid[explorer["x"]][explorer["y"]] = True
                i = 0
                for x, y in AgentUtils.possiblePositions(grid, explorer):
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
                    i += 1
                if i == 0 or explorer["d"] > max_depth_value:
                    del explorers[k]
                else:
                    k += 1
                    
        return distances

    @staticmethod
    def directionToVector(direction):
        return {
            game.Directions.NORTH: (0, 1),
            game.Directions.SOUTH: (0, -1),
            game.Directions.EAST: (1, 0),
            game.Directions.WEST: (-1, 0),
        }[direction]

    @staticmethod
    def hasWall(state, x, y):
        try:
            return state.hasWall(x, y)
        except:
            return True

    @staticmethod
    def hasFood(state, x, y):
        return state.hasFood(x, y)

    @staticmethod
    def hasPill(state, x, y):
        return (x, y) in state.getCapsules()

    @staticmethod
    def hasGhost(state, x, y):
        return (x, y) in [
            (int(ghostState.getPosition()[0]), int(ghostState.getPosition()[1]))
            for ghostState in state.getGhostStates()
        ]

    @staticmethod
    def hasNonEdibleGhost(state, x, y):
        return (x, y) in [
            (int(ghostState.getPosition()[0]), int(ghostState.getPosition()[1]))
            for ghostState in state.getGhostStates()
            if ghostState.scaredTimer <= 0
        ]

    @staticmethod
    def hasEdibleGhost(state, x, y):
        return (x, y) in [
            (int(ghostState.getPosition()[0]), int(ghostState.getPosition()[1]))
            for ghostState in state.getGhostStates()
            if ghostState.scaredTimer > 0
        ]

    @staticmethod
    def hasJunction(state, x, y):
        return (
            sum(
                [
                    AgentUtils.hasWall(state, x + x1, y + y1)
                    for x1 in range(-1, 2)
                    for y1 in range(-1, 2)
                    if x1 ^ y1 and x1 + y1
                ]
            )
            < 2
        )

    @staticmethod
    def possiblePositions(grid, explorer):
        x, y = explorer["x"], explorer["y"]

        if x+1 < grid.width and not grid[x+1][y]:
            yield (x+1,y)
        if x-1 >= 0 and not grid[x-1][y]:
            yield (x-1,y)
        if y+1 < grid.height and not grid[x][y+1]:
            yield (x,y+1)
        if y-1 >= 0 and not grid[x][y-1]:
            yield (x,y-1)

    @staticmethod
    def ghostBeforeJunction(distance_next, direction):
        return distance_next[direction]["Ghost"] < distance_next[direction]["Junction"]

    @staticmethod
    def pillBeforeGhost(distance_next, direction):
        return distance_next[direction]["Pill"] < distance_next[direction]["Ghost"]

    @staticmethod
    def count(state, direction, what, inc_value=0.1):
        has = {
            "Wall": AgentUtils.hasWall,
            "Food": AgentUtils.hasFood,
            "Pill": AgentUtils.hasPill,
            "NonEdibleGhost": AgentUtils.hasNonEdibleGhost,
            "EdibleGhost": AgentUtils.hasEdibleGhost,
            "Ghost": AgentUtils.hasGhost,
            "Junction": AgentUtils.hasJunction,
        }
        count = 0
        x, y = state.getPacmanPosition()
        while not state.hasWall(x, y):
            vector = AgentUtils.directionToVector(direction)
            x, y = x + vector[0], y + vector[1]
            if has[what](state, x, y):
                count += inc_value
        return count

    @staticmethod
    def countGhostAway(state, direction, what, step=1):
        has = {
            "NonEdibleGhost": AgentUtils.hasNonEdibleGhost,
            "EdibleGhost": AgentUtils.hasEdibleGhost,
        }
        count = 0
        x, y = state.getPacmanPosition()
        vector = AgentUtils.directionToVector(direction)
        x, y = x + vector[0], y + vector[1]
        
        if not AgentUtils.hasWall(state, x, y) and has[what](state, x, y):
            count += 1
        if not AgentUtils.hasWall(state, x+1, y) and has[what](state, x+1, y):
            count += 1
        if not AgentUtils.hasWall(state, x, y+1) and has[what](state, x, y+1):
            count += 1
        if not AgentUtils.hasWall(state, x-1, y) and has[what](state, x-1, y):
            count += 1
        if not AgentUtils.hasWall(state, x, y-1) and has[what](state, x, y-1):
            count += 1
        if step > 1:
            if not AgentUtils.hasWall(state, x+2, y) and has[what](state, x+2, y):
                count += 1
            if not AgentUtils.hasWall(state, x, y+2) and has[what](state, x, y+2):
                count += 1
            if not AgentUtils.hasWall(state, x-2, y) and has[what](state, x-2, y):
                count += 1
            if not AgentUtils.hasWall(state, x, y-2) and has[what](state, x, y-2):
                count += 1
            if not AgentUtils.hasWall(state, x+1, y-1) and has[what](state, x+1, y-1):
                count += 1
            if AgentUtils.hasWall(state, x+1, y+1) and has[what](state, x+1, y+1):
                count += 1
            if not AgentUtils.hasWall(state, x-1, y-1) and has[what](state, x-1, y-1):
                count += 1
            if not AgentUtils.hasWall(state, x-1, y+1) and has[what](state, x-1, y+1):
                count += 1

        return count

class EvolutionaryAgent(Agent):
    actions = [
        Directions.NORTH,
        Directions.SOUTH,
        Directions.WEST,
        Directions.EAST,
        Directions.STOP,
    ]

    def __init__(self, gene=None):
        self.gene = gene

    def getAction(self, state):
        legal_actions = state.getLegalPacmanActions()
        if Directions.STOP in legal_actions:
            legal_actions.remove(Directions.STOP)

        best = {"action": None, "score": float("-inf")}
        distance_next = AgentUtils.calcDistances(state, legal_actions) 
        for action in legal_actions:
            action_sensors = {
                "dist_to_next_food": distance_next[action]["Food"],
                "dist_to_next_pill": distance_next[action]["Pill"],
                "dist_to_edible_ghost": distance_next[action]["EdibleGhost"],
                "dist_to_non_edible_ghost": distance_next[action]["NonEdibleGhost"],
                "dist_to_next_junction": distance_next[action]["Junction"],
                "ghost_before_junction": AgentUtils.ghostBeforeJunction(distance_next, action),
                "pill_before_ghost": AgentUtils.pillBeforeGhost(distance_next, action),
                "count_food": AgentUtils.count(state, action, "Food"),
                "count_pill": AgentUtils.count(state, action, "Pill"),
                "count_edible_ghost": AgentUtils.count(state, action, "EdibleGhost"),
                "count_non_edible_ghost": AgentUtils.count(state, action, "NonEdibleGhost"),
                "count_junction": AgentUtils.count(state, action, "Junction"),
            }
            
            gene_score = self.gene(action_sensors)

            if gene_score > best["score"]:
                best["action"] = action
                best["score"] = gene_score

        return best["action"]

class LearningAgent(Agent):
    def __init__(self, weights, gamma=0.5, learning_rate=0.001):
        self.w = weights
        self.distances = None
        self.q = 0.0
        self.f = None
        self.prev_state = None
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.state = None
        self.first_state = True
        self.freeze_weights = False
        self.num_actions = 0
        self.mean_reward = 0

    def calc_f(self, action):
        ghost_near = AgentUtils.countGhostAway(self.state, action, "NonEdibleGhost", step=2) > 0
        food_near = self.distances[action]["Food"] <= 2
        return [
            self.distances[action]["Food"]*0.1,
            AgentUtils.countGhostAway(self.state, action, "NonEdibleGhost", step=1),
            AgentUtils.countGhostAway(self.state, action, "NonEdibleGhost", step=2),
            AgentUtils.countGhostAway(self.state, action, "EdibleGhost", step=1),
            AgentUtils.countGhostAway(self.state, action, "EdibleGhost", step=2),
            1 if food_near and not ghost_near else 0
        ]

    def calc_q(self, action):
        fs = self.calc_f(action)
        q = 0
        for fi, wi in zip(fs, self.w):
            q += wi*fi
        return q

    def restart(self):
        self.num_actions = 0
        self.mean_reward = 0
        self.first_state = True
    
    def _freeze_weights(self, freeze):
        self.freeze_weights = freeze

    def update_weights(self, state, best_q=0.0):
        if not self.freeze_weights:
            # calculate reward
            r = state.getScore() - self.prev_state.getScore()
            #compute diff
            difference = (r + self.gamma*best_q) - self.q

            for i in range(len(self.w)):
                self.w[i] = self.w[i] + self.learning_rate*difference*self.f[i]
            
            self.mean_reward += r

    def get_data(self):
        return self.mean_reward / self.num_actions, self.num_actions

    def getAction(self, state):
        self.state = state
        # get legal actions for pacman  
        legal_actions = state.getLegalPacmanActions()
        legal_actions.remove(Directions.STOP)  
        self.distances = AgentUtils.calcDistances(state, legal_actions, max_depth_value=200, not_found_value=500, inc_value=1)

        # pick best q to update weights
        # calculate best q and action 
        best = {"action": None, "q": None}
        for idx, action in enumerate(legal_actions):
            # q calculation expression
            qa = self.calc_q(action)
            if idx == 0:
                best["q"] = qa
                best["action"] = action
            elif qa > best["q"]:
                best["q"] = qa
                best["action"] = action

        #update weights
        if not self.first_state:
            self.update_weights(state, best["q"])

        # update state for future reward calculation and future weight update
        self.action = best["action"]
        self.q = best["q"]
        self.f = self.calc_f(self.action)
        self.prev_state = state
        self.first_state = False
        self.num_actions += 1

        return self.action
        
          