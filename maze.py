from collections import deque
from time import sleep
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

    def __init__(self, maze, start, end):
        '''
        Initialize a maze using a 2 dimensional list
        where '+' marks an obstacle, a start location and an end location.
        Assumes all inner lists are the same size.
        '''

        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.start = start
        self.end = end
        maze[start[0]][start[1]] = START
        maze[end[0]][end[1]] = END

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


class MazeRunner(object):

    '''
    A maze runner is an object that finds the exit in the maze class,
    keeping it's own states.
    '''

    def __init__(self):
        self.reset()

    def reset(self):
        ''' Resets the node list and frontier.'''
        self.came_from = {}
        self.frontier = deque()

    def search_maze(self, maze):
        ''' A generator the yields the next step in the maze
            until getting to the end. '''

        self.reset()
        self.maze = maze
        self.came_from[maze.start] = None
        self.frontier.append(maze.start)

        while self.frontier:
            current = self.frontier.popleft()
            yield current

            # If we found the end
            if current == maze.end:
                # Return the path to the end
                self.construct_path(current)
                return

            # Otherwise get all the new neighbours and add them to the frontier
            for neighbour in maze.get_neighbours(current):
                if neighbour not in self.came_from:
                    self.frontier.append(neighbour)
                    self.came_from[neighbour] = current

            # If after the search we did not find anything
        self.path = False

    def construct_path(self, loc):
        ''' Returns a list of all tiles visited to given loc, if possible.'''
        path = [loc]
        while self.came_from[loc]:
            loc = self.came_from[loc]
            path.append(loc)

        self.path = reversed(path)

if __name__ == '__main__':
    myMaze = Maze.FromFile('maze2.txt')
    r1 = MazeRunner()

    for tile in r1.search_maze(myMaze):
        pass

    for tile in r1.path:
        os.system('cls')
        y, x = tile
        myMaze[y][x] = ':'
        myMaze.draw_maze()
        sleep(0.3)
