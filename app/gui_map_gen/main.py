#!/usr/bin/env python3

import pygame, sys
from pygame.locals import *

import sys
sys.path.append('../../.')

from live_sim.map_gen import Generator

#initiize pygame constants
FPS = 30
RESOLUTION = (500, 500)

def main():
	water_level = 0.0
	weight_frequencies = ((0.5, 10), (0.25, 20))
	scroller = Scroller(0.01)

	generator = Generator()
	height_map = generator.generate_map(RESOLUTION, weight_frequencies)

	#initiize pygame instant
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	fps_clock = pygame.time.Clock()
	display_surf = pygame.display.set_mode(RESOLUTION)
	pygame.display.set_caption('Live Sim')

	while True: # the main game loop
		events = pygame.event.get()

		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		scroller.handle_events(events)
		scroller.process()

		water_level = scroller.get_water_level()

		#draw scenary
		draw_map(display_surf, height_map, water_level)

		pygame.display.update()
		fps_clock.tick(FPS)

def draw_map(display_surf, height_map, water_level):
	for y in range(len(height_map.pixels)):
		for x in range(len(height_map.pixels[y])):
			value = height_map.pixels[y][x]

			if value < water_level:
				display_surf.set_at((x, y), (0, 0, 255))

			elif value < 0.1 + water_level:
				display_surf.set_at((x, y), (255, 255, 0))
				
			elif value < 0.2 + water_level:
				display_surf.set_at((x, y), (0, 255, 0))
				
			elif value < 0.3 + water_level:
				display_surf.set_at((x, y), (0, 155, 0))
				
			elif value < 0.4 + water_level:
				display_surf.set_at((x, y), (255, 255, 255))
				
			elif value < 0.5 + water_level:
				display_surf.set_at((x, y), (155, 155, 0))
				
			else:
				display_surf.set_at((x, y), (255, 255, 255))
				
			"""else:
				display_surf.set_at((x, y), (255*value, 255*value, 255*value))"""

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
			elif event.type == MOUSEBUTTONUP and event.button == 1:
				self.active = False
			elif event.type == MOUSEBUTTONUP and event.button == 4:
				self.total_offset[1] += self.scaling_factor
			elif event.type == MOUSEBUTTONUP and event.button == 5:
				self.total_offset[1] -= self.scaling_factor
			if event.type == KEYDOWN and event.key == K_r:
				self.reset = True

	def _scroll(self):
		if self.active:
			scrolled_dist = [0.0, 0.0]
			self.pos_new = pygame.mouse.get_pos()

			scrolled_dist[0] = (self.pos_new[0] - self.pos_old[0])*self.scaling_factor
			scrolled_dist[1] = (self.pos_new[1] - self.pos_old[1])*self.scaling_factor

			self.total_offset[0] -= scrolled_dist[0]
			self.total_offset[1] -= scrolled_dist[1]

			self.pos_old = self.pos_new

	def process(self):
		self._scroll()

	def get_water_level(self):
		if self.total_offset[1] >= 1.0:
			return 1.0
		elif self.total_offset[1] <= 0.0:
			return 0.0
		else:
			return self.total_offset[1]

if __name__ == "__main__":
	main()