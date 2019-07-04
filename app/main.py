#!/usr/bin/env python3

import sys
sys.path.append('../.')

from live_sim.world import World
from os import system
from time import sleep

def main():
	wrld = World()

	print("World created")
	print(80*"-")

	wrld.generate_creatures(10)

	print("Creatures created. Number  = ", len(wrld.creatures))
	print(80*"-")

	print_world(wrld)

	for i in range(10):
		wrld.update_creatures()

		print_world(wrld)
		sleep(0.1)

def print_world(wrld):
	prt = []

	for i in range(int(wrld.size[1])):
		prt_loc = []

		for j in range(int(wrld.size[0])):
			prt_loc.append(".")

		prt.append(prt_loc)

	for creature in wrld.creatures:
		prt[int(creature.position[1])][int(creature.position[0])] = "X"

	system('clear')

	for val in prt:
		print(val)

if __name__ == "__main__":
	main()