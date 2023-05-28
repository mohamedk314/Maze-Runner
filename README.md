# MazeRunner
This Algorithm lets you find a path through any maze using the following algorithms : DFS, BFS. Greedy and A* .
It will help you find the path cost with the number of expanded nodes and create a visual of the maze using pygame.


Installation

  Install XCode
  
In your Terminal app, run the following command to install XCode and its command-line tools:
$ xcode-select --install

It is a large program so this may take a while to download. Make sure to click through all the confirmation prompts that XCode requires.

Install Homebrew

Next install Homebrew by copy/pasting the following command into Terminal and then type Enter:

$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

To confirm Homebrew installed correctly, run this command:

$ brew doctor
Your system is ready to brew.

Install Python 3

Now we can install the latest version of Python 3. Type the following command into Terminal and press Enter:
$ brew install python3

To confirm which version of Python 3 was installed, run the following command in Terminal:
$ python3 --version
Python 3.7.7

Install Pygame
$ pip install pygame

The installation will start at this point and you need to wait till the PyGame installation is done. You’ll know it’s done when you see a message  saying successfully installed pygame.

How To Run Guide

-Run the following command on your Terminal:

python main.py mediumMaze.txt --method bfs

You can change the maze by adding a sequence of maze to .txt file and instead of mediumMaze.txt, we can put the desired file.The algorithm works with 4 searches Depth-first Search, Breadth-first Search, Greedy Best-First Search and A* search.Method can be changed by changing the method name in the command to either dfs or bfs or greedy or astar.
