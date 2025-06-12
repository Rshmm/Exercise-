"""
Maze Runner 2D with AI Solver
Move around a maze and try to escape using AI.
"""

import sys
import os
from collections import deque
import time

# Maze file characters:
WALL = "#"
EMPTY = " "
START = "S"
EXIT = "E"

# Display characters:
PLAYER = "@"
BLOCK = chr(9617)  # '░'

# Global variables for player and exit positions, and maze size
playerx = None
playery = None
exitx = None
exity = None
WIDTH = 0
HEIGHT = 0

def displayMaze(maze):
    """Display the maze with the player and exit."""
    global playerx, playery, exitx, exity, WIDTH, HEIGHT
    os.system('cls' if os.name == 'nt' else 'clear')
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) == (playerx, playery):
                print(PLAYER, end='')
            elif (x, y) == (exitx, exity):
                print("X", end='')
            elif maze.get((x, y)) == WALL:
                print(BLOCK, end='')
            else:
                print(maze.get((x, y), ' '), end='')
        print()

def solve_maze(maze, start, goal):
    """Solve the maze using BFS and return the path."""
    queue = deque()
    queue.append((start, []))  # (position, path)
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) == goal:
            return path

        for (dx, dy), move in [((0, -1), "W"), ((0, 1), "S"), ((-1, 0), "A"), ((1, 0), "D")]:
            nx, ny = x + dx, y + dy
            if maze.get((nx, ny), WALL) == EMPTY:
                queue.append(((nx, ny), path + [move]))

    return None

# === Get maze filename from user ===
while True:
    print("Enter the filename of the maze (or LIST or QUIT): ")
    filename = input("> ")
    if filename.upper() == 'LIST':
        print("Maze files found in", os.getcwd())
        for fileInCurrentFolder in os.listdir():
            if fileInCurrentFolder.startswith("maze") and fileInCurrentFolder.endswith(".txt"):
                print("  ", fileInCurrentFolder)
        continue
    if filename.upper() == "QUIT":
        sys.exit()
    if os.path.exists(filename):
        break
    print("There is no file named", filename)

# === Load the maze from the file ===
mazeFile = open(filename)
maze = {}
lines = mazeFile.readlines()
playerx = None
playery = None
exitx = None
exity = None
y = 0

for line in lines:
    line = line.rstrip("\n")
    WIDTH = max(WIDTH, len(line))
    for x, character in enumerate(line):
        assert character in (WALL, EMPTY, START, EXIT), \
            f"Invalid character at column {x + 1}, line {y + 1}"
        if character == START:
            playerx, playery = x, y
            maze[(x, y)] = EMPTY
        elif character == EXIT:
            exitx, exity = x, y
            maze[(x, y)] = EMPTY
        else:
            maze[(x, y)] = character
    y += 1
HEIGHT = y

assert playerx is not None and playery is not None, "No start in maze file."
assert exitx is not None and exity is not None, "No exit in maze file."

# === Solve the maze using AI ===
solution = solve_maze(maze, (playerx, playery), (exitx, exity))
if solution is None:
    print("No path found by AI!")
    sys.exit()
else:
    print("AI found a path:", ''.join(solution))
    for move in solution:
        displayMaze(maze)
        time.sleep(1)
        if move == "W":
            playery -= 1
        elif move == "S":
            playery += 1
        elif move == "A":
            playerx -= 1
        elif move == "D":
            playerx += 1
    displayMaze(maze)
    print("AI reached the exit successfully!")
    sys.exit()
