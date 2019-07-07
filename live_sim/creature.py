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

import random
import math
import numpy as np
import sys

class Creature:
	"""Docstring for creaure class"""

	def __init__(self, world):
		self.state = State()
		self.world = world
		self.energy_init = 10.0
		self.energy = self.energy_init
		self.speed = 1.0
		self.sense = 1.0
		self.position = np.array([0.0, 0.0, 0.0])
		self.reproduction_threshold = 0.0

	def copy(self, other):
		self.state = other.state
		self.world = other.world 
		self.energy_init = other.energy_init
		self.energy = other.energy
		self.speed = other.speed
		self.sense = other.sense
		self.position = other.position

	def update(self):
		if self.state.reproducing:
			self._repoduce()

		if self.state.consuming:
			self._consume_energy()

		if self.state.moving:
			self._move()

	def _repoduce(self):
		if self.energy > (self.energy_init + self.energy_init * self.reproduction_threshold):
			self.energy *= 0.5

			creature = Creature(self.world)

			creature.copy(self)
			creature.energy = self.energy_init

			self._mutate(creature)

			self.world.creatures.append(creature)

	def _mutate(self, creature):
		self._mutate_speed(creature)
		self._mutate_sense(creature)

	def _mutate_speed(self, creature):
		creature.speed = (1.1 - 0.2*random.random())*creature.speed

	def _mutate_sense(self, creature):
		creature.sense = (1.1 - 0.2*random.random())*creature.sense

	def _consume_energy(self):
		self.energy -= self.speed*self.speed

		if self.energy <= 0.0:
			self.state = Dead()

	def _move(self):
		dist = self._find_food()

		if dist[1] == None:
			self.position = self._get_new_pos_random()
		else:
			dist_vec = dist[1].position - self.position
			dist_scal = np.linalg.norm(dist_vec)
			speed = min(dist_scal, self.speed)
			
			if dist_scal > 0.0:
				self.position = self.position + (speed/dist_scal)*dist_vec

			if(speed < 0.5*self.speed):
				self._eat(dist[1])

	def _eat(self, food):
		self.energy += food.energy
		food.eaten = True

	def _find_food(self):
		dist = [sys.float_info.max, None]

		for food in self.world.food:
			dist_new = np.linalg.norm(self.position - food.position)

			if dist_new <= self.sense:
				dist[0] =  dist_new
				dist[1] = food

				break

		return dist

	def _get_new_pos_random(self):
		degree = 2.0*random.random()*math.pi
		pos_diff = np.array([self.speed*math.sin(degree), self.speed*math.cos(degree), 0.0])
		position_new =  self.position + pos_diff

		while self.world.collision(position_new):
			degree = 2.0*random.random()*math.pi
			pos_diff = np.array([self.speed*math.sin(degree), self.speed*math.cos(degree), 0.0])
			position_new =  self.position + pos_diff

		return position_new

class State:
	"""Base state class representing the state of the creature"""
	def __init__(self):
		self.name  = "base_state"
		self.alive = True
		self.reproducing = True
		self.consuming = True
		self.moving = True

class Dead(State):
	"""docstring for Dead"""
	def __init__(self):
		super().__init__()

		self.name  = "dead"
		self.alive = False
		self.reproducing = False
		self.consuming = False
		self.moving = False