#!/usr/bin/env python3

import sys
sys.path.append('../.')

from live_sim.world import World
from os import system
from time import sleep
import math

def main():
	wrld = World()

	print("World created")
	print(80*"-")

	wrld.generate_creatures(10)

	print("Creatures created. Number  = ", len(wrld.creatures))
	print(80*"-")

	wrld.generate_food(10)

	print("Food created. Number  = ", len(wrld.food))
	print(80*"-")

	print_world(wrld)

	for i in range(10):
		wrld.update()

		print_world(wrld)
		sleep(0.2)

def print_world(wrld):
	prt = []

	for i in range(int(wrld.size[1])):
		prt_loc = []

		for j in range(int(wrld.size[0])):
			prt_loc.append(".")

		prt.append(prt_loc)

	for creature in wrld.creatures:
		x = math.ceil(creature.position[0]) - 1
		y = math.ceil(creature.position[1]) - 1

		prt[y][x] = "X"

	for food in wrld.food:
		x = int(food.position[0])
		y = int(food.position[1])

		prt[y][x] = "O"

	system('clear')

	print("time of day:", wrld.time, "o'clock")

	for val in prt:
		print(val)

if __name__ == "__main__":
	main()