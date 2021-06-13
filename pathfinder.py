'''
PATH FINDING VISUALIZATION
Press A for choosing A star algorithm
Press D for choosing dijkastra algrothm

First two left mouse clicks chosses start and end point

Space for running the algorithm
C for clearing 

'''

import pygame as py
import math
from queue import PriorityQueue

WIDTH = 800
DISPLAY = py.display.set_mode((WIDTH, WIDTH))
py.display.set_caption("Path Finding Algorithm Visualization")

TRAVERSE_COL = (255, 204, 255)
BOUNDARY_COL = (255, 128, 0)
BLUE = (0, 255, 0)
YELLOW = (242, 221, 84 )
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PATH_COL = (102, 0, 102)
START_COL = (0, 0 ,255)
GREY = (128, 128, 128)
END_COL = (255, 255, 0)

class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == TRAVERSE_COL

	def is_open(self):
		return self.color == BOUNDARY_COL

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == START_COL

	def is_end(self):
		return self.color == END_COL

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = START_COL

	def make_closed(self):
		self.color = TRAVERSE_COL

	def make_open(self):
		self.color = BOUNDARY_COL

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = END_COL

	def make_path(self):
		self.color = PATH_COL

	def draw(self, DISPLAY):
		py.draw.rect(DISPLAY, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []

		# up neighbor
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		#down neighbor
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		#right neighbor
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		#left neighbor
		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

		#this algo is not for diagonal path finding but you can add them also


	#Defines the behaviour of the less-than operator <	
	def __lt__(self, other):
		return False

#for A star algo
def heuristic_dist(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# building the path again for a star and dijkastra
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

#Astar algo
def algorithm1(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0
	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = heuristic_dist(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in py.event.get():
			if event.type == py.QUIT:
				py.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + heuristic_dist(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

#dijkastra algo
def algorithm2(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0

	open_set_hash = {start}

	while not open_set.empty():
		for event in py.event.get():
			if event.type == py.QUIT:
				py.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((g_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid


def draw_grid(DISPLAY, rows, width):
	gap = width // rows
	for i in range(rows):
		py.draw.line(DISPLAY, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			py.draw.line(DISPLAY, GREY, (j * gap, 0), (j * gap, width))


def draw(DISPLAY, grid, rows, width):
	DISPLAY.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(DISPLAY)

	draw_grid(DISPLAY, rows, width)
	py.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(DISPLAY, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None
	choice=0
	run = True
	while run:
		draw(DISPLAY, grid, ROWS, width)
		for event in py.event.get():
			if event.type == py.QUIT:
				run = False

			if py.mouse.get_pressed()[0]: # LEFT
				pos = py.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				if not start and node != end:
					start = node
					start.make_start()

				elif not end and node != start:
					end = node
					end.make_end()

				elif node != end and node != start:
					node.make_barrier()

			elif py.mouse.get_pressed()[2]: # RIGHT
				pos = py.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == py.KEYDOWN:
    				if event.key == py.K_a:
    						choice=0
							
    			
			if event.type == py.KEYDOWN:
    				if event.key == py.K_d:
    						choice=1    
    						
			if event.type == py.KEYDOWN:
				if event.key == py.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					if(choice==0):	
						algorithm1(lambda: draw(DISPLAY, grid, ROWS, width), grid, start, end)
					else:
						algorithm2(lambda: draw(DISPLAY, grid, ROWS, width), grid, start, end)
    						
				if event.key == py.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	py.quit()

main(DISPLAY, WIDTH)