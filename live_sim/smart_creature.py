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
from neat.network import Gene
from neat.network import Network
from neat.neat import NEAT

from .creature import Creature

class InputNodeType(Enum):
	#Other creature related input
	OTHER_CREATURE_ANGLE = 1
	OTHER_CREATURE_DISTANCE = 2
	OTHER_CREATURE_SIZE = 3
	OTHER_CREATURE_ENERGY = 4
	OTHER_CREATURE_FOUND_STATUS = 5

	#Food related input
	FOOD_ANGLE = 6
	FOOD_DISTANCE = 7
	FOOD_FOUND_STATUS = 8

	#Self related input
	SELF_ENERNGY = 9
	SELF_SIZE = 10
	SELF_SPEED = 11

class OutputNodeType(Enum):
	#Movement related input
	MOVE_STATUS = 12 #Move status output
	MOVE_ANGLE = 13 #Move angle output
	MOVE_SPEED = 14 #Move speed output

	#Eating related input
	EAT_STATUS = 15 #Eat status output

	#Reproduction related input
	REPRODUCE_STATUS = 16 #Reproduce status output

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

		#------------------------------------------------------------------
		#INPUT NODES
		#------------------------------------------------------------------
		#Other creature related input
		self._add_input_node(InputNodeType.OTHER_CREATURE_ANGLE.value) #Angle to next creature
		self._add_input_node(InputNodeType.OTHER_CREATURE_DISTANCE.value) #Distance to next creature
		self._add_input_node(InputNodeType.OTHER_CREATURE_SIZE.value) #Size of next creature
		self._add_input_node(InputNodeType.OTHER_CREATURE_ENERGY.value) #Enerngy of next creature
		self._add_input_node(InputNodeType.OTHER_CREATURE_FOUND_STATUS.value) #Next creature found status

		#Food related input
		self._add_input_node(InputNodeType.FOOD_ANGLE.value) #Angle to next creature
		self._add_input_node(InputNodeType.FOOD_DISTANCE.value) #Distance to next creature
		self._add_input_node(InputNodeType.FOOD_FOUND_STATUS.value) #Food found status

		#Self related input
		self._add_input_node(InputNodeType.SELF_ENERNGY.value) #Energy
		self._add_input_node(InputNodeType.SELF_SIZE.value) #Size
		self._add_input_node(InputNodeType.SELF_SPEED.value) #Speed

		#------------------------------------------------------------------
		#OUTPUT NODES
		#------------------------------------------------------------------
		#Movement related input
		self._add_output_node(OutputNodeType.MOVE_STATUS.value) #Move status output
		self._add_output_node(OutputNodeType.MOVE_ANGLE.value) #Move angle output
		self._add_output_node(OutputNodeType.MOVE_SPEED.value) #Move speed output

		#Eating related input
		self._add_output_node(OutputNodeType.EAT_STATUS.value) #Eat status output

		#Reproduction related input
		self._add_output_node(OutputNodeType.REPRODUCE_STATUS.value) #Reproduce status output

		self.__set_up_genes()

	def __set_up_genes(self):
		bias_node_id = 0
		genes = []

		for out_node_id in self.output_node_ids:
			for in_node_id in self.input_node_ids:
				gene = Gene(in_node = in_node_id, out_node = out_node_id, weight = self.__get_random_weight(), enabled = True)
				genes.append(gene)

			gene = Gene(in_node = bias_node_id, out_node = out_node_id, weight = self.__get_random_weight(), enabled = True)
			genes.append(gene)

		self.set_genes(genes)

	def __get_random_weight(self):
		return  10 - 20.0*random.random()

class Mutator(NEAT):
	def __init__(self):
		super().__init__()

		self.new_node_prob = 0.01
		self.new_connection_prob = 0.2
		self.set_new_weight_prob = 0.31
		self.new_activation_status_prob = 0.33
		self.modify_weight_prob = 0.5
		self.max_network_size = 30

		self.weight_modification_variation = 0.1
		self.weight_setting_variation = 10.0

class SmartCreature(Creature):
	def __init__(self, world):
		super().__init__(world)

		self.mutator = Mutator()
		self.brain = Brain()

	def copy(self, other):
		super().copy(other)

		self.mutator = copy.deepcopy(other.mutator)
		self.brain = copy.deepcopy(other.brain)

	def move(self):
		dist_food = self._find_food()
		dist_enemy = self._find_enemy()
		input_values = self.__set_up_brain_input_values(dist_food, dist_enemy)

		ret_vals = self.brain.execute(input_values)
		self.__process_output(ret_vals)

	def __process_output(self, ret_vals):
		if ret_vals[OutputNodeType.MOVE_STATUS.value] > 0.5:
			self.__get_new_position(ret_vals[OutputNodeType.MOVE_ANGLE.value], ret_vals[OutputNodeType.MOVE_SPEED.value]) 

	def __get_new_position(self, angle, speed):
		dist_vec = self.position = np.array([math.sin(angle), math.cos(angle), 0.0])
		dist_vec *= speed*self.speed

		self.position += dist_vec

	def __set_up_brain_input_values(self, dist_food, dist_enemy):
		input_values = []

		self.__set_brain_with_other_creature_input_values(input_values, dist_enemy)
		self.__set_brain_with_food_input_values(input_values, dist_food)

		return input_values

	def __set_brain_with_other_creature_input_values(self, input_values, dist_enemy):
		if dist_enemy[1]:
			input_values.append((self.__get_angle(dist_enemy), InputNodeType.OTHER_CREATURE_ANGLE.value))
			input_values.append((dist_enemy[0], InputNodeType.OTHER_CREATURE_DISTANCE.value))
			input_values.append((dist_enemy[1].size, InputNodeType.OTHER_CREATURE_SIZE.value))
			input_values.append((dist_enemy[1].energy, InputNodeType.OTHER_CREATURE_ENERGY.value))
			input_values.append((1, InputNodeType.OTHER_CREATURE_FOUND_STATUS.value))
		else:
			input_values.append((0, InputNodeType.OTHER_CREATURE_ANGLE.value))
			input_values.append((0, InputNodeType.OTHER_CREATURE_DISTANCE.value))
			input_values.append((0, InputNodeType.OTHER_CREATURE_SIZE.value))
			input_values.append((0, InputNodeType.OTHER_CREATURE_ENERGY.value))
			input_values.append((0, InputNodeType.OTHER_CREATURE_FOUND_STATUS.value))

	def __set_brain_with_food_input_values(self, input_values, dist_food):
		if dist_food[1]:
			input_values.append((self.__get_angle(dist_food), InputNodeType.FOOD_ANGLE.value))
			input_values.append((dist_food[0], InputNodeType.FOOD_DISTANCE.value))
			input_values.append((1, InputNodeType.FOOD_FOUND_STATUS.value))
		else:
			input_values.append((0, InputNodeType.FOOD_ANGLE.value))
			input_values.append((0, InputNodeType.FOOD_DISTANCE.value))
			input_values.append((0, InputNodeType.FOOD_FOUND_STATUS.value))

	def __get_angle(self, dist_other):
		vec = (dist_other[1].position - self.position)/dist_other[0]

		return math.sin(vec[0])