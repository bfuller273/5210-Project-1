import numpy as np 
from msvcrt import getch
import os
import random

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

	def __init__(self, size, shelves): # environment constructor		
		self.a = Agent() # agent object
		self.agentx = 0 # tracks agent's x pos
		self.agenty = 0 # tracks agent's y pos
		#self.world = self.draw_world(size, shelves)
		self.world = np.empty(shape=size, dtype=str)
		self.steps = 0 # num steps agent has taken
		self.score = 0 # keeps agent's score

	def draw_world(self, size, shelves):
		#create world and fill with shelf info
		#world = np.empty(shape=size, dtype=str) #declares an empty numpy array of shape 'size' (global) and type string
		NewWorld = self.world
		NewWorld.fill('_') # fills the numpy array with underscore char
		for (locy,locx), label in shelves:  # sets 
			NewWorld[locy,locx] = label
		NewWorld[self.agenty,self.agentx] = 'R'
		os.system('cls')
		print(NewWorld, "\n"*2, self.a.order)

		return NewWorld

	def get_order(self):
		#generate random list of shelves for an order
		shelves = ['A','B','C','D','E','F','G','H','I','J'] # list of 10 shelves (given by problem)
		order = [] # empty order list to be populated
		order_length = np.random.randint(1,11) # random order length between 1 and 10 (shifted for 0-based)
		for x in range(0,order_length):
			order.append(shelves.pop(np.random.randint(10-x))) # appends a random shelf to 'orders' and removes it from 'shelves'

		return order

	def get_neighbors(self):
		#agent perception of the world 
		#including the inaccurate sensors
		north = np.where(self.world[self.agenty-1, self.agentx])
		south = self.world[self.agenty+1, self.agentx]
		east = self.world[self.agenty, self.agentx+1]
		west = self.world[self.agenty, self.agentx-1]
		neighbors = [north, south, east, west]
		print("\nNorth:", north, "\nSouth:", south, "\nEast:", east, "\nWest:", west)
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
		for j in self.neighbors: # iterate thru neighbors columns
			for i in self.neighbors: # iterate thru neighbors rows
				if self.neighbors[i][j] == self.order[i][j]: # if any of the agent's current neighbors match a shelf in an order...
					self.agentx == i # move the agent to the shelf's x position (row)
					self.agenty == j # move the agent to the shelf's y position (column)
				else: # otherwise (no match found)...
					random(np.size(self.neighbors[i][j])) # generate a random number based on neighbors (which is all valid positions that can be moved to)
					
		action = 0

		c = ord(getch())
		if c == 224:
			action = ord(getch())
		elif c == 113:
			action = 113

		return action


e = Environment(world_size, shelves1)
e.run_order(1)
e.get_neighbors()