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

sys.path.append('../../neat-python/.')

from neat.network import Node
from neat.network import Gene
from neat.network import Network
from neat.neat import NEAT

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

		node_id = 0

		#Other creature related input
		node_id = self.__add_input_node(node_id) #Angle to next creature
		node_id = self.__add_input_node(node_id) #Distance to next creature

		node_id = self.__add_output_node(node_id)

		self.__set_up_genes()

	def __set_up_genes(self):
		bias_node_id = 0
		genes = []

		for in_node_id in self.input_node_ids:
			for out_node_id in self.output_node_ids:
				gene1 = Gene(in_node = in_node_id, out_node = out_node_id, weight = self.__get_random_weight(), enabled = True)
				gene2 = Gene(in_node = bias_node_id, out_node = out_node_id, weight = self.__get_random_weight(), enabled = True)
				
				genes.append(gene1)
				genes.append(gene2)

		self.set_genes(genes)

	def __get_random_weight(self):
		return  10 - 20.0*random.random()

	def __add_input_node(self, node_id):
		self._add_input_node(node_id)

		return node_id + 1

	def __add_output_node(self, node_id):
		self._add_output_node(node_id)

		return node_id + 1

class Mutator(NEAT):
	def __init__(self):
		super().__init__()

class SmartCreature:
	pass