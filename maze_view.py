import pygame
import maze
from pygame.locals import *
from collections import defaultdict
from time import sleep

BG_COLOR = 0, 0, 0
WALL_COLOR = 200, 200, 255
START_COLOR = 255, 255, 255
END_COLOR = 255, 165, 0

BLOCK_SIZE = 20
MARK_SIZE = 4
MARK_PADDING = BLOCK_SIZE - MARK_SIZE
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                     (0, 255, 255), (255, 255, 0), (255, 0, 255)]


class MazeView(object):

    '''
    A view for a Maze class with runners.
    '''

    def __init__(self, maze, runners=None):
        ''' Initialize view for given maze with given runners. '''
        self.maze = maze
        self.runners = runners or list()

        self.height = maze.rows * BLOCK_SIZE
        self.width = maze.cols * BLOCK_SIZE

        self.window = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.display.get_surface()

        self.reset()

    def reset(self):
        ''' Resets all the runs for the view.'''
        self.visits = defaultdict(list)
        self.runs = []
        for runner in self.runners:
            self.runs.append(runner.search_maze(self.maze))

        if self.runs:
            self.running = True
        self.draw_maze()

    def step(self):
        ''' Move all the runs one step, and append to visits.'''
        for idx, run in enumerate(self.runs):
            try:
                next_loc = next(run)
                self.visits[next_loc].append(idx)
            except StopIteration:
                self.runs.remove(run)
        if not self.runs:
            self.running = False

        self.draw_visits()

    def draw_visits(self):
        for visit in self.visits:
            for visitor in self.visits[visit]:
                rect = self.get_block(*visit, padding=MARK_PADDING)
                offset = MARK_SIZE * (-2 + visitor)
                rect.move_ip(offset, offset)
                pygame.draw.rect(self.screen, COLORS[visitor], rect)
        pygame.display.flip()

    def get_block(self, row, col, padding=0):
        row, col = row*BLOCK_SIZE + padding / 2, col*BLOCK_SIZE + padding / 2
        rect = Rect(col, row, BLOCK_SIZE - padding,
                                        BLOCK_SIZE - padding)
        return rect

    def draw_maze(self):
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                rect = self.get_block(row, col)
                if self.maze[row][col] == maze.WALL:
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                if (row, col) == self.maze.start:
                    pygame.draw.rect(self.screen, START_COLOR, rect)
                if (row, col) == self.maze.end:
                    pygame.draw.rect(self.screen, END_COLOR, rect)
        pygame.display.flip()

if __name__ == '__main__':
    m = maze.Maze.FromFile('maze2.txt')
    r = maze.MazeRunner()
    r2 = maze.MazeRunner()
    r3 = maze.MazeRunner()
    r5 = maze.MazeRunner()
    r4 = maze.MazeRunner()
    view = MazeView(m, [r, r2, r3, r4, r5])
    while view.running:
        view.step()
        sleep(0.2)
    input()

