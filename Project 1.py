import numpy as np 
import os

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

shelves2 = {
	(0,2): 'A',
	(1,2): 'B',
	(3,0): 'C',
	(1,0): 'D',
	(2,0): 'E',
	(2,2): 'F',
	(4,0): 'G',
	(3,2): 'H',
	(5,0): 'I',
	(4,2): 'J',
	(2,4): 'K',
	(1,4): 'M',
	(5,4): 'N',
	(3,5): 'O',
	(0,4): 'P',
	(4,5): 'Q'
}

class Environment:

	def __init__(self, size, shelves): # environment constructor		
		self.a = Agent() # agent object
		self.agentx = 0 # tracks agent's x pos
		self.agenty = 0 # tracks agent's y pos
		self.shelves = shelves
		self.size = size
		self.world = self.make_world()
		self.steps = 0 # num steps agent has taken
		self.score = 0 # keeps agent's score

	def make_world(self):
		#create world and fill with shelf info
		world = np.empty(shape=self.size, dtype=str) #declares an empty numpy array of shape 'size' (global) and type string
		world.fill('_') # fills the numpy array with underscore char
		for locy, locx in self.shelves:  # sets 
			world[locy][locx] = self.shelves[(locy, locx)]		

		return world

	def print_world(self):
		#visualize the world for debugging
		holder = self.world[self.agenty,self.agentx]
		self.world[self.agenty,self.agentx] = 'R'
		os.system('cls')
		print(self.world, "\n"*2, self.a.order)
		self.world[self.agenty,self.agentx] = holder

	def get_order(self):
		#generate random list of shelves for an order
		shelves = list(self.shelves.values()) # list of 10 shelves (given by problem)
		shelf_amt = len(shelves)

		order = [] # empty order list to be populated
		order_length = np.random.randint(1,shelf_amt+1) # random order length between 1 and 10 (shifted for 0-based)
		for x in range(0,order_length):
			order.append(shelves.pop(np.random.randint(shelf_amt-x))) # appends a random shelf to 'orders' and removes it from 'shelves'

		return order

	def get_neighbors(self):
		#agent perception of the world including the inaccurate sensors

		#first find the true neighbors, None when the agent is against an edge of the world
		north = self.world[self.agenty-1][self.agentx] if self.agenty > 0 else None
		south = self.world[self.agenty+1][self.agentx] if self.agenty < 5 else None
		east = self.world[self.agenty][self.agentx+1] if self.agentx < 5 else None
		west = self.world[self.agenty][self.agentx-1] if self.agentx > 0 else None
		neighbors = [north, south, east, west]		

		#sensor inaccuracy
		shelves = list(self.shelves.values())
		for index, neighbor in enumerate(neighbors):
			#10% of the time the sensor fails, and the robot thinks that a shelf is present when it is not the case
			if neighbor == '_':
				if np.random.randint(10) == 9:
					rand_shelf = shelves[np.random.randint(10)]
					neighbors[index] = rand_shelf
			#10% of the time a shelf exists but the sensor fails to detect it
			elif neighbor in shelves:
				if np.random.randint(10) == 9:
					neighbors[index] = '_'

		# print("\nNorth:", neighbors[0], "\nSouth:", neighbors[1], "\nEast:", neighbors[2], "\nWest:", neighbors[3])

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
		#path record-keeping variables
		shortest_path = []
		shortest_length = 9999
		shortest_score = 0
		shortest_order = []
		longest_path = []
		longest_length = 0 
		longest_order = []
		longest_score = 0

		score_list = np.zeros(order_amount)

		#loop for the amount of orders in an episode
		for order_index in range(order_amount):
			path = [(self.agenty, self.agentx)]
			self.steps = 0

			#update agent order state
			self.a.order = self.get_order()	
			path_order = self.a.order.copy()		
			self.score = 4*len(self.a.order)

			#initial check on starting tile
			current_tile = self.world[self.agenty][self.agentx]
			if current_tile in self.a.order:
				self.a.order.remove(current_tile)

			#for each order: get neighbors and update agent neighbor state, request action from agent, move agent, then check current tile for part of order
			while self.a.order:
				# self.print_world()
				self.a.neighbors = self.get_neighbors()
				action = self.a.get_action()
				self.agent_move(action)
				path.append((self.agenty, self.agentx))
				
				current_tile = self.world[self.agenty][self.agentx]
				if current_tile in self.a.order:
					self.a.order.remove(current_tile)

			#adjust if no steps are taken
			if self.steps == 0:
				self.steps =1
			self.score -= self.steps

			#update the longest and shortest path if the current order is the new longest/shortest
			if len(path) > longest_length:
				longest_path = path.copy()
				longest_length = len(path)
				longest_order = path_order
				longest_score = self.score

			if len(path) < shortest_length:
				shortest_path = path.copy()
				shortest_length = len(path)
				shortest_order = path_order
				shortest_score = self.score

			score_list[order_index] = self.score

		return shortest_path, shortest_order, shortest_score, longest_path, longest_order, longest_score, np.average(score_list)

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
		while action == -1:
			action = np.random.randint(4)
			#if the action would result in running into the wall, try again
			if self.neighbors[action] == None:
				action = -1

		return action

#create environment and run for 1000 orders on either shelves1 or shelves2
e = Environment(world_size, shelves2)
shortest_path, shortest_order, shortest_score, longest_path, longest_order, longest_score, avg_score = e.run_order(1000)

#print results
print("SHORTEST PATH:", shortest_path, "\nORDER:", shortest_order, "\nSCORE:", shortest_score)
print("LONGEST PATH:", longest_path, "\nORDER:", longest_order, "\nSCORE:", longest_score)
print("\nAVERAGE SCORE:", avg_score)