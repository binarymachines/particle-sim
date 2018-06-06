#!/usr/bin/env python


import unittest
from particlesim import Animation


class ParticleSimTest(unittest.TestCase):

    def test_correct_state_vector_generation(self):
        init_state = 'LRR.....'
        speed = 5

        animation = Animation()
        state_vector = animation.generate_particle_state_vector(speed, init_state)
        self.assertEqual(len(state_vector), 3)
        for particle in state_vector:
            self.assertEqual(particle.speed, speed)
        self.assertEqual(state_vector[0].direction, 'L')
        self.assertEqual(state_vector[1].direction, 'R')
        self.assertEqual(state_vector[2].direction, 'R')

        for i in range(len(state_vector)):
            self.assertEqual(state_vector[i].position, i)


    def test_generate_correct_particle_display(self):
        init_state = 'LRLR.LRLR'
        speed = 2

        animation = Animation()
        svec = animation.generate_particle_state_vector(speed, init_state)
        display = animation.readout(svec, len(init_state))
        
        self.assertEqual(display.count('X'), 8)
        self.assertEqual(display, '[XXXX.XXXX]')        


    def test_generate_correct_chamber_particle_count(self):
        init_state = 'LRL....'
        speed = 2
        chamber_size = len(init_state)
        animation = Animation()
        svec = animation.generate_particle_state_vector(speed, init_state)
        
        self.assertEqual(animation.num_particles_in_chamber(svec, chamber_size), 3)        


    def test_particle_exit_logic(self):
        init_state = 'RL...R'
        speed = 2
        chamber_size = len(init_state)
        animation = Animation()
        svec = animation.generate_particle_state_vector(speed, init_state)

        initial_count = animation.num_particles_in_chamber(svec, chamber_size)
        self.assertEqual(initial_count, 3)

        # two of the three initial particles should exit the chamber on this update, based on 
        # their speed and direction
        new_svec = animation.update(svec)

        final_count = animation.num_particles_in_chamber(new_svec, chamber_size)
        self.assertEqual(final_count, 1)

        # particles remain in the simulation even when they exit the chamber
        self.assertEqual(len(new_svec), initial_count)


    def test_detect_empty_chamber(self):
        init_state = '.....'
        speed = 1
        chamber_size = len(init_state)
        a = Animation()
        svec = a.generate_particle_state_vector(speed, init_state)
        self.assertTrue(a.particles_have_all_exited_chamber(svec, chamber_size))


    def test_particle_display_and_motion_logic(self):
        init_state = '.R....L'
        speed = 2
        chamber_size = len(init_state)
        a = Animation()
        svec = a.generate_particle_state_vector(speed, init_state)
        new_svec = a.update(svec)

        # strip brackets; we are counting dots, not framing characters
        display_string = a.readout(new_svec, chamber_size).lstrip('[').rstrip(']')

        self.assertEqual(display_string.count('X'), 2)
        self.assertEqual(display_string[3], 'X')
        self.assertEqual(display_string[4], 'X')


    def test_particle_superposition_display_logic(self):
        init_state = '..R.L..'
        speed = 1
        chamber_size = len(init_state)
        a = Animation()
        state_vector = a.generate_particle_state_vector(speed, init_state)
        new_svec = a.update(state_vector)
        display = a.readout(new_svec, chamber_size)

        # two particles may occupy the same position in the simulation
        self.assertEqual(display.count('X'), 1)
        self.assertEqual(len(new_svec), 2)