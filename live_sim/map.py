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

class Map:
	def __init__(self, coords = (10, 10)):
		self.tiles = [[]]
		self.tile_size = 2.0

		self.set_up(coords)

	def set_up(self, coords):
		self.tiles = []

		for x in range(coords[0]):
			row = []

			for y in range(coords[1]):
				tile  = Tile()

				tile.position[0] = x*self.tile_size + 0.5*self.tile_size
				tile.position[1] = y*self.tile_size + 0.5*self.tile_size

				row.append(tile)

			self.tiles.append(row)

class Tile:
	def __init__(self):
		self.position = [0, 0]