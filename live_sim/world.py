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

from .creature import Creature
import random
import math
import numpy as np

class World:
	def __init__(self):
		self.size = [20.0, 20.0]
		self.creatures = []
		self.food = []
		self.time = 0

	def generate_creatures(self, number, sense = 1.0, speed = 1.0, size = 1.0):
		for i in range(number):
			creature = Creature(self)
			creature.sense = (0.001 + 5.0*random.random())*sense
			creature.speed = (0.001 + 1.0*random.random())*speed
			creature.size = (0.001 + 3.0*random.random())*size
			creature.size_max = creature.size
			creature.position = self._generate_random_position()

			self.creatures.append(creature)

	def _generate_random_position(self):
		position = np.array([random.random()*self.size[0], random.random()*self.size[1], 0.0])

		while self.collision(position):
			position = np.array([random.random()*self.size[0], random.random()*self.size[1], 0.0])

		return position

	def _generate_position_on_border(self):
		position = np.array([0.0, 0.0, 0.0])
		i = math.ceil(random.random()*4.0)

		if i == 1:
			position[0] = 0.0
			position[1] = random.random()*self.size[1]
		elif i == 2:
			position[0] = self.size[0]
			position[1] = random.random()*self.size[1]
		elif i == 3:
			position[0] = random.random()*self.size[0]
			position[1] = 0.0
		elif i == 4:
			position[0] = random.random()*self.size[0]
			position[1] = self.size[1]

		return position

	def update(self):
		self._update_creatures()
		self._update_time()
		self._remove_entities()

	def _update_time(self):
		self.time += 1

		if self.time == 24:
			self.time = 0

	def _update_creatures(self):
		for creature in self.creatures:
			creature.grow()
			creature.move()
			creature.consume_energy()
			creature.fight()

		for creature in self.creatures:
			creature.reproduce()

	def _remove_entities(self):
		self._remove_food()
		self._remove_creatures()	

	def _remove_food(self):
		left_food = []

		for food in self.food:
			if not food.eaten:
				left_food.append(food)

		self.food = left_food

	def _remove_creatures(self):
		left_creatures = []

		for creature in self.creatures:
			if creature.state.alive:
				left_creatures.append(creature)

		self.creatures = left_creatures

	def collision(self, position):
		if position[0] < self.size[0] and position[0] > 0 and position[1] < self.size[1] and position[1] > 0:
			return False
		else:
			return True

	def generate_food(self, number):
		for i in range(number):
			food = Food()
			food.position = self._generate_random_position()

			self.food.append(food)

class Food:
	def __init__(self):
		self.eaten = False
		self.energy = 5.0
		self.position = np.array([0.0, 0.0, 0.0])