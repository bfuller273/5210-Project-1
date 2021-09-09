import numpy as np 
from msvcrt import getch
import os

#environment info
world_size = (6,6)
shelves1 = [[(1,1),'A'],
			[(2,2),'B'],
			[(3,1),'C'],
			[(0,2),'D'],
			[(2,0),'E'],
			[(4,2),'F'],
			[(1,4),'G'],
			[(4,5),'H'],
			[(2,4),'I'],
			[(5,3),'J']]


def draw_world(world_size, shelves):
	#create world and fill with shelf info
	world = np.empty(shape=world_size, dtype=str)
	world.fill('_')
	for (locy,locx), label in shelves1:
		world[locy,locx] = label

	return world

def get_order():
	shelves = ['A','B','C','D','E','F','G','H','I','J']
	order = []
	order_length = np.random.randint(1,10)
	for x in range(0,order_length):
		order.append(shelves.pop(np.random.randint(10-x)))
	return order

def get_neighbors(robot_pos, world):
	#robot perception of the world 
	#including the inaccurate sensors
	return 0

def get_action(neighbors, order):
	#if a neighbor is part of the order,  move to it
	#else move random
	return 0 

#robot
#states are neighbors and orders
visited = np.zeros(world_size)
robot_pos = [0,0]
visited[robot_pos[0],robot_pos[1]] = 1

def robot_move(action):
	#up
	if(action == 72):
		robot_pos[0] = np.maximum(robot_pos[0]-1,0)
	#down
	elif(action == 80):
		robot_pos[0] = np.minimum(robot_pos[0]+1,5)
	#left
	elif(action == 75):
		robot_pos[1] = np.maximum(robot_pos[1]-1,0)
	#right
	elif(action == 77):
		robot_pos[1] = np.minimum(robot_pos[1]+1,5)

	visited[robot_pos[0],robot_pos[1]] = 1

order = get_order()

c = 0
steps = 0
world = draw_world(world_size,shelves1)

while(c != 113):
	if(c == 224):
		c = ord(getch())
		robot_move(c)
		steps += 1

	state = world[robot_pos[0],robot_pos[1]]
	if state in order:
		order.remove(state)		

	os.system('cls')
	world = draw_world(world_size, shelves1)
	world[robot_pos[0],robot_pos[1]] = 'R'
	print(world, "\n"*2, visited, "\n"*2, order)

	if not order:
		print("ORDER DONE IN ", steps,"STEPS")
		break

	c = ord(getch())







