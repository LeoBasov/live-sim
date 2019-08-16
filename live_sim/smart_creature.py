"""live_sim a evolution simulation
Copyright (C) 2019  Leo Basov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
long with this program. If not, see <https://www.gnu.org/licenses/>."""

import sys
import random
from enum import Enum
import copy
import math
import numpy as np

sys.path.append('../../neat-python/.')

from neat.network import Node
from neat.genome import Gene
from neat.genome import Genome
from neat.network import Network
from neat.neat import NEAT
from neat.neat import Mutator

from .creature import Creature

class Brain(Network):
	"""This is the brain of of the new creature typ

	The creature is provided with a set of sensory input as well as outputs generated by the network.
	The set of input and output values is fixed while the rest of the network can evolve freely.
	However technically the network has the capabolity to eveolve enven with a varying set of inputs if executed properly

	"""
	def __init__(self):
		"""
		"""
		super().__init__()
		self.created_output_node_ids = []
		self.created_input_node_ids = []

		#Inputs
		self.INPUT_OTHER_CREATURE_ANGLE = 0
		self.INPUT_OTHER_CREATURE_DISTANCE = 0
		self.INPUT_OTHER_CREATURE_SIZE = 0
		self.INPUT_OTHER_CREATURE_ENERGY = 0
		self.INPUT_OTHER_CREATURE_FOUND_STATUS = 0

		self.INPUT_FOOD_ANGLE = 0
		self.INPUT_FOOD_DISTANCE = 0
		self.INPUT_FOOD_FOUND_STATUS = 0

		self.INPUT_SELF_ENERNGY = 9
		self.INPUT_SELF_SIZE = 10
		self.INPUT_SELF_SPEED = 11

		#Movement related output
		self.OUTPUT_MOVE_STATUS = 12 #Move status output
		self.OUTPUT_MOVE_ANGLE = 13 #Move angle output
		self.OUTPUT_MOVE_SPEED = 14 #Move speed output

		#Eating related output
		self.OUTPUT_EAT_STATUS = 15 #Eat status output

		#Reproduction related output
		self.OUTPUT_REPRODUCE_STATUS = 16 #Reproduce status output

		genome = Genome()

		#------------------------------------------------------------------
		#INPUT NODES
		#------------------------------------------------------------------
		#Other creature related input
		self.INPUT_OTHER_CREATURE_ANGLE = genome.add_input_node() #Angle to next creature
		self.INPUT_OTHER_CREATURE_DISTANCE = genome.add_input_node() #Distance to next creature
		self.INPUT_OTHER_CREATURE_SIZE = genome.add_input_node() #Size of next creature
		self.INPUT_OTHER_CREATURE_ENERGY = genome.add_input_node() #Enerngy of next creature
		self.INPUT_OTHER_CREATURE_FOUND_STATUS = genome.add_input_node() #Next creature found status

		self.created_input_node_ids.append(self.INPUT_OTHER_CREATURE_ANGLE)
		self.created_input_node_ids.append(self.INPUT_OTHER_CREATURE_DISTANCE)
		self.created_input_node_ids.append(self.INPUT_OTHER_CREATURE_SIZE)
		self.created_input_node_ids.append(self.INPUT_OTHER_CREATURE_ENERGY)
		self.created_input_node_ids.append(self.INPUT_OTHER_CREATURE_FOUND_STATUS)

		#Food related input
		self.INPUT_FOOD_ANGLE = genome.add_input_node() #Angle to next creature
		self.INPUT_FOOD_DISTANCE = genome.add_input_node() #Distance to next creature
		self.INPUT_FOOD_FOUND_STATUS = genome.add_input_node() #Food found status

		self.created_input_node_ids.append(self.INPUT_FOOD_ANGLE)
		self.created_input_node_ids.append(self.INPUT_FOOD_DISTANCE)
		self.created_input_node_ids.append(self.INPUT_FOOD_FOUND_STATUS)

		#Self related input
		self.INPUT_SELF_ENERNGY = genome.add_input_node() #Energy
		self.INPUT_SELF_SIZE = genome.add_input_node() #Size
		self.INPUT_SELF_SPEED = genome.add_input_node() #Speed

		self.created_input_node_ids.append(self.INPUT_SELF_ENERNGY)
		self.created_input_node_ids.append(self.INPUT_SELF_SIZE)
		self.created_input_node_ids.append(self.INPUT_SELF_SPEED)

		#------------------------------------------------------------------
		#OUTPUT NODES
		#------------------------------------------------------------------
		#Movement related input
		self.OUTPUT_MOVE_STATUS = genome.add_output_node() #Move status output
		self.OUTPUT_MOVE_ANGLE = genome.add_output_node() #Move angle output
		self.OUTPUT_MOVE_SPEED = genome.add_output_node() #Move speed output

		self.created_output_node_ids.append(self.OUTPUT_MOVE_STATUS)
		self.created_output_node_ids.append(self.OUTPUT_MOVE_ANGLE)
		self.created_output_node_ids.append(self.OUTPUT_MOVE_SPEED)

		#Eating related input
		self.OUTPUT_EAT_STATUS = genome.add_output_node() #Eat status output

		self.created_output_node_ids.append(self.OUTPUT_EAT_STATUS)

		#Reproduction related input
		self.OUTPUT_REPRODUCE_STATUS = genome.add_output_node() #Reproduce status output

		self.created_output_node_ids.append(self.OUTPUT_REPRODUCE_STATUS)

		self.__set_up_genes(genome)

	def __set_up_genes(self, genome):
		bias_node_id = 0
		number_hidden_nodes = 5
		number_genes = 50
		genes = []

		for out_node_id in self.created_output_node_ids:
			for in_node_id in self.created_input_node_ids:
				gene = Gene(in_node_id = in_node_id, out_node_id = out_node_id, weight = self.__get_random_weight(), enabled = True)
				genes.append(gene)

			gene = Gene(in_node_id = bias_node_id, out_node_id = out_node_id, weight = self.__get_random_weight(), enabled = True)
			genes.append(gene)

		genome.allocate_hidden_nodes(number_hidden_nodes)
		genome.set_genes(genes)
		genome.allocate_genes(number_genes)

		self.set_up(genome)

	def __get_random_weight(self):
		return  10 - 20.0*random.random()

class SmartCreature(Creature):
	def __init__(self, world):
		super().__init__(world)

		self.mutator = Mutator()
		self.brain = Brain()

	def copy(self, other):
		super().copy(other)

		self.mutator = copy.deepcopy(other.mutator)
		self.brain = copy.deepcopy(other.brain)

	def _move(self):
		#super()._move()

		dist_food = self._find_food()
		dist_enemy = self._find_enemy()
		input_values = self.__set_up_brain_input_values(dist_food, dist_enemy)

		ret_vals = self.brain.execute(input_values)
		self.__process_output(ret_vals)

		if dist_food[1] != None and dist_food[0] < 0.5*self.size:
			self.energy += dist_food[1].be_consumed()

		if dist_enemy[1] != None and self.size > 1.2*dist_enemy[1].size and dist_enemy[0] < 0.5*self.size:
			self.energy += dist_enemy[1].be_consumed()

	def __process_output(self, ret_vals):
		if ret_vals[self.brain.OUTPUT_MOVE_STATUS] > 0.5:
			self.__get_new_position(ret_vals[self.brain.OUTPUT_MOVE_ANGLE], ret_vals[self.brain.OUTPUT_MOVE_SPEED])

	def __get_new_position(self, angle, speed):
		dist_vec = np.array([math.sin(angle), math.cos(angle), 0.0])
		dist_vec *= speed*self.speed

		position_new = self.position + dist_vec

		if self.world.collision(position_new):
			self.position =  self._random_move()
		else:
			self.position = position_new

	def __set_up_brain_input_values(self, dist_food, dist_enemy):
		input_values = []

		self.__set_brain_with_other_creature_input_values(input_values, dist_enemy)
		self.__set_brain_with_food_input_values(input_values, dist_food)

		return input_values

	def __set_brain_with_other_creature_input_values(self, input_values, dist_enemy):
		if dist_enemy[1]:
			input_values.append((self.__get_angle(dist_enemy), self.brain.INPUT_OTHER_CREATURE_ANGLE))
			input_values.append((dist_enemy[0], self.brain.INPUT_OTHER_CREATURE_DISTANCE))
			input_values.append((dist_enemy[1].size, self.brain.INPUT_OTHER_CREATURE_SIZE))
			input_values.append((dist_enemy[1].energy, self.brain.INPUT_OTHER_CREATURE_ENERGY))
			input_values.append((1, self.brain.INPUT_OTHER_CREATURE_FOUND_STATUS))
		else:
			input_values.append((0, self.brain.INPUT_OTHER_CREATURE_ANGLE))
			input_values.append((0, self.brain.INPUT_OTHER_CREATURE_DISTANCE))
			input_values.append((0, self.brain.INPUT_OTHER_CREATURE_SIZE))
			input_values.append((0, self.brain.INPUT_OTHER_CREATURE_ENERGY))
			input_values.append((0, self.brain.INPUT_OTHER_CREATURE_FOUND_STATUS))

	def __set_brain_with_food_input_values(self, input_values, dist_food):
		if dist_food[1]:
			input_values.append((self.__get_angle(dist_food), self.brain.INPUT_FOOD_ANGLE))
			input_values.append((dist_food[0], self.brain.INPUT_FOOD_DISTANCE))
			input_values.append((1, self.brain.INPUT_FOOD_FOUND_STATUS))
		else:
			input_values.append((0, self.brain.INPUT_FOOD_ANGLE))
			input_values.append((0, self.brain.INPUT_FOOD_DISTANCE))
			input_values.append((0, self.brain.INPUT_FOOD_FOUND_STATUS))

	def __get_angle(self, dist_other):
		vec = np.array([0, 0, 0])

		if dist_other[0] > 0:
			vec = (dist_other[1].position - self.position)/dist_other[0]

		return math.sin(vec[0])
