import pygame
import argparse

from pygame.locals import *
from maze import Maze
from algorithm import algori

class Application:
    def __init__(self, trans):
        self.run = True
        self.surface = None
        self.trans = trans
        self.windowTitle = "Maze : "
    
    # Initializes the pygame context and certain properties of the maze
    def initialize(self, mapfile):

        self.windowTitle += mapfile
        # Initial the maze
        self.maze = Maze(mapfile)
        # Get maze board
        self.grid = self.maze.getDimensions()
        # Get size of maze board
        self.w_height = self.grid[0] * self.trans
        self.w_width = self.grid[1] * self.trans

        self.squareSizeX = int(self.w_width / self.grid[1])
        self.squareSizeY = int(self.w_height / self.grid[0])
        # Get wall for print result on terminal
        self.term_walls = []
        eachlines = self.maze.getlines()
        for i in range(self.grid[0]):
            row = []
            for j in range(self.grid[1]):
                try:
                    if eachlines[i][j] == "P":
                        self.start = (i, j)
                        row.append(False)
                    elif eachlines[i][j] == '.':
                        self.goal = (i, j)
                        row.append(False)
                    elif eachlines[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.term_walls.append(row)
        self.solution = None

    # Once the application is initiated, execute is in charge of drawing the game and dealing with the game loop
    def execute(self, mapfile, Method):
        self.initialize(mapfile)
        # Check the maze
        if self.maze is None:
            print("No maze created")
            raise SystemExit
        # Pring maze panel
        self.solution = []
        print("Maze : ")
        self.term_print()
        # Get result of maze
        path, statesExplored = algori(self.maze, Method)
        self.solution = path
        # initial the pygame for display
        pygame.init()
        self.surface = pygame.display.set_mode((self.w_width, self.w_height), pygame.HWSURFACE)
        self.surface.fill((255, 255, 255))
        pygame.display.flip()
        pygame.display.set_caption(self.windowTitle)
        # print the result on terminal
        print("Results")
        print("Cost : ", len(path))
        print("Number of nodes : ",statesExplored)
        self.term_print()
        # Draw the result as pygame
        self.drawPath(path)
        self.drawMaze()
        pygame.display.flip()

        while self.run:
            pygame.event.pump()            
            keys = pygame.key.get_pressed()

            if (keys[K_ESCAPE]):
                    raise SystemExit

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
    # Implementation of a color scheme for the path taken
    def pathColor(self, length, index):
        firstColor = (255, 0, 0)
        lastColor = (0, 255, 0)
        rcolor = (lastColor[0] - firstColor[0]) / length
        gcolor = (lastColor[1] - firstColor[1]) / length
        bcolor = (lastColor[2] - firstColor[2]) / length
        red = firstColor[0] + index * rcolor
        green = firstColor[1] + index * gcolor
        blue = firstColor[2] + index * bcolor
        return (red, green, blue)

    # Draws the path (given as a list of (row, col) tuples) to the display context
    def drawPath(self, path):
        for p in range(len(path)):
            color = self.pathColor(len(path), p)
            self.circle(path[p][0], path[p][1], color)

    # Simple wrapper for drawing a wall as a rectangle
    def wall(self, row, col):
        pygame.draw.rect(self.surface, (0, 0, 0), (col * self.squareSizeX, row * self.squareSizeY, self.squareSizeX, self.squareSizeY), 0)

    # drawing a circle
    def circle(self, row, col, color, radius=None):
        if radius is None:
            radius = min(self.squareSizeX, self.squareSizeY) / 4
        pygame.draw.circle(self.surface, color, (int(col * self.squareSizeX + self.squareSizeX / 2), int(row * self.squareSizeY + self.squareSizeY / 2)), int(radius))

    # Draws the full maze to the display context
    def drawMaze(self):
        for row in range(self.grid[0]):
            for col in range(self.grid[1]):
                if self.maze.checkWall(row, col):
                    self.wall(row, col)
        row, col = self.maze.getFirst()
        pygame.draw.rect(self.surface, (0, 0, 255), (int(col * self.squareSizeX + self.squareSizeX / 4), int(row * self.squareSizeY + self.squareSizeY / 4),  int(self.squareSizeX * 0.5), int(self.squareSizeY * 0.5)), 0)
        for obj in self.maze.getObj():
            self.circle(obj[0], obj[1], (0, 0, 0))

    def term_print(self):
        # solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.term_walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("P", end="")
                elif (i, j) == self.goal:
                    print('.', end="")
                elif (i, j) in self.solution:
                    print(".", end="")
                else:
                    print(" ", end="")
            print()
        print()

if __name__ == "__main__":

    # Part of the args for get parameters for running
    args = argparse.ArgumentParser()

    args.add_argument('mapfile')
    args.add_argument('--method', dest="Type", type=str, default = "bfs",
                        choices = ["bfs", "dfs", "greedy", "astar"], help='search method - default bfs')
    params = args .parse_args()
    maze_app = Application(trans=20)
    maze_app.execute(params.mapfile, params.Type)
