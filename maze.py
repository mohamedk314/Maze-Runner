import re
import copy

class Maze:
    # Define the Maze object by reading the maze from a mapfile
    def __init__(self, mapfile):
        self.mapfile = mapfile
        self.__wall = '%'
        self.__firstPoint = 'P'
        self._pointChar = '.'
        self.__first = None
        self._point = []
        # Read file and get maze map.
        with open(mapfile) as file:
            eachlines = file.readlines()

        eachlines = list(filter(lambda x: not re.match(r'^\s*$', x), eachlines))
        eachlines = [list(line.strip('\n')) for line in eachlines]
        self.lines = eachlines

        self.rows = len(eachlines)
        self.cols = len(eachlines[0])
        self.mazeRaw = eachlines

        if (len(self.mazeRaw) != self.rows) or (len(self.mazeRaw[0]) != self.cols):
            print("Maze dimensions incorrect")
            raise SystemExit
            return

        for row in range(len(self.mazeRaw)):
            for col in range(len(self.mazeRaw[0])):
                if self.mazeRaw[row][col] == self.__firstPoint:
                    self.__first = (row, col)
                    print()
                elif self.mazeRaw[row][col] == self._pointChar:
                    self._point.append((row, col))

    def getlines(self):
        return self.lines
    # Get True if the given position is the location of a wall
    def checkWall(self, row, col):
        return self.mazeRaw[row][col] == self.__wall

    # Get True if the given position is the location of an objective
    def checkObj(self, row, col):
        return (row, col) in self._point

    # Get the start position as a tuple of (row, column)
    def getFirst(self):
        return self.__first

    # Get the dimensions of the maze as a (row, column) tuple
    def getDimensions(self):
        return (self.rows, self.cols)

    # Get the list of objective positions of the maze
    def getObj(self):
        return copy.deepcopy(self._point)

    def setObjectives(self, objectives):
        self._point = objectives

    # Check if the pacman can move into a specific row and column
    def checkValid(self, row, col):
        return row >= 0 and row < self.rows and col >= 0 and col < self.cols and not self.checkWall(row, col)
        
    # Get list of neighboing squares that can be moved to from the given row,col
    def getnear(self, row, col):
        possibleNeighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1)
        ]
        neighbors = []
        for r, c in possibleNeighbors:
            if self.checkValid(r,c):
                neighbors.append((r,c))
        return neighbors

    def dfs_getnear(self, row, col):
        possibleNeighbors = [
            (row + 1, col),
            (row, col + 1),
            (row - 1, col),
            (row, col - 1)
        ]
        neighbors = []
        for r, c in possibleNeighbors:
            if self.checkValid(r,c):
                neighbors.append((r,c))
        return neighbors