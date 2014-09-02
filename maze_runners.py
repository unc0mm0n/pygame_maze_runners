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
        ''' Returns a list of all tiles visited to given loc, if possible.
            Return None otherwise. '''
        path = [loc]
        if loc not in self.came_from:
            return None
        while self.came_from[loc]:
            loc = self.came_from[loc]
            path.append(loc)

        return list(reversed(path))

    def solve(self, maze):
        ''' Return a path through a solved maze.'''
        for _ in self.search_maze(maze):
            pass
        return self.path


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
                self.path = self.construct_path(current)
                return

            # Otherwise get all the new neighbours and add them to the frontier
            for neighbour in maze.get_neighbours(current):
                if neighbour not in self.came_from:
                    self.frontier.append(neighbour)
                    self.came_from[neighbour] = current


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
                self.path = self.construct_path(loc)
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
    If no endpoint is given all cells .
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
        ''' The distance heuristic used calculates the
            expected distance from the end.
            Return 0 if no there's no end point. '''

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
                self.path = self.construct_path(current)
                return

            # Otherwise get all the new neighbours and add them to the frontier
            for neighbour in maze.get_neighbours(current):
                if neighbour not in self.came_from:
                    self.came_from[neighbour] = current
                    priority = self.distance_heuristic(neighbour)
                    self.push_to_frontier(neighbour, priority)


class AStarRunner(GreedyFirstRunner):

    ''' A Maze runner using the A* algorithm to find the shortest path.'''

    def search_maze(self, maze):
        ''' A generator that yields the next step in the maze
            until getting to the end, using a greedy Best-First algorithm.
            Maze must have an endpoint for the search to work.'''

        self.reset()

        self.maze = maze
        self.end = maze.end
        self.start = maze.start
        self.came_from[maze.start] = None
        self.push_to_frontier(maze.start)

        while self.frontier:
            current = self.get_from_frontier()
            yield current

            # If we found the end
            if current == maze.end:
                # Return the path to the end
                self.path = self.construct_path(current)
                return

            # Otherwise get all the new neighbours and add them to the frontier
            new_cost = len(self.construct_path(current)) + 1
            for neighbour in maze.get_neighbours(current):
                old_path = self.construct_path(neighbour)
                if not old_path or new_cost < len(old_path):
                    self.came_from[neighbour] = current
                    priority = new_cost + self.distance_heuristic(neighbour)
                    self.push_to_frontier(neighbour, priority)


class AStarTiebreakRunner(AStarRunner):

    ''' AStarRunner with a tiebreak inside the heuristic to prefer
        nodes closer to the goal.'''

    def distance_heuristic(self, loc):
        dist = super().distance_heuristic(loc)
        if dist == 0:
            return dist

        # Get the cross product of the vectors:
        # (start, end), (loc, end)
        # Which is also the area of the parallelogram formed by the vectors.
        dy1 = loc[0] - self.end[0]
        dx1 = loc[1] - self.end[1]
        dy2 = self.start[0] - self.end[0]
        dx2 = self.start[1] - self.end[1]
        cross = abs(dx1*dy2 - dx2*dy1)

        # Add the cross product as a small fraction to the calculation
        # to break ties by picking the node closer to a straight line
        # to the goal.
        # Note that this makes the heuristic inadmissable!
        # Though this will come into effect only in rare cases and where the expected
        # Path length is bigger than 1000.
        # This can be optimized by changing 0.001 to a smaller number that fits the
        # maze size.
        return dist + cross * 0.001
