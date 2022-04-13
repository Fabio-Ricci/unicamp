from copy import deepcopy
from random import choice, choices, random, seed
from IPython.display import clear_output
#import matplotlib.pyplot as plt

import gc

import pacman
import textDisplay
import graphicsDisplay

class Node:
    functions = {
        "max": lambda before, after: max(before, after),
        "min": lambda before, after: min(before, after),
        "mean": lambda before, after: (before + after) / 2,
        "sum": lambda before, after: before + after,
        "sub": lambda before, after: before - after,
        "mul": lambda before, after: before * after,
        "div": lambda before, after: before / after if after != 0 else 1,
    }
    consts = [-1.0, 0.0, 0.1, 0.5, 2.0, 5.0, 10.0]

    def __init__(self, func, before=None, after=None):
        self.function = func
        self.is_leaf = func not in Node.functions
        self.depth = 1
        self.before = None
        self.after = None
        self.set_before(before)
        self.set_after(after)
    def __call__(self, sensors={}):
        if self.is_leaf:
            if type(self.function) == str:
                assert self.function in sensors, "Leaf function not found in sensors dictionary"
                return sensors[self.function]
            return self.function
        return Node.functions[self.function](self.before(sensors), self.after(sensors))
    def set_before(self, node):
        self.before = node
        if node:
            self.depth = max(node.depth, self.after.depth if self.after else 0) + 1
    def set_after(self, node):
        self.after = node
        if node:
            self.depth = max(node.depth, self.before.depth if self.before else 0) + 1
    def __repr__(self, depth=0):
        if self.is_leaf:
            return "  "*depth + f"{self.function}"
        return "  "*depth + f"{self.function}(\n{self.before.__repr__(depth+1)},\n{self.after.__repr__(depth+1)}\n" + "  "*depth + ")"
    def list_branches(self, min_depth=2):
        assert min_depth >= 2, "min_depth must be at least 2"
        if self.depth < min_depth:
            return []
        return [self] + self.before.list_branches(min_depth) + self.after.list_branches(min_depth)
    def __deepcopy__(self, memo=None):
        if self.is_leaf:
            return Node(self.function)
        return Node(self.function, deepcopy(self.before), deepcopy(self.after))

class EvolutionaryForest:
    def __init__(self, mutation_rate=0.2, crossover_rate=0.7, population_size=1000, tournament_size=10, max_generations=0, possible_sensors=[], genes_size=1, elite_size=5):
        self.max_depth = 20
        self.elite_size = elite_size
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.max_generations = max_generations
        self.population_size = population_size
        self.possible_terminals = possible_sensors + Node.consts
        self.possible_primitives = list(Node.functions.keys())
        #
        self.population = [{
            "genes": [self.generate_random_tree(5,10) for _ in range(genes_size)],
            "fitness": 0
        } for _ in range(population_size)]
    
    def evaluate(self):
        for idx,ind in enumerate(self.population):
            fitness = sum([gene() for gene in ind["genes"]])
            x = ind["genes"][0]()
            func = abs(x**2 - 2)
            fitness = (1 / func) if func != 0 else float('inf')
            ind["fitness"] = fitness
    
    def evolve(self, epochs=1):
        for epoch in range(epochs):
            self.evaluate()
            best_ind = sorted(self.population, key=lambda x: x["fitness"])[-1]
            print(f"Generation {epoch} of {epochs}")
            gene = best_ind['genes'][0]
            #f"Fitness: {best_ind['fitness']}, 
            print(f"gene depth: {gene.depth}, gene value: {gene()}")
            self.next_generation()
    
    def select_roulette(self):
        # roulette method with applied linear normalization
        return choices(self.population, weights=[idx+1 for idx,_ in enumerate(self.population)])[0]
        
    def select_tournament(self):
        tournament_group = [choice(self.population) for _ in range(self.tournament_size)]
        return sorted(tournament_group, key=lambda x: x["fitness"])[-1]
    
    def select_couples(self, num_couples):
        for _ in range(num_couples):
            ind1 = self.select_roulette()
            ind2 = self.select_tournament()
            yield ind1, ind2

    def next_generation(self):
        self.population = sorted(self.population, key=lambda x: x["fitness"])
        new_population = self.population[-self.elite_size:]
        num_couples = (self.population_size - self.elite_size) // 2
        for ind1, ind2 in self.select_couples(num_couples):
            new_population.extend(self.breed(ind1, ind2))

        self.population = new_population

    def breed(self, ind1, ind2):
        new_ind1 = {"genes": [], "fitness": 0}
        new_ind2 = {"genes": [], "fitness": 0}
        
        for gene1, gene2 in zip(ind1['genes'], ind2['genes']):
            rand = random()
            
            if rand < self.mutation_rate + self.crossover_rate:
                new_gene1, new_gene2 = self.crossover(gene1, gene2)
                
                if rand < self.mutation_rate:
                    self.mutate(new_gene1)
                    self.mutate(new_gene2)
                    
                new_ind1["genes"].append(new_gene1)
                new_ind2["genes"].append(new_gene2)
            else:
                new_ind1["genes"].append(gene1)
                new_ind2["genes"].append(gene2)
                
        return new_ind1, new_ind2

    def mutate(self, gene):
        root = gene
        path_tree = [root]
        y = 1 / root.depth
        subtree = root.before if random() < 0.5 else root.after
        while random() > y and not subtree.is_leaf:
            path_tree.append(subtree)
            y = 1 / subtree.depth
            subtree = subtree.before if random() < 0.5 else subtree.after

        tree = path_tree[-1]
        d = random() < 0.5
        if subtree.is_leaf:
            new_subtree = self.generate_random_tree(1,min(3, self.max_depth - tree.depth))
            if d:
                tree.set_after(new_subtree)
            else:
                tree.set_before(new_subtree)
        else:
            if random() < 0.5:
                if d:
                    max_random_tree_depth = min(3, self.max_depth - tree.before.depth + 1)
                    new_subtree = self.generate_random_tree(1,max_random_tree_depth)
                    tree.set_after(new_subtree)
                else:
                    max_random_tree_depth = min(3, self.max_depth - tree.after.depth + 1)
                    new_subtree = self.generate_random_tree(1,max_random_tree_depth)
                    tree.set_before(new_subtree)
            else:
                subtree.function = choice(self.possible_primitives)
        
        # Update depth for all nodes when mutation is over
        while len(path_tree):
            tree = path_tree.pop()
            tree.depth = max(tree.before.depth, tree.after.depth) + 1

        return root

    def crossover(self, gene1, gene2):
        try:
            # gene1 chooses random subtree from gene2
            # gene1 decides where to put this subtree according to depth and max_depth
            copy1, copy2 = (deepcopy(gene1), deepcopy(gene2)) if gene1.depth < gene2.depth else (deepcopy(gene2), deepcopy(gene1))

            rand = random()
            tree1 = choice(copy1.list_branches())
            subtree1 = tree1.before if rand < 0.5 else tree1.after

            tree2 = choice([tree for tree in copy2.list_branches(min_depth=subtree1.depth+1) if tree.before.depth == subtree1.depth or tree.after.depth == subtree1.depth])
            if tree2.before.depth == subtree1.depth and tree2.after.depth == subtree1.depth:
                if rand < 0.5:
                    subtree2 = tree2.before
                    tree2.set_before(subtree1)
                else:
                    subtree2 = tree2.after
                    tree2.set_after(subtree1)
            elif tree2.before.depth == subtree1.depth:
                subtree2 = tree2.before
                tree2.set_before(subtree1)
            else:
                subtree2 = tree2.after
                tree2.set_after(subtree1)

            if rand < 0.5:
                tree1.set_before(subtree2)
            else:
                tree1.set_after(subtree2)
            return copy1, copy2
        except:
            print(f"gene1: {gene1}\n\ngene2: {gene2}\n\ntree1: {tree1}\n\nsubtree1: {subtree1}\n\n")
            return gene1, gene2

    def generate_random_tree(self, min_depth, max_depth):
        my_depth = choice(range(min_depth,max_depth+1))

        if my_depth == 1: #is_leaf
            return Node(choice(self.possible_terminals))

        root = Node(choice(self.possible_primitives))
        direction = choice([0,1]) # 0: before, 1: after

        if direction == 0:
            root.set_before(self.generate_random_tree(my_depth-1, my_depth-1))
            root.set_after(self.generate_random_tree(1, my_depth-1))
        else:
            root.set_after(self.generate_random_tree(my_depth-1, my_depth-1))
            root.set_before(self.generate_random_tree(1, my_depth-1))

        return root

class EvolutionaryPacman(EvolutionaryForest):
    def __init__(self, layout="smallClassic", population_size=500, mutation_rate=0.2, crossover_rate=0.7):
        possible_sensors = [
            "dist_to_next_food",
            "dist_to_next_pill",
            "dist_to_edible_ghost",
            "dist_to_non_edible_ghost",
            "dist_to_next_junction",
            "ghost_before_junction",
            "pill_before_ghost",
            "count_food",
            "count_pill",
            "count_edible_ghost",
            "count_non_edible_ghost",
            "count_junction"
        ]

        super().__init__(possible_sensors=possible_sensors, mutation_rate=mutation_rate, crossover_rate=crossover_rate, population_size=population_size)

        self.layout = layout

    def getGameArgs(self, ind, num_games=5, show_graphics=False):
        layout = pacman.layout.getLayout(self.layout)

        GeneticAgent = pacman.loadAgent("GeneticAgent", True)
        pacmanGene = ind["genes"][0] # Node (....)
        pacmanAgent = GeneticAgent(pacmanGene) # todo genes

        ghostType = pacman.loadAgent("RandomGhost", True) #"RandomGhost"
        ghosts = [ghostType( i+1 ) for i in range( 2 )]

        graphics = graphicsDisplay.PacmanGraphics(1.0, frameTime = 0.1)
        no_graphics = textDisplay.NullGraphics()
        display = graphics if show_graphics else no_graphics

        record = False

        return {
            "layout": layout, 
            "pacman": pacmanAgent, 
            "ghosts": ghosts,
            "display": display,
            "numGames": num_games, 
            "record": record
        }
    
    def run_games(self, idx, ind):
        print(f"Evaluating individual {idx+1} of {self.population_size}...")
        games = pacman.runGames(**self.getGameArgs(ind))

        games_fitness = []
        avg_score = 0
        for game in games:
            food_matrix = game.state.getFood()
            food_non_eaten = 0
            for row in food_matrix:
                for food in row:
                    food_non_eaten += 1 if food else 0
            
            avg_score += game.state.getScore()
            fitness_score = game.state.getScore() - 10*food_non_eaten
            games_fitness.append(fitness_score)
        
        avg_score = avg_score / float(len(games_fitness))
        average_fitness = sum(games_fitness) / float(len(games_fitness))
        ind["fitness"] = average_fitness
        print(f"Average score: {avg_score}")

    def evaluate(self):
        for idx,ind in enumerate(self.population):
            self.run_games(idx,ind)

    def evolve(self, epochs=1):
        best_fitness = []
        worst_fitness = []
        avg_fitness = []
        for epoch in range(epochs):
            print(f"Generation: {epoch+1}")
            self.evaluate()
            sorted_inds = sorted(self.population, key=lambda x: x["fitness"])
            best_fitness.append(sorted_inds[-1]["fitness"])
            worst_fitness.append(sorted_inds[0]["fitness"])
            avg_fitness.append(sum([ind["fitness"] for ind in self.population])/len(self.population))
            #clear_output(wait=True)
            print(f"Generation {epoch+1} of {epochs} complete.")
            if self.stop_criteria(sorted_inds[-3:]):
                break
            # print(f"Best fitness: {best_ind['fitness']}")
            # print(f"Max gene-tree depth: {max(gene.depth for gene in best_ind['genes'])}")
            self.next_generation()
            gc.collect(2)
    
        #clear_output(wait=True)
        plt.plot(best_fitness, 'g', label="Best Fitness")
        plt.plot(worst_fitness, 'r', label="Worst Fitness")
        plt.plot(avg_fitness, 'b', label="Avg Fitness")
        plt.show()

    def stop_criteria(self, best_inds):
        for num, potential_ind in enumerate(best_inds):
            if potential_ind["fitness"] > 1000:
                print(f"Testing ind number: {num}")
                games = pacman.runGames(**self.getGameArgs(potential_ind, num_games=30))
                wins = [game for game in games if game.state.isWin()]
                print(f"Won: {len(wins)}/{len(games)}")
                return len(wins) >= 0.9*len(games)

if __name__ == "__main__":
    evolPacmanSmall = EvolutionaryPacman(layout="smallClassic", population_size=200)
    evolPacmanSmall.evolve(20)