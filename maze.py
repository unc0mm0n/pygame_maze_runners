from time import sleep
from random import random
import os

START = 'S'
END = 'E'
WALL = '+'


class Maze:

    '''
    A class representing a maze as a 2 dimensional list.
    '''

    @classmethod
    def FromFile(cls, mazeFileName):
        maze = []
        with open(mazeFileName, 'r') as mazeFile:
            start = tuple(int(i) for i in mazeFile.readline().split(','))
            end = tuple(int(i) for i in mazeFile.readline().split(','))
            for line in mazeFile:
                row = []
                for ch in line[:-1]:
                    row.append(ch)
                maze.append(row)

        return cls(maze, start, end)

    @classmethod
    def Random(cls, width, height, ratio, start=(0, 0), end=None):
        ''' Generate a maze randomly if given width and height.
            Higher ratio = more walls. '''
        if not end:
            end = (height - 1, width - 1)

        maze = []
        for y in range(height):
            row = []
            for x in range(width):
                if random() < ratio:
                    row.append(WALL)
                else:
                    row.append(' ')

            maze.append(row)

        maze[start[0]][start[1]] = ' '
        maze[end[0]][end[1]] = ' '

        return cls(maze, start, end)

    def __init__(self, maze, start, end=None):
        '''
        Initialize a maze using a 2 dimensional list
        where '+' marks an obstacle, a start location and an end location.
        Assumes all inner lists are the same size.
        '''

        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.start = start

        if self.is_valid_tile(*start):
            maze[start[0]][start[1]] = START
        else:
            raise ValueError("Invalid start location")

        if end and self.is_valid_tile(*end):
            maze[end[0]][end[1]] = END
            self.end = end
        else:
            self.end = None

    def draw_maze(self):
        for row in self.maze:
            for tile in row:
                print(tile, end='')
            print()

    def is_valid_tile(self, row, col):
        '''
        return True if maze[row][col] is inside the maze
        and is not a wall.
        '''
        if row >= self.rows or row < 0:
            return False
        if col >= self.cols or col < 0:
            return False
        if self[row][col] == WALL:
            return False
        return True

    def get_neighbours(self, loc):
        ''' Returns all neighbours of loc that aren't walls.'''
        row, col = loc
        neighbours = []
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dir in dirs:
            neighbour = (row + dir[0], col + dir[1])
            if self.is_valid_tile(*neighbour):
                neighbours.append(neighbour)

        return neighbours

    def __getitem__(self, idx):
        return self.maze[idx]

if __name__ == '__main__':
    from maze_runners import *

    m = Maze.Random(300, 300, 0.23, (50, 50), (298, 298))
    r1 = AStarRunner()

    for tile in r1.search_maze(m):

        continue

    print(r1.path)


