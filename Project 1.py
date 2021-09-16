import numpy as np 
from msvcrt import getch
import os
from time import sleep

#environment info
world_size = (6,6)

shelves1 = {
	(1,1): 'A',
	(2,2): 'B',
	(3,1): 'C',
	(0,2): 'D',
	(2,0): 'E',
	(4,2): 'F',
	(1,4): 'G',
	(4,5): 'H',
	(2,4): 'I',
	(5,3): 'J'
}

class Environment:

	def __init__(self, size, shelves): # environment constructor		
		self.a = Agent() # agent object
		self.agentx = 0 # tracks agent's x pos
		self.agenty = 0 # tracks agent's y pos
		self.shelves = shelves
		self.size = size
		self.world = np.empty(shape=size, dtype=str)
		self.steps = 0 # num steps agent has taken
		self.score = 0 # keeps agent's score

	def draw_world(self):
		#create world and fill with shelf info
		#world = np.empty(shape=size, dtype=str) #declares an empty numpy array of shape 'size' (global) and type string
		newWorld = self.world
		newWorld.fill('_') # fills the numpy array with underscore char
		for locy, locx in self.shelves:  # sets 
			newWorld[locy][locx] = self.shelves[(locy, locx)]
		newWorld[self.agenty,self.agentx] = 'R'
		os.system('cls')
		print(newWorld, "\n"*2, self.a.order)

		return newWorld

	def get_order(self):
		#generate random list of shelves for an order
		shelves = ['A','B','C','D','E','F','G','H','I','J'] # list of 10 shelves (given by problem)
		order = [] # empty order list to be populated
		order_length = np.random.randint(1,11) # random order length between 1 and 10 (shifted for 0-based)
		for x in range(0,order_length):
			order.append(shelves.pop(np.random.randint(10-x))) # appends a random shelf to 'orders' and removes it from 'shelves'

		return order

	def get_neighbors(self):
		#agent perception of the world including the inaccurate sensors

		#first find the true neighbors, None when the agent is against an edge of the world
		north = self.world[self.agenty-1][self.agentx] if self.agenty > 0 else None
		south = self.world[self.agenty+1][self.agentx] if self.agenty < 5 else None
		east = self.world[self.agenty][self.agentx+1] if self.agentx < 5 else None
		west = self.world[self.agenty][self.agentx-1] if self.agentx > 0 else None
		neighbors = [north, south, east, west]

		print("\nNorth:", north, "\nSouth:", south, "\nEast:", east, "\nWest:", west)
		return neighbors

	def agent_move(self, action):
		#up
		if(action == 0):
			self.agenty = np.maximum(self.agenty-1,0)
		#down
		elif(action == 1):
			self.agenty = np.minimum(self.agenty+1,5)
		#right
		elif(action == 2):
			self.agentx = np.minimum(self.agentx+1,5)
		#left
		elif(action == 3):
			self.agentx = np.maximum(self.agentx-1,0)			

		self.steps += 1	

	def run_order(self, order_amount):

		for order_index in range(order_amount):
			self.a.order = self.get_order()
			self.score = 3*len(self.a.order)	

			while self.a.order:
				self.draw_world()
				self.a.neighbors = self.get_neighbors()
				action = self.a.get_action()
				self.agent_move(action)
				current_tile = self.world[self.agenty][self.agentx]
				
				if current_tile in self.a.order:
					self.a.order.remove(current_tile)

				sleep(0.1)

			self.draw_world()
			self.score -= self.steps
			print("ORDER", order_index+1,"/", order_amount, "COMPLETED IN", self.steps, "STEPS")
			print("SCORE =", self.score)

#agent states are neighbors and orders
#simple reflex agent looks at current state and returns action
class Agent:

	def __init__(self):
		self.neighbors = []
		self.order = []

	def get_action(self):
		#if a neighbor is part of the order move to it, else move random
		action = -1
		#loop through neighbors and compares to order, if found then set action to move to that neighbor
		#action values: up=0, down=1, right=2, left=3
		#stops after finding the first neighbor in the order
		for index, neighbor in enumerate(self.neighbors):
			if neighbor in self.order:
				action = index
				break
		
		#if the neighbors have nothing in the order, then move in a random direction
		if action == -1:
			action = np.random.randint(4)

		return action


e = Environment(world_size, shelves1)
e.run_order(1)
