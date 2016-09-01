import random
import numpy as np
from math import atan2, fabs, floor, ceil, sqrt

# USE ONLY NUMPY IF POSSIBLE

# distance
def dist(p1, p2):
  return sqrt(fabs(p1[0]-p2[0])**2 + fabs(p1[1]-p2[1])**2)

class bucket_grid:
  """
  Fixed radius nearest neighbour search using a grid of buckets of size r.
  Width and height are needed to wrap around (periodic boundary conditions).
  """
  def __init__(self, birds, param):
    self.param = param
    self.n = self.param.width / self.param.r # number of horizontal buckets
    self.m = self.param.height / self.param.r # number of vertical buckets 
    self.buckets = {} # dictionary of buckets -> points

    # create dictionary for given points
    for b in birds:
      self.buckets.setdefault(self.get_index(b), []).append(b)
 
  def get_index(self, b):
    # returns bucket coordinates of point
    return ( int(floor(b[0]/self.param.width*self.n)),
             int(floor(b[1]/self.param.height*self.m)) )

  def neighbours(self, b):
    # position of the central bucket
    i, j = self.get_index(b)
    # this is the number of adjacent buckets we need to check
    cx = int(ceil(float(self.param.r)/self.param.width*self.n))
    cy = int(ceil(float(self.param.r)/self.param.height*self.m))
    neighbours = []
    # check all neighbouring buckets
    for f in range(-cx, 1+cx):
      for g in range(-cy, 1+cy):
        # add points
        neighbours += filter(
          lambda q: dist(b, q) < self.param.r,
          self.buckets.setdefault( ( (i+f)%self.n, (j+g)%self.m ), [])
          )
    return np.array(neighbours) # is there a numpy way of doing this above?

class flock:
  """
  Many of those things together.
  """
  # define a class param with all parameters
  def __init__(self, param):
    self.param = param

    # array for birds xy-position and angle
    self.birds     = np.array([self.param.width,
                               self.param.height,
                               2*np.pi]) * np.random.random((self.param.N,3))
    self.birds_old = self.birds 

  def move(self):
    # create the buckets
    grid = bucket_grid(self.birds_old, self.param)

    # update the angles
    for k in range(self.param.N):
      sin_tot = 0.
      cos_tot = 0.
      # loop over neighbours
      neighbours = grid.neighbours(self.birds_old[k]) 
      for n in neighbours: # REMOVE THIS LOOP, ACT ON ARRAY INSTEAD
          sin_tot += np.sin(n[2])
          cos_tot += np.cos(n[2])
      # update angle // WHY CAN'T PUT LINEJUMP AFTER +
      self.birds[k,2] = atan2(sin_tot, cos_tot) + self.param.n/2.*(1-2.*np.random.rand())
      # update position
      self.birds[k,0:2] = np.array([ self.param.speed*np.cos(self.birds[k,2])%self.param.width,
                                     self.param.speed*np.sin(self.birds[k,2])%self.param.height ])
    # global update
    self.birds_old = self.birds

class param:
  """
  Parameters of the 
  """
  def __init__(self, width = 512, height = 512, N = 250, T=100, r = 10,
    n = 0.5, speed = 10, dt = 10):
    self.width = width # box width
    self.height = height # box height
    self.N = N # number of birds
    self.T = T # total time steps
    self.r = r # interaction radius
    self.n = n # noise strength
    self.speed = speed # linear speed of birds
    self.dt = dt # time interval for storage

class simulate:
  """
  Run the iterative loop
  """
  def __init__(self, param):
    self.param = param
    self.flock = flock(self.param)

  def run(self):
    for t in range(self.param.T):
      self.flock.move()
      if t==0: print('save initial flock with parameters')
      if t%self.param.dt==0: print('store flock positions and angles') #

class analysis:
  """
  Perform analysis of the simulation, for which we pass... stored flocks?
  """
  def __init__(self, flock):
    self.flock = flock

class plotter:
  """
  Make movie of the flock, also plot correlations and so on...
  """
  # def frame
  # def movie