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

	def scroll(self, world):
		scrolled_dist = [0.0, 0.0]

		if self.active:
			self.pos_new = pygame.mouse.get_pos()

			scrolled_dist[0] = self.pos_new[0] - self.pos_old[0]
			scrolled_dist[1] = self.pos_new[1] - self.pos_old[1]

			self.pos_old = self.pos_new

			self._move_world(world)

	def _move_world(self, world):
		pass