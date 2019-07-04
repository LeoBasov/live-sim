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

class Creature:
	"""Docstring for creaure class"""

	def __init__(self, world):
		self.state = State()
		self.world = world
		self.energy = 1.0
		self.position = [0.0, 0.0, 0.0]

	def update(self):
		self._check_if_has_died()
		self._repoduce()
		self._consume_energy()
		self._move()

	def _check_if_has_died(self):
		"""Checks if the creature died to some cicumstances"""
		pass

	def _repoduce(self):
		pass

	def _consume_energy(self):
		pass

	def _move(self):
		pass

class State:
	"""Base state class representing the state of the creature"""
	def __init__(self):
		self.name  = "base_state"
		self.alive = True
		self.reproducing = True
		self.consuming = True
		self.moving = True