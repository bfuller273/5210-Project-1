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

class Environment:

	def __init__(self, size, shelves):		
		self.a = Agent()
		self.agentx = 0
		self.agenty = 0
		self.world = self.draw_world(size, shelves)
		self.steps = 0
		self.score = 0

	def draw_world(self, size, shelves):
		#create world and fill with shelf info
		world = np.empty(shape=size, dtype=str)
		world.fill('_')
		for (locy,locx), label in shelves:
			world[locy,locx] = label
		world[self.agenty,self.agentx] = 'R'
		os.system('cls')
		print(world, "\n"*2, self.a.order)

		return world

	def get_order(self):
		#generate random list of shelves for an order
		shelves = ['A','B','C','D','E','F','G','H','I','J']
		order = []
		order_length = np.random.randint(1,11)
		for x in range(0,order_length):
			order.append(shelves.pop(np.random.randint(10-x)))

		return order

	def get_neighbors(self):
		#agent perception of the world 
		#including the inaccurate sensors
		neighbors = []
		return neighbors

	def agent_move(self, action):
		#up
		if(action == 72):
			self.agenty = np.maximum(self.agenty-1,0)
		#down
		elif(action == 80):
			self.agenty = np.minimum(self.agenty+1,5)
		#left
		elif(action == 75):
			self.agentx = np.maximum(self.agentx-1,0)
		#right
		elif(action == 77):
			self.agentx = np.minimum(self.agentx+1,5)	

		self.steps += 1	

	def run_order(self, number):
		self.a.order = self.get_order()
		world = self.draw_world(world_size, shelves1)
		self.score = 3*len(self.a.order)

		while self.a.order:
			action = self.a.get_action()

			if action == 113:
				break

			self.agent_move(action)
			tile = world[self.agenty, self.agentx]
			world = self.draw_world(world_size, shelves1)
			
			if tile in self.a.order:
				self.a.order.remove(tile)
				self.draw_world(world_size, shelves1)

		self.score -= self.steps
		print("ORDER", number, "COMPLETED IN", self.steps, "STEPS")
		print("SCORE =", self.score)

#agent states are neighbors and orders
#simple reflex agent looks at current state and returns action
class Agent:

	def __init__(self):
		self.neighbors = []
		self.order = []

	def get_action(self):
		#if a neighbor is part of the order,  move to it
		#else move random
		action = 0

		c = ord(getch())
		if c == 224:
			action = ord(getch())
		elif c == 113:
			action = 113

		return action


e = Environment(world_size, shelves1)
e.run_order(1)