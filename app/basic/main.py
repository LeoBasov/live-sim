#!/usr/bin/env python3

import sys
sys.path.append('../../.')

from live_sim.world import World
from os import system
from time import sleep
import math
import csv

def main():
	with open('numbers.csv', '+w', newline='') as csvfile:
		number_writer = csv.writer(csvfile, delimiter=',')

		wrld = World()

		creature_number = 100
		creature_sense = 3.5
		creature_speed = 0.16
		creature_size = 1.0

		food_number = 10
		number_cycles = 100

		print("World created")
		print(80*"-")

		wrld.generate_creatures(creature_number, creature_sense, creature_speed, creature_size)

		print("Creatures created. Number  = ", len(wrld.creatures))
		print(80*"-")

		wrld.generate_food(food_number)

		print("Food created. Number  = ", len(wrld.food))
		print(80*"-")

		print_world(wrld, 0)

		for j in range(number_cycles):
			write_state("sate_", j, wrld)

			for i in range(24):
				number_writer.writerow([len(wrld.creatures), len(wrld.food)])
				wrld.update()

				print_world(wrld, j + 1)
				sleep(0.1)

				if not len(wrld.creatures):
					break

				if wrld.time == 0:
					wrld.generate_food(food_number)

			if not len(wrld.creatures):
				break

def print_world(wrld, cycle):
	"""prt = []

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

		prt[y][x] = "O"""

	system('clear')

	print("Cycle number:", cycle)
	print("Time of day:", wrld.time, "o'clock")

	"""for val in prt:
		print(val)"""

	print("Creatures", len(wrld.creatures))
	print("food", len(wrld.food))

def write_state(name, cycle, wrld):
	speeds = []
	senses = []
	sizes = []

	for creature in wrld.creatures:
		speeds.append(creature.speed)
		senses.append(creature.sense)
		sizes.append(creature.size)

	with open(name + str(cycle + 1) + '.csv', '+w', newline='') as csvfile:
		state_writer = csv.writer(csvfile, delimiter=',')
		state_writer.writerow(speeds)
		state_writer.writerow(senses)
		state_writer.writerow(sizes)

if __name__ == "__main__":
	main()