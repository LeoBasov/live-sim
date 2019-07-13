#!/usr/bin/env python3

import pygame, sys
from pygame.locals import *

import sys
sys.path.append('../../.')

#initiize pygame constants
FPS = 30
RESOLUTION = (800, 800)

def main():
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
		display_surf.fill((0, 0, 0))
		draw_hud(display_surf)

		pygame.display.update()
		fps_clock.tick(FPS)

def draw_hud(display_surf):
	display_surf.fill((100, 100, 100))

if __name__ == "__main__":
	main()