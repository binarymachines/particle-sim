#!/usr/bin/env python


''' Usage:     particlesim -s <speed> -i <initial_state>

'''


import os
import re
from collections import namedtuple
import docopt


ParticleState = namedtuple('ParticleState', 'position speed direction')
state_rx = re.compile(r'[LR.]+$')


class Animation(object):
    def __init__(self):
        pass

    def generate_particle_state_vector(self, particle_speed, initial_string):
        '''Turn the given string format into a list of immutable particle states
        '''
        v = []
        index = 0
        for value in initial_string:
            if value == 'L':
                v.append(ParticleState(position=index, speed=particle_speed, direction='L'))
            elif value == 'R':
                v.append(ParticleState(position=index, speed=particle_speed, direction='R'))
            index += 1
        return v


    def update(self, particle_state_vector):
        '''Perform a functional transfom of a particle state into a new state,
        based on its position and speed
        '''
        result = []
        for particle in particle_state_vector:
            new_direction = particle.direction
            new_speed = particle.speed
            if particle.direction == 'L':
                new_position = particle.position - particle.speed
            else: # direction is 'R'
                new_position = particle.position + particle.speed
            result.append(ParticleState(position=new_position, speed=new_speed, direction=new_direction))
        return result


    def particles_have_all_exited_chamber(self, particle_state_vector, chamber_size):
        '''Return true if none of the particles in the state vector have a position index within
        the virtual chamber specified by [0..<chamber_size>]
        ''' 
        return self.num_particles_in_chamber(particle_state_vector, chamber_size) == 0


    def run_simulation(self, state_vector, chamber_size):
        '''Perform the core animation logic, using a Pythonic generator.
        This is desirable in cases where the potential number of simulation states per run is very large.
        '''
        current_state_vector = state_vector
        while True:
            current_state_vector = self.update(current_state_vector)
            yield(current_state_vector)
            if self.particles_have_all_exited_chamber(current_state_vector, chamber_size):
                break


    def readout(self, state_vector, chamber_size):
        '''Generate a display string representing the positions of simulated particles
        in the chamber
        '''
        display = ['.' for i in range(chamber_size)]
        for particle in state_vector:
            if particle.position >=0 and particle.position < chamber_size:
                display[particle.position] = 'X'
        return '[%s]' % ''.join(display)


    def num_particles_in_chamber(self, state_vector, chamber_size):
        '''Return the number of simulated particles whose position index places them
        inside the chamber
        '''
        count = 0
        for particle in state_vector:
            if particle.position >=0 and particle.position < chamber_size:
                count += 1        
        return count


    def animate(self, speed, initial_state_string):
        if speed < 1 or speed > 10:
            raise Exception('invalid speed: %d. Particle speeds may range from 1 to 10.')

        if len(initial_state_string) > 50:
            raise Exception('no more than 50 particles allowed in simulation.')

        if not state_rx.match(initial_state_string):
            raise Exception('badly formatted state string. Valid characters are "L", "R", and "."')

        initial_state = self.generate_particle_state_vector(speed, initial_state_string)
        particle_chamber_size = len(initial_state_string)

        result = []
        result.append(self.readout(initial_state, particle_chamber_size))
        for state_vector in self.run_simulation(initial_state, particle_chamber_size):
            result.append(self.readout(state_vector, particle_chamber_size))
        return result



def main(args):
    speed = int(args['<speed>'])
    initial_state_string = args['<initial_state>']

    particle_animation = Animation()
    '''
    sv = particle_animation.particle_(speed, initial_state_string)
    print(sv)
    chamber_size = len(initial_state_string)
    print(particle_animation.readout(sv, chamber_size))
    sv = particle_animation.update(sv)
    print(particle_animation.readout(sv, chamber_size))
    sv = particle_animation.update(sv)
    print(particle_animation.readout(sv, chamber_size))
    sv = particle_animation.update(sv)
    print(particle_animation.readout(sv, chamber_size))

    print(particle_animation.particles_have_all_exited_chamber(sv, chamber_size))
    '''

    print('\n'.join(particle_animation.animate(speed, initial_state_string)))
    

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)
    