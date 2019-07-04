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

class World:
	def __init__(self):
		self.size = [100.0, 100.0]
		self.creatures = []

	def generate_creatures(self, number):
		for i in range(number):
			creature = Creature(self)

			self.creatures.append(creature)

	def update_creatures(self):
		for creature in self.creatures:
			creature.update()

	def collision(self, position):
		if position[0] < self.size[0] and position[0] > 0 and position[1] < self.size[1] and position[1] > 0:
			return False
		else:
			return True