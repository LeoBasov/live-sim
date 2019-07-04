# Natural Selection Simulation

## Base Idea
This is a tool which tries to mimic natural selection.
The simulation contains of creatures which each have a set of traits.
Those traits influce three things:

* enegry input (rate)
* energy consumption rate
* reproduction rate
* the death rate is controlled implicitly

The criature can interact with each other and the envorinment.

## Creatures
Creatures live on a 2D map.
Each creater has at least the following members:

* Position (Position of creature on the map)
* Live status (Indicates if the creature is dead or alive)
* Energy
* Speed

Each creature has this member functions:

* update (do things)

## World
Is construted as a ungridded 2D map.
A grid can be overlayd.
Has position dependant properties.
Terrain hight can be added.
Has information about time of day / weather / daylight...

The world basically serves as the state of the simulation.
Everything lives inside of the world.

## Loop
Day night cycle.
Maybe season cycle later.
Runs with time steps. (Standard time step = 1h)
Update every time step.

## Engine
PyGame seems like a reasonable choice.
