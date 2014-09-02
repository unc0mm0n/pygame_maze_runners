import pygame
import maze
import maze_runners as mr

from pygame.locals import *
from collections import defaultdict
import os

BG_COLOR = 100, 100, 100
WALL_COLOR = 200, 200, 200
START_COLOR = 255, 255, 255
END_COLOR = 255, 165, 0
BLOCK_COLOR = 0, 0, 0
COLORS = [(255, 0, 0), (0, 255, 0), (255, 0, 255),
                     (255, 255, 0), (255, 0, 255)]

BLOCK_SIZE = 20
FPS = 60


class MazeView(object):

    '''
    A view for a Maze class with runners.
    '''

    def __init__(self, maze, runners=None, block_size=None, mark_size=None):
        ''' Initialize view for given maze with given runners. '''
        self.maze = maze
        self.runners = runners or list()

        # Set block_size to default of needed
        self.block_size = block_size
        if not block_size:
            self.block_size = BLOCK_SIZE

        # Caulculate window sizer
        self.height = maze.rows * self.block_size
        self.width = maze.cols * self.block_size

        # Set mark size to default if needed
        if mark_size:
            self.mark_size = mark_size
        else:
            # default mark_size is calculated to exactly fit all runners.
            self.mark_size = self.block_size / len(self.runners)

        self.mark_padding = self.block_size - self.mark_size

        self.window = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.display.get_surface()
        self.timer = pygame.time.Clock()
        self.reset()

    def reset(self):
        ''' Resets all the runs for the view.'''
        self.visits = defaultdict(list)
        self.runs = []

        # For every runner given
        for runner in self.runners:
            # Create a new run generator using the runner's
            # seartch_maze method.
            self.runs.append(runner.search_maze(self.maze))

        if self.runs:
            # Set self to running as long as we have at least one run
            self.running = True
        self.draw_maze()

    def step(self):
        ''' Move all the runs one step, and append to visits.'''
        done = 0
        for idx, run in enumerate(self.runs):
            # For each of our runs.
            try:
                # Try to get the next location in the run
                next_loc = next(run)
                self.visits[next_loc].append(idx)
            except StopIteration:
                # keep track of the number of done runs.
                done += 1

        return(done)

        self.draw_visits()

    def run(self, winner=False):
        ''' Run all runners through the maze.
            If winner is set to True will exit when the first runner
            Reach the exit. '''
        if winner:
            goal = 1
        else:
            goal = len(self.runs)

        while self.step() < goal:
            self.draw_visits()
            self.timer.tick(FPS)

    def draw_visits(self):
        ''' draw all the given visits, each visit is a location as the key
            and a list of runners that visited it as value.'''
        for visit in self.visits:
            # for each visitor in each cell (idx number of runner from 0)
            for visitor in self.visits[visit]:
                # get a rect in the corret size
                rect = self.get_block(*visit, padding=self.mark_padding)

                # Calculate the location of the specific runner
                if len(self.runners) == 1:
                    runner_offset = 0
                else:
                    runner_offset = visitor / (len(self.runners) - 1) - 0.5

                # Calculate the offset by multiplying the offset of the current runner
                # With the initial padding used to determine the center location.
                offset = self.mark_padding * runner_offset
                # Move the rectangle in place by the offset

                rect.move_ip(offset, offset)
                pygame.draw.rect(self.screen, COLORS[visitor], rect)
                # Remove the visit so it won't get drawn again and again
                self.visits[visit].remove(visitor)
        pygame.display.flip()

    def get_block(self, row, col, padding=0):
        # Return the block at given location with given padding
        row = row*self.block_size + padding / 2
        col = col*self.block_size + padding / 2
        rect = Rect(col, row, self.block_size - padding, self.block_size - padding)
        return rect

    def draw_maze(self):
        self.screen.fill(BG_COLOR)

        # Iterate each cell in the maze
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                try:
                    # draw accoridng to it's value
                    rect = self.get_block(row, col)
                    if (row, col) == self.maze.start:
                        pygame.draw.rect(self.screen, START_COLOR, rect)
                    elif (row, col) == self.maze.end:
                        pygame.draw.rect(self.screen, END_COLOR, rect)
                    elif self.maze[row][col] == maze.WALL:
                        pygame.draw.rect(self.screen, WALL_COLOR, rect)
                    else:
                        rect = self.get_block(row, col, 1)
                        pygame.draw.rect(self.screen, BLOCK_COLOR, rect)
                except:
                    print('rogue coors ', row, col)
                    print(self.get_block(row, col))

        pygame.display.flip()

    def draw_path(self, path, color):
        ''' Draw given path (list of coordinates) on the maze.'''
        for loc in path:
            rect = self.get_block(*loc)
            pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "{}, {}".format(10, 30)

    from random import randint
    start, end = [(randint(0, 199), randint(0, 199)) for _ in range(2)]

    m = maze.Maze.FromFile('bird.txt')

    r1 = mr.AStarTiebreakRunner()
    r2 = mr.BreathRunner()
    r3 = mr.GreedyFirstRunner()
    r4 = mr.AStarRunner()
    view = MazeView(m, [r1])
    #r4.solve(m)
    #view.draw_path(r4.path, (255, 0, 0))
    #r1.solve(m)
    #view.draw_path(r1.path, (0, 0, 255))
    view.run()
    print('Breath ', len(r2), len(r2.came_from),
            '\ngreedy ', len(r3), len(r3.came_from),
            '\nA* ', len(r4), len(r4.came_from),
            '\nA* tiebreak ', len(r1), len(r1.came_from))

    input()
