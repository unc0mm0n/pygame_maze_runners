import pygame
from collections import defaultdict

BG_COLOR = 0, 0, 0
WALL_COLOR = 255, 255, 255

BLOCK_SIZE = 20


class MazeView(object):

    '''
    A view for a Maze class with runners.
    '''

    def __init__(self, maze, runners=None):
        ''' Initialize view for given maze with given runners. '''
        self.maze = maze
        self.runners = runners

        self.height = maze.rows * BLOCK_SIZE
        self.width = maze.cols * BLOCK_SIZE
        self.reset()

    def reset(self):
        ''' Resets all the runs for the view.'''
        self.visits = defaultdict(list)
        self.runs = []
        for runner in self.runners:
            self.runs.append(runner.search_maze(self.maze))

    def step(self):
        ''' Move all the runs one step, and append to visits.'''
        for run, idx in enumerate(self.runs):
            try:
                next_loc = next(run)
                self.visits[next_loc].append(idx)
            except StopIteration:
                self.runs.remove(run)

    def draw(self):
        ''' Draws self to pygame screen. '''
