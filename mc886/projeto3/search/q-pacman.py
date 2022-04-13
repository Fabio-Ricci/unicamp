from copy import deepcopy
from random import choice, choices, random, seed
from IPython.display import clear_output
#import matplotlib.pyplot as plt

import gc

import pacman
import textDisplay
import graphicsDisplay

class QPacman:
    def __init__(self):
        LearningAgent = pacman.loadAgent("LearningAgent", True)
        self.pacman_agent = LearningAgent([-7.601506480015166, -102.44014366338222, -72.6036001197846, 21.856321021458953, 22.238553257816214, 0.6314606762760442])
        
    def getGameArgs(self, num_games=1, show_graphics=True):
        layout = pacman.layout.getLayout("originalClassic")

        ghostType = pacman.loadAgent("RandomGhost", True) #"RandomGhost"
        ghosts = [ghostType( i+1 ) for i in range( 4 )]

        graphics = graphicsDisplay.PacmanGraphics(1.0, frameTime = 0.01)
        no_graphics = textDisplay.NullGraphics()
        display = graphics if show_graphics else no_graphics

        record = False

        return {
            "layout": layout, 
            "pacman": self.pacman_agent, 
            "ghosts": ghosts,
            "display": display,
            "numGames": num_games, 
            "record": record
        }

    def run(self):
        for i in range(100):
            game = pacman.runGames(**self.getGameArgs())[0]
            if game.state.isLose():
                self.pacman_agent.update_weights(game.state)
                self.pacman_agent.set_first_state()
                print(self.pacman_agent.w)

if __name__ == "__main__":
    qpacman = QPacman()
    qpacman.run()