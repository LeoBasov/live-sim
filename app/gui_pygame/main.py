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
BLACK = (0, 0, 0)

def main():
	#initiize pygame
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	FPS = 30
	fps_clock = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((850, 850), 0, 32)
	pygame.display.set_caption('Live Sim')
	
	wrld = World()

	creature_number = 10
	creature_sense = 1.0
	creature_speed = 1.0
	creature_size = 1.0

	food_number = 5
	number_cycles = 100

	reset(wrld, creature_number, creature_sense, creature_speed, creature_size, food_number)

	RUN = False

	while True: # the main game loop
		DISPLAYSURF.fill(WHITE)
		draw_frame(DISPLAYSURF)
		max_speed = 0
		min_speed = sys.float_info.max

		for creature in wrld.creatures:
			if creature.speed > max_speed:
				max_speed = creature.speed

			if creature.speed < min_speed:
				min_speed = creature.speed

		for creature in wrld.creatures:
			point = (25 + 40*creature.position[0], 25 + 40*creature.position[1], 25 + 40*creature.position[2])
			_draw_point(DISPLAYSURF, point, get_color(creature.speed, max_speed, min_speed), int(max(1, creature.size*20)))

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
				elif event.key == K_r:
					reset(wrld, creature_number, creature_sense, creature_speed, creature_size, food_number)

		pygame.display.update()
		fps_clock.tick(FPS)

		if RUN:
			if len(wrld.creatures) == 0:
				RUN = False

			wrld.update()

			if wrld.time == 0:
				wrld.generate_food(food_number)

def reset(wrld, creature_number, creature_sense, creature_speed, creature_size, food_number):
	wrld.creatures = []
	wrld.food = []

	wrld.generate_creatures(creature_number, creature_sense, creature_speed, creature_size)
	wrld.generate_food(food_number)

def draw_frame(display_surf):
	pygame.draw.rect(display_surf, (0, 0, 0), (20, 20, 850 - 40, 850 - 40), 5)

def _draw_point(surface_surf, point, color, size = 5):
		pygame.draw.circle(surface_surf, color, (int(point[0]), int(point[1])), size, 0)
		pygame.draw.circle(surface_surf, BLACK, (int(point[0]), int(point[1])), size, min(size, 1))

def get_color(value, value_max, value_min):
	R = 0
	G = 0
	B = 0

	dist = value_max - value_min

	if value < 0.5*value_max:
		R = 0
		G = 255*((value - value_min)/(0.5*dist))
		B = 255 - 255*((value - value_min)/(0.5*dist))
	elif value > 0.5*value_max  and value < value_max:
		R = 255*((value - value_min)/(dist))
		G = 255 - 255*((value - value_min)/(dist))
		B = 0
	else:
		R = 255
		G = 0
		B = 0

	return (R, G, B)

if __name__ == "__main__":
	main()