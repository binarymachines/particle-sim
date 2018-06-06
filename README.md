# particle-sim
A simulated particle animation code challenge in python

## Prerequisites

particle-sim is written in Python 3.5 and uses pipenv to manage dependencies -- of which there is only one: docopt, which is the One True Way to parse command line args in Python. (There are some who disagree, but it is important to note that they are wrong.)

## Running it

issue `pipenv install` to install the dependencies; then either run  `pipenv shell` to enter the virtual environment, or issue `pipenv run python particlesim.py`. Issue `make test` to run the tests.

## Notes
Possible optimizations: the animate() method compiles an in-memory array, but invokes an underlying generator, so we could ease our memory restrictions by making it a straight callthrough. A possible evolution is the use of very "long" particle chambers, which would 
start to be a problem in terms of calculating particle counts and such. Using bitmaps and bitshift / bitwise AND operations, as opposed to arrays of first-class objects, might be one way to get around this problem. If we were to stay with a first-class object strategy, we could optimize by introducing a bit of local state in the form of a Chamber type that wraps the particle state vector. On each update the chamber would update its own internal count of resident vs. exited particles, removing the need for a linear search of all particles in the breakout logic. 