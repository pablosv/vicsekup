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
  def __init__(self, points, width, height, n, m):
    self.width = width
    self.height = height
    self.n = n
    self.m = m
    # here are your buckets (dict)
    self.buckets = {}
    # put all points into them
    for p in points:
      self.buckets.setdefault(self.get_index(p), []).append(p)

  def get_index(self, p):
    return ( int(floor(p[0]/self.width*self.n)), int(floor(p[1]/self.height*self.m)) )

  def neighbours(self, p, r):
    # position of the central bucket
    i, j = self.get_index(p)
    # this is the number of adjacent buckets we need to check
    cx = int(ceil(float(r)/self.width*self.n))
    cy = int(ceil(float(r)/self.height*self.m))
    neighbours = []
    # check all neighbouring buckets
    for a in range(-cx, 1+cx):
      for b in range(-cy, 1+cy):
        # add points
        neighbours += filter(
          lambda q: dist(p, q) < r,
          self.buckets.setdefault( ( (i+a)%self.n, (j+b)%self.m ), [])
          )
    return neighbours

class bird:
  """
  Flies.  
  """
  def __init__(self, app, pos, phi, speed):
    self.pos  = pos
    self.tail  = [ copy.deepcopy(self.pos) ]
    self.phi   = phi
    self.speed = speed
    self.size  = 7
    self.app = app

  def __getitem__(self, index):
    """
    Return position
    """
    return self.pos[index]

  def move(self):
    self.pos = map(sum, zip(self.pos, [ self.speed*cos(self.phi), self.speed*sin(self.phi) ]))
    # periodic boundary conditions
    self.pos = [ self.pos[0]%app.width, self.pos[1]%app.height ] 

class flock:
  """
  Many of those things together.
  """
  def __init__(self, app, N, r, n, speed):
    self.N = N
    self.r = r
    self.n = n
    self.app = app
    self.speed = speed
    # create birds
    self.birds = [ bird(self.app, 
                        [ random.random()*app.width, random.random()*app.height ], 
                        2*pi*random.random(), 
                        self.speed
                       ) for i in range(self.N) ]

  def set_temp(self, n):
    self.n = n
    for b in self.birds:
      b.n = n

  def move(self):
    # create the buckets
    grid = bucket_grid(self.birds, self.app.width, self.app.height, self.app.width/self.r, self.app.height/self.r)
    # update the angles
    for b in self.birds:
      sin_tot = 0.
      cos_tot = 0.
      counter = 0
      # loop over neighbours
      neighbours = grid.neighbours(b, self.r)
      for n in neighbours:
          sin_tot += sin(n.phi)
          cos_tot += cos(n.phi)
      counter = len(neighbours)
      # update
      b.phi = atan2(sin_tot, cos_tot) + self.n/2.*(1-2.*random.random())

    # move them
    for b in self.birds:
      b.move()

class game:
  """
  Fly, baby, fly.
  """
  def __init__(self):
    self.width, self.height = 512, 512
    self.N = 250
    self.r = 10
    self.n = 0.5
    self.v = 3.
    self.fps = 30

    self.flock = flock(self, self.N, self.r, self.n, self.v)

  def run(self):
    running = True

    while running:
      # moving
      self.flock.move()

def test_bucket():
  """
  Small test function of the bucket grid
  """
  import matplotlib.pyplot as plt
  points = [ ( random.random()*512, random.random()*512 ) for i in range(400) ]
  bnn = bucket_grid(points, 512, 512, 10, 10)
  neighbours = bnn.neighbours(points[0], 10)

  print points[0]
  print neighbours

if __name__ == "__main__":
  #http://stackoverflow.com/questions/419163/what-does-if-name-main-do
  app = game() 
  app.run()