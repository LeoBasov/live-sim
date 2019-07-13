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

from opensimplex import OpenSimplex
import math

class Generator:
	def __init__(self):
		self.noise_gen = OpenSimplex()

	def rest_noise_gen(self):
		self.noise_gen = OpenSimplex()

	def noise(self, x, y):
		# Rescale from -1.0:+1.0 to 0.0:1.0
		return self.noise_gen.noise2d(x, y)/2.0 + 0.5

	def generate_map(self, resolution, weight_frequencies = ((1, 1),)):
		game_map = Map(resolution)

		for y in range(resolution[1]):
			for x in range(resolution[0]):
				for weight_frequency in weight_frequencies:
					weight = weight_frequency[0]
					frequency = weight_frequency[1]
					game_map.pixels[y][x] += weight*math.pow(self.noise(frequency*x/resolution[0], frequency*y/resolution[1]), 4.0)

		return game_map

class Map:
	def __init__(self, resolution):
		self.pixels = self._gen_map(resolution)

	def _gen_map(self, resolution):
		pixels = [[0] * resolution[0] for i in range(resolution[1])]

		return pixels

class Pixel:
	def __init__(self):
		self.height = 0