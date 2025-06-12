"""
Maze Runner 2D, by Al Sweigart (fixed version)
Move around a maze and try to escape.
"""

import sys
import os

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
        print()  # Move to next line after each row

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

# === Main game loop ===
while True:
    displayMaze(maze)

    while True:
        print("                            W")
        print("Enter direction, or QUIT: A S D")
        move = input("> ").upper()

        if move == "QUIT":
            print("Thanks for playing!")
            sys.exit()

        if move not in ["W", "A", "S", "D"]:
            print("Invalid direction. Enter one of W, A, S, or D.")
            continue

        # Check if player can move in that direction:
        if move == "W" and maze.get((playerx, playery - 1), WALL) == EMPTY:
            break
        elif move == "S" and maze.get((playerx, playery + 1), WALL) == EMPTY:
            break
        elif move == "A" and maze.get((playerx - 1, playery), WALL) == EMPTY:
            break
        elif move == "D" and maze.get((playerx + 1, playery), WALL) == EMPTY:
            break

        print("You cannot move in that direction.")

    # Move continuously in the chosen direction until a branch point or exit is reached
    if move == "W":
        while True:
            playery -= 1
            if (playerx, playery) == (exitx, exity):
                break
            if maze.get((playerx, playery - 1), WALL) == WALL:
                break
            if maze.get((playerx - 1, playery), WALL) == EMPTY or maze.get((playerx + 1, playery), WALL) == EMPTY:
                break

    elif move == "S":
        while True:
            playery += 1
            if (playerx, playery) == (exitx, exity):
                break
            if maze.get((playerx, playery + 1), WALL) == WALL:
                break
            if maze.get((playerx - 1, playery), WALL) == EMPTY or maze.get((playerx + 1, playery), WALL) == EMPTY:
                break

    elif move == "A":
        while True:
            playerx -= 1
            if (playerx, playery) == (exitx, exity):
                break
            if maze.get((playerx - 1, playery), WALL) == WALL:
                break
            if maze.get((playerx, playery - 1), WALL) == EMPTY or maze.get((playerx, playery + 1), WALL) == EMPTY:
                break

    elif move == "D":
        while True:
            playerx += 1
            if (playerx, playery) == (exitx, exity):
                break
            if maze.get((playerx + 1, playery), WALL) == WALL:
                break
            if maze.get((playerx, playery - 1), WALL) == EMPTY or maze.get((playerx, playery + 1), WALL) == EMPTY:
                break

    # Check if player reached the exit
    if (playerx, playery) == (exitx, exity):
        displayMaze(maze)
        print("You have reached the exit! Good job!")
        print("Thanks for playing!")
        sys.exit()
