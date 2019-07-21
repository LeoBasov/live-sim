import unittest
import sys

sys.path.append('../.')

import live_sim.smart_creature as sc
from live_sim.world import World

class UtilityTest(unittest.TestCase):
	def test_brain(self):
		brain = sc.Brain()

	def test_mutator(self):
		mutator  = sc.Mutator()

	def test_creature(self):
		world = World()
		mutator  = sc.SmartCreature(world)