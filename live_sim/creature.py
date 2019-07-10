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

BASE_ENERGY = 10

class Creature:
	"""Docstring for creaure class"""

	def __init__(self, world):
		self.state = State()
		self.world = world
		self.energy_init = BASE_ENERGY
		self.energy = self.energy_init
		self.speed = 1.0
		self.sense = 1.0
		self.size = 1.0
		self.size_max = 1.0
		self.position = np.array([0.0, 0.0, 0.0])
		self.reproduction_threshold = 0.0
		self.children = []
		self.move_counter = 0
		self.move_counter_max = 10
		self.move_vector = np.array([0, 0, 0])

	def copy(self, other):
		self.state = other.state
		self.world = other.world 
		self.energy_init = other.energy_init
		self.energy = other.energy
		self.speed = other.speed
		self.sense = other.sense
		self.size = other.size
		self.size_max = other.size_max
		self.position = other.position
		self.reproduction_threshold = other.reproduction_threshold

	def reproduce(self):
		if self.state.reproducing:
			self._repoduce()

	def consume_energy(self):
		if self.state.consuming:
			self._consume_energy()

	def move(self):
		if self.state.moving:
			self._move()

	def grow(self):
		if self.state.growing:
			self._grow()

	def _grow(self):
		if self.size >= self.size_max:
			self.state.growing = False
		else:
			self.size += self.size_max*0.1

	def _find_enemy(self):
		dist = [sys.float_info.max, None]

		for creature in self.world.creatures:
			if (creature.state.alive == True) and (creature != self) and creature not in self.children:

				dist_new = np.linalg.norm(self.position - creature.position)

				if (dist_new <= self.sense) and (dist_new < dist[0]):
					dist[0] =  dist_new
					dist[1] = creature

		return dist

	def _repoduce(self):
		if self.energy > (self.energy_init + self.energy_init * self.reproduction_threshold):
			self.energy *= 0.5

			creature = Creature(self.world)

			creature.copy(self)

			self._mutate(creature)
			self._reproduce_position(creature)

			creature.energy_init = creature.size*creature.size*creature.size*BASE_ENERGY
			creature.energy = creature.energy_init

			self.children.append(creature)
			self.world.creatures.append(creature)

	def _reproduce_position(self, child):
		position = self._get_new_pos_random()

		dist_vec = position - self.position
		dist = np.linalg.norm(dist_vec)

		child.position = self.position + ((0.5*self.size + 0.5*child.size)/dist)*dist_vec

		while self.world.collision(child.position):
			position = self._get_new_pos_random()

			dist_vec = position - self.position
			dist = np.linalg.norm(dist_vec)

			child.position = self.position + ((0.5*self.size + 0.5*child.size)/dist)*dist_vec

	def _mutate(self, creature):
		self._mutate_speed(creature)
		self._mutate_sense(creature)
		self._mutate_size(creature)

	def _mutate_speed(self, creature):
		creature.speed = (1.1 - 0.2*random.random())*creature.speed

	def _mutate_sense(self, creature):
		creature.sense = (1.1 - 0.2*random.random())*creature.sense

	def _mutate_size(self, creature):
		creature.size_max = (1.1 - 0.2*random.random())*creature.size_max
		creature.size = 0.2*creature.size_max

	def _consume_energy(self):
		self.energy -= self.speed*self.speed*self.size*self.size*self.size

		if self.energy <= 0.0:
			self.state = Dead()

	def _move(self):
		dist_food = self._find_food()
		dist_enemy = self._find_enemy()

		if dist_food[1] == None and dist_enemy[1] == None:
			self.position = self._random_move()

		elif dist_food[1] != None and dist_enemy[1] == None:
			self._only_food(dist_food)

		elif dist_food[1] == None and dist_enemy[1] != None:
			self._only_enemy(dist_enemy)

		else:
			self._both(dist_food, dist_enemy)

	def _random_move(self):
		if self.move_counter == 0:
			position = self._get_new_pos_random()
			self.move_vector = (position - self.position)
			self.move_vector /= np.linalg.norm(self.move_vector)

		position_new = self.position + self.speed*self.move_vector

		if self.world.collision(position_new):
			self.move_counter = 0

			return self._random_move()

		self.move_counter += 1

		if self.move_counter > self.move_counter_max:
			self.move_counter = 0

		return position_new


	def _only_food(self, dist_food):
		self._get_food(dist_food)

	def _only_enemy(self, dist_enemy):
		if self.size > 1.2*dist_enemy[1].size:
			self._get_food(dist_enemy)
		elif 1.2*self.size < dist_enemy[1].size:
			self._flee(dist_enemy)
		else:
			self.position = self._random_move()

	def _flee(self, dist_enemy):
		dist_vec = dist_enemy[1].position - self.position
			
		if dist_enemy[0] > 0.0:
			position_new = self.position - (self.speed/dist_enemy[0])*dist_vec

			if not self.world.collision(position_new):
				self.position = position_new

	def _both(self, dist_food, dist_enemy):
		if (self._calc_rel_energy(dist_food) > self._calc_rel_energy(dist_enemy)) and (self.size > 1.2*dist_enemy[1].size):
			self._get_food(dist_enemy)
		elif (self._calc_rel_energy(dist_food) > self._calc_rel_energy(dist_enemy)) and (1.2*self.size > dist_enemy[1].size) and (dist_enemy[0] < dist_food[0]):
			self._flee(dist_enemy)
		else:
			self._get_food(dist_food)

	def _calc_rel_energy(self, dist):
		return dist[1].energy - dist[0]*self.speed

	def _get_food(self, food_pair):
		dist_vec = food_pair[1].position - self.position
		speed = min(food_pair[0], self.speed)
			
		if food_pair[0] > 0.0:
			self.position = self.position + (speed/food_pair[0])*dist_vec

		if food_pair[0] < 0.5*self.size:
			self.energy += food_pair[1].be_consumed()

	def _find_food(self):
		dist = [sys.float_info.max, None]

		for food in self.world.food:
			dist_new = np.linalg.norm(self.position - food.position)

			if (dist_new <= self.sense) and (dist_new < dist[0]):
				dist[0] =  dist_new
				dist[1] = food

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

	def be_consumed(self):
		self.state = Dead()

		return self.energy

class State:
	"""Base state class representing the state of the creature"""
	def __init__(self):
		self.name  = "base_state"
		self.alive = True
		self.reproducing = True
		self.consuming = True
		self.moving = True
		self.growing = True

class Dead(State):
	"""docstring for Dead"""
	def __init__(self):
		super().__init__()

		self.name  = "dead"
		self.alive = False
		self.reproducing = False
		self.consuming = False
		self.moving = False
		self.growing = False