from collections import deque
import heapq as hq


class MazeRunner(object):

    '''
    A base class for the maze runners, with no search algorithm implemented.
    '''

    def __init__(self):
        self.reset()

    def __len__(self):
        return len(self.path)

    def reset(self):
        ''' Resets the node list and frontier.'''
        self.came_from = {}
        self.frontier = deque()
        self.path = []

    def search_maze(self, maze):
        raise NotImplemented("subclass and implement this!")

    def construct_path(self, loc):
        ''' Returns a list of all tiles visited to given loc, if possible.'''
        path = [loc]
        while self.came_from[loc]:
            loc = self.came_from[loc]
            path.append(loc)

        self.path = list(reversed(path))


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

            # If after the search we did not find anything, path will still be empty


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
            if self.path:
                # Return if a solution was already found
                return

            yield loc
            if loc == maze.end:
                # Build a path
                self.construct_path(loc)
                return

            neighbours = maze.get_neighbours(loc)
            neighbours = sorted(neighbours, key=lambda n: n[0] * 1 + n[1] * 10)
            for n in neighbours:
                if n not in self.came_from:
                    self.came_from[n] = loc
                    yield from search_maze_helper(n)

        self.reset()
        self.maze = maze
        self.came_from[maze.start] = None

        yield from search_maze_helper(maze.start)


class GreedyFirstRunner(MazeRunner):

    '''
    A Maze runner using a Greedy Best-First algorithm.
    maze Must have an endpoint for the search to work.
    '''

    def reset(self):
        ''' Resets the Greedy First-search runner. '''
        super().reset()
        self.frontier = []

    def push_to_frontier(self, loc, priority=0):
        hq.heappush(self.frontier, (priority, loc))

    def get_from_frontier(self):
        return hq.heappop(self.frontier)[1]

    def distance_heuristic(self, loc):
        ''' The distance heuristic used calculates the total distance of
            the x and y values from loc to the end. '''

        if not self.end:
            return 0
        return abs(self.end[0] - loc[0]) + abs(self.end[1] - loc[1])

    def search_maze(self, maze):
        ''' A generator that yields the next step in the maze
            until getting to the end, using a greedy Best-First algorithm.
            Maze must have an endpoint for the search to work.'''

        self.reset()
        self.maze = maze
        self.end = maze.end
        self.came_from[maze.start] = None
        self.push_to_frontier(maze.start)

        while self.frontier:
            current = self.get_from_frontier()
            yield current

            # If we found the end
            if current == maze.end:
                # Return the path to the end
                self.construct_path(current)
                return

            # Otherwise get all the new neighbours and add them to the frontier
            for neighbour in maze.get_neighbours(current):
                if neighbour not in self.came_from:
                    priority = self.distance_heuristic(neighbour)
                    self.push_to_frontier(neighbour, priority)
                    self.came_from[neighbour] = current

            # If There is no solution, path will still be empty
