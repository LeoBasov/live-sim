#!/usr/bin/env python3

import sys
sys.path.append('../.')

from live_sim.creature import Creature

def main():
	crt = Creature(1)

	print(crt.position)

if __name__ == "__main__":
	main()