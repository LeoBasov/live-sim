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
		creature  = sc.SmartCreature(world)

	def test_copy(self):
		world = World()
		creature1 = sc.SmartCreature(world)
		creature2 = sc.SmartCreature(world)

		creature1.speed = 3.0
		creature2.speed = 7.0

		self.assertEqual(creature1.speed, 3.0)
		self.assertEqual(creature2.speed, 7.0)

		creature1.copy(creature2)

		self.assertEqual(creature1.speed, 7.0)
		self.assertEqual(creature2.speed, 7.0)