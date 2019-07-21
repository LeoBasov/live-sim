import unittest
import sys

sys.path.append('../.')

import live_sim.smart_creature as sc

class UtilityTest(unittest.TestCase):
	def test_brain(self):
		brain = sc.Brain()

	def test_mutator(self):
		mutator  = sc.Mutator()