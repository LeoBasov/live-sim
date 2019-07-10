#!/usr/bin/env python3

import pygame, sys
from pygame.locals import *

import sys
sys.path.append('../../.')

from live_sim.map import Map
import graphics

#initiize pygame constants
FPS = 30

RESOLUTION = (1200, 800)
MAP_DISPLAY_SIZE = (800, 800)

def main():
	#Set up sim
	game_map = Map((20, 20))

	#initiize pygame instant
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	fps_clock = pygame.time.Clock()
	display_surf = pygame.display.set_mode(RESOLUTION)
	pygame.display.set_caption('Live Sim')

	#Set up stuff
	scaling_factor = get_scaling_factor(game_map)
	scroller = graphics.Scroller(scaling_factor)

	while True: # the main game loop
		events = pygame.event.get()
		scroller.handle_events(events)

		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		#prework graphics
		scroller.process(game_map)

		#draw scenary
		display_surf.fill((0, 0, 0))
		draw_tiles(display_surf, game_map, scaling_factor)
		draw_hud(display_surf)

		pygame.display.update()
		fps_clock.tick(FPS)

def draw_tiles(display_surf, game_map, scaling_factor, zoom = 1.0):
	for row in game_map.tiles:
		for tile in row:
			position = tile.position

			rect_left = (position[0] - 0.5*game_map.tile_size)*scaling_factor
			rect_top = (position[1] - 0.5*game_map.tile_size)*scaling_factor
			rect_width = game_map.tile_size*scaling_factor
			rect_height = game_map.tile_size*scaling_factor
			rect = pygame.Rect(rect_left, rect_top, rect_width, rect_height)

			display_surf.fill((0, 100, 50), rect)
			pygame.draw.rect(display_surf, (255, 255, 255), rect, 1)

def draw_hud(display_surf):
	display_surf.fill((0, 0, 0), (MAP_DISPLAY_SIZE[0], 0, RESOLUTION[0], RESOLUTION[1]))
	pygame.draw.rect(display_surf, (50, 100, 100), (MAP_DISPLAY_SIZE[0], 0, RESOLUTION[0], RESOLUTION[1]), 5)

def get_scaling_factor(game_map):
	if len(game_map.tiles) > len(game_map.tiles[0]):
		return MAP_DISPLAY_SIZE[0]/(len(game_map.tiles)*game_map.tile_size)
	else:
		return MAP_DISPLAY_SIZE[1]/(len(game_map.tiles[0])*game_map.tile_size)

if __name__ == "__main__":
	main()