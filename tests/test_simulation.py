#!/usr/bin/env python


import unittest
from particlesim import Animation


class ParticleSimTest(unittest.TestCase):

    def test_generate_correct_particle_display(self):
        init_state = 'LRLR.LRLR'

        animation = Animation()
        svec = animation.generate_particle_state_vector(2, init_state)
        display = animation.readout(svec, len(init_state))
        print(display)
        self.assertEqual(display.count('X'), 8)        

