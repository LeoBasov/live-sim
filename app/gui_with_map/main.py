#!/usr/bin/env python3

import pygame, sys
from pygame.locals import *

import sys
sys.path.append('../../.')

from live_sim.map import Map

def main():
	#Set up sim
	game_map = Map()

	#initiize pygame
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	FPS = 30
	fps_clock = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((1200, 800))
	pygame.display.set_caption('Live Sim')

	while True: # the main game loop
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()
		fps_clock.tick(FPS)

if __name__ == "__main__":
	main()