#!/usr/bin/env python3

import sys
sys.path.append('../.')

from live_sim.world import World

def main():
	wrld = World()

	print("World created")
	print(80*"-")

	wrld.generate_creatures(1)

	print("Creatures created. Number  = ", len(wrld.creatures))
	print(80*"-")

	print(wrld.creatures[0].position)

	for i in range(10):
		wrld.update_creatures()

		print(wrld.creatures[0].position)

if __name__ == "__main__":
	main()