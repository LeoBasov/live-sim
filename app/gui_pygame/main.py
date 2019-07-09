#!/usr/bin/env python3

import pygame, sys
from pygame.locals import *

import sys
sys.path.append('../../.')

from live_sim.world import World
from os import system
from time import sleep
import math
import csv

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def main():
	#initiize pygame
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	FPS = 30
	fps_clock = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((850, 850), 0, 32)
	pygame.display.set_caption('Live Sim')
	
	wrld = World()

	creature_number = 100
	creature_sense = 3.5
	creature_speed = 0.16
	creature_size = 1.0

	food_number = 10
	number_cycles = 100

	wrld.generate_creatures(creature_number, creature_sense, creature_speed, creature_size)
	wrld.generate_food(food_number)

	RUN = False

	while True: # the main game loop
		DISPLAYSURF.fill(WHITE)
		draw_frame(DISPLAYSURF)

		for creature in wrld.creatures:
			point = (25 + 40*creature.position[0], 25 + 40*creature.position[1], 25 + 40*creature.position[2])
			_draw_point(DISPLAYSURF, point, BLUE)

		for food in wrld.food:
			point = (25 + 40*food.position[0], 25 + 40*food.position[1], 25 + 40*food.position[2])
			_draw_point(DISPLAYSURF, point, GREEN)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					RUN = not RUN

		pygame.display.update()
		fps_clock.tick(FPS)

		if RUN:
			wrld.update()

			if wrld.time == 0 and len(wrld.creatures) > 0:
				wrld.generate_food(food_number)

def draw_frame(display_surf):
	pygame.draw.rect(display_surf, (0, 0, 0), (25, 25, 850 - 50, 850 - 50), 5)

def _draw_point(surface_surf, point, color, size = 5):
		pygame.draw.circle(surface_surf, color, (int(point[0]), int(point[1])), size, 0)

if __name__ == "__main__":
	main()