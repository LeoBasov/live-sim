import pygame, sys
from pygame.locals import *

class Scroller:
	def __init__(self):
		self.active = False
		self.pos_old = [0.0, 0.0]
		self.pos_new = [0.0, 0.0]

	def handle_events(self, events):
		for event in events:
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				self.active = True
				self.pos_old = pygame.mouse.get_pos()
			if event.type == MOUSEBUTTONUP:
				if event.button == 1:
					self.active = False

	def scroll(self, world, scaling_factor):
		scrolled_dist = [0.0, 0.0]

		if self.active:
			self.pos_new = pygame.mouse.get_pos()

			scrolled_dist[0] = (self.pos_new[0] - self.pos_old[0])/scaling_factor
			scrolled_dist[1] = (self.pos_new[1] - self.pos_old[1])/scaling_factor

			self.pos_old = self.pos_new

			self._move_world(world, scrolled_dist)

	def _move_world(self, world, scrolled_dist):
		for row in world.tiles:
			for tile in row:
				tile.position[0] = tile.position[0] + scrolled_dist[0]
				tile.position[1] = tile.position[1] + scrolled_dist[1]