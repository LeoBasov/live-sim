import pygame, sys
from pygame.locals import *

class Scroller:
	def __init__(self, scaling_factor = 1.0):
		self.active = False
		self.reset = False
		self.pos_old = [0.0, 0.0]
		self.pos_new = [0.0, 0.0]
		self.total_offset = [0.0, 0.0]
		self.scaling_factor = scaling_factor

	def handle_events(self, events):
		for event in events:
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				self.active = True
				self.pos_old = pygame.mouse.get_pos()
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					self.active = False

			if event.type == KEYDOWN and event.key == K_r:
				self.reset = True

	def process(self, world):
		self._reset(world)
		self._scroll(world)

	def _scroll(self, world):
		scrolled_dist = [0.0, 0.0]

		if self.active:
			self.pos_new = pygame.mouse.get_pos()

			scrolled_dist[0] = (self.pos_new[0] - self.pos_old[0])/self.scaling_factor
			scrolled_dist[1] = (self.pos_new[1] - self.pos_old[1])/self.scaling_factor

			self.total_offset[0] -= scrolled_dist[0]
			self.total_offset[1] -= scrolled_dist[1]

			self.pos_old = self.pos_new

			self._move_world(world, scrolled_dist)

	def _reset(self, world):
		if self.reset:
			self._move_world(world, self.total_offset)

			self.reset = False
			self.total_offset = [0.0, 0.0]

	def _move_world(self, world, scrolled_dist):
		for row in world.tiles:
			for tile in row:
				tile.position[0] = tile.position[0] + scrolled_dist[0]
				tile.position[1] = tile.position[1] + scrolled_dist[1]