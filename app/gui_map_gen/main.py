#!/usr/bin/env python3

import pygame, sys
from pygame.locals import *

import sys
sys.path.append('../../.')

from live_sim.map_gen import Generator

#initiize pygame constants
FPS = 30
RESOLUTION = (800, 800)

def main():
	generator = Generator()
	height_map = generator.generate_map(RESOLUTION, 10)

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

		#draw scenary
		draw_map(display_surf, height_map)

		pygame.display.update()
		fps_clock.tick(FPS)

def draw_map(display_surf, height_map):
	for y in range(len(height_map.pixels)):
		for x in range(len(height_map.pixels[y])):
			display_surf.set_at((x, y), (255*height_map.pixels[y][x], 255*height_map.pixels[y][x], 255*height_map.pixels[y][x]))

if __name__ == "__main__":
	main()