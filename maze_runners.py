from collections import deque


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
