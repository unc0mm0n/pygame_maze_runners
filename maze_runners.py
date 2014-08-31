from collections import deque


class MazeRunner(object):

    '''
    A base class for the maze runners, with no search algorithm implemented.
    '''

    def __init__(self):
        self.reset()

    def reset(self):
        ''' Resets the node list and frontier.'''
        self.came_from = {}
        self.frontier = deque()

    def search_maze(self, maze):
        raise NotImplemented("subclass and implement this!")

    def construct_path(self, loc):
        ''' Returns a list of all tiles visited to given loc, if possible.'''
        path = [loc]
        while self.came_from[loc]:
            loc = self.came_from[loc]
            path.append(loc)

        self.path = reversed(path)


class BreathRunner(MazeRunner):

    '''
    A maze runner for the maze class using the breath-first algorithm.
    '''

    def search_maze(self, maze):
        ''' A generator the yields the next step in the maze
            until getting to the end. using breath-first algorithm. '''

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


class RecursiveRunner(MazeRunner):

    '''
    A maze runner for the maze class using a procedural
    recursive algorithm.
    '''

    def search_maze(self, maze):
        ''' A generator the yields the next step in the maze
            until getting to the end, using recursive algorithm. '''

        def search_maze_helper(loc):
            ''' A recursive function to search through the maze. '''
            yield loc
            if loc == maze.end:
                print('out')
                self.path = self.construct_path(loc)
                return

            for n in maze.get_neighbours(loc):
                if n not in self.came_from:
                    self.came_from[n] = loc
                    yield from search_maze_helper(n)

            return

        self.reset()
        self.maze = maze
        self.came_from[maze.start] = None

        yield from search_maze_helper(maze.start)

        # If after the serach we did not find anything
        self.path = False
