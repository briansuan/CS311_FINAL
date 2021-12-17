# Brian Suan
# Depth First Search algorithm visualizer for CS 311 final project
# Depth First Search Sources:
# https://courses.cs.washington.edu/courses/cse326/03su/homework/hw3/dfs.html
# https://medium.com/swlh/solving-mazes-with-depth-first-search-e315771317ae
# Visualizer tutorial Source:
# https://www.youtube.com/watch?v=msttfIHHkak



import pygame
from collections import deque




WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("DFS VISUALIZER")

# Set colors to RGB color codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)

# A Node represents each box on the grid
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self. col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = BLUE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Place a node into the neighbors list, make sure it's not a barrier or out of bounds
    def update_neighbors(self, grid):
        self.neighbors = []
        # Append to the neighbors array only if the neighbor is within the grid and not out of bounds or is a barrier
        # DOWN NEIGHBOR
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP NEIGHBOR
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT NEIGHBOR
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT NEIGHBOR
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False




# Draws the path in purple when the path is found
def finalize_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()




########## DEPTH FIRST SEARCH ALGORITHM ############
def DFS(draw, grid, start, end):
    # Use deque as a stack instead of a list because it is faster
    open_stack = deque()
    # Put start in the open stack
    open_stack.append(start)
    # Nodes we visited
    came_from = {}
    # Keep track of neighbors using dictionary
    neighbor_set = {start}


    while open_stack:
        # Allows user to exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # When this function is first executed, the current node is the start node
        current = open_stack.pop()
        # Remove the current node from the neighbors set
        neighbor_set.remove(current)

        # If the current node is the end node, complete the path from the start node to the end node
        if current == end:
            end.make_end()
            finalize_path(came_from, end, draw)
            return True

        # For every neighbors in the neighbors set, if a node is not in the neighbor set, add it to the neighbor set
        # and if it is not in the came_from dictionary, add the neighbor to the open_stack stack, set that neighbor
        # as the current node and make that node open
        for neighbor in current.neighbors:
            if neighbor not in neighbor_set:
                neighbor_set.add(neighbor)
                if neighbor not in came_from:
                    open_stack.append(neighbor)
                    came_from[neighbor] = current
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False




# Makes the grid to be placed on the board
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

# Draws the grid on the board
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Draws the board
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

# Function to determine which node (box) is clicked
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# Main function
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    # Initialize start to None
    start = None
    # Initialize end to None
    end = None


    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # If left mouse click
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                # set row and col to the node that was clicked
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                # Can't put end node over start node and vice versa
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            # If right mouse click, reset clicked node
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # Start DFs algorithm is "d" is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # Lambda passes a draw() function as an argument for the DFS() function
                    DFS(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # If "c" is pressed, clear and reset the board
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)










