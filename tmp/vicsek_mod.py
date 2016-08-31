################################################################################
#                                                                              #
# Copyright (c) 2014 Romain Mueller                                            #
#                                                                              #
# Distributed under the GNU GPL v2. For full terms see the file LICENSE.       #
#                                                                              #
################################################################################

import copy, random, time, datetime
from math import pi, cos, sin, atan2, fabs, floor, ceil, sqrt

# distance
def dist(p1, p2):
  return sqrt(fabs(p1[0]-p2[0])**2 + fabs(p1[1]-p2[1])**2)

def sign(v):
  return v/abs(v)

class bucket_grid:
  """Fixed radius nearest neighbour search using a grid of buckets of size r.
     Width and height are needed to wrap around (periodic boundary conditions).
    """
  def __init__(self, points, param):
    self.param = param
    n = self.param.width / self.param.r # # of horizontal buckets
    m = self.param.height / self.param.r # # of vertical buckets 
    self.buckets = {} # dictionary of buckets -> points

    # create dictionary for given points
    for p in points:
      self.buckets.setdefault(self.get_index(p), []).append(p)
 
  def get_index(self, p):
    # returns bucket coordinates of point
    return ( int(floor(p[0]/self.param.width*n)),
             int(floor(p[1]/self.param.height*m)) )

  def neighbours(self, p):
    # position of the central bucket
    i, j = self.get_index(p)
    # this is the number of adjacent buckets we need to check
    cx = int(ceil(float(self.param.r)/self.param.width*n))
    cy = int(ceil(float(self.param.r)/self.param.height*m))
    neighbours = []
    # check all neighbouring buckets
    for a in range(-cx, 1+cx):
      for b in range(-cy, 1+cy):
        # add points
        neighbours += filter(
          lambda q: dist(p, q) < r,
          self.buckets.setdefault( ( (i+a)%n, (j+b)%m ), [])
          )
    return neighbours

class bird:
  """
  Flies.  
  """
  def __init__(self, param, pos, phi):
    self.pos  = pos
    self.phi   = phi
    self.size  = 7
    self.param = param

  def __getitem__(self, index):
    """
    Return position
    """
    return self.pos[index]

  def move(self):
    # 
    self.pos = map(sum, zip(self.pos, [ self.param.speed*cos(self.phi),
                                        self.param.speed*sin(self.phi) ]))
    # implement bc with mod=%
    self.pos = [ self.pos[0]%self.param.width,
                 self.pos[1]%self.param.height ] 

class flock:
  """
  Many of those things together.
  """
  # define a class param with all parameters
  def __init__(self, param):
    self.param = param
    # create birds
    self.birds = [ bird(param, # can change to param?
                        [ random.random()*param.width, random.random()*param.height ], 
                        2*pi*random.random(), 
                        param.speed
                       ) for i in range(param.N) ]

  def set_temp(self):
    # is this necessary after init again?
    for b in self.birds:
      b.n = n

  def move(self):
    # create the buckets
    grid = bucket_grid(self.birds, self.param.width,
      self.param.height, self.param.width/self.param.r,
      self.param.height/self.param.r)
    # update the angles
    for b in self.birds:
      sin_tot = 0.
      cos_tot = 0.
      counter = 0
      # loop over neighbours
      neighbours = grid.neighbours(b, self.param.r)
      for n in neighbours:
          sin_tot += sin(n.phi)
          cos_tot += cos(n.phi)
      counter = len(neighbours)
      # update
      b.phi = atan2(sin_tot, cos_tot) + self.param.n/2.*(1-2.*random.random())

    # move them
    for b in self.birds:
      b.move()

class param:
  """
  Parameters of the 
  """
  def __init__(self, width = 512, height = 512, N = 250, r = 10,
    n = 0.5, speed = 10):
    self.width = width
    self.height = height
    self.N = N
    self.r = r
    self.n = n # this can be removed, and teime parameters added.
    self.speed = speed