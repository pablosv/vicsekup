# Introduction
Simulation of the vicsek model. The goal is to learn good coding practices, such as how to use git, github, and create a proper program structure. We will also compare how an object oriented method compares to a numpy array method.

For example, we will learn how to upload changes, and how to download changes (made by someone else, myself from another computer, or on the web).

# Vicsek's model
In the Vicsek model birds, or boids, align with the average flying direction of the neighbors in a range $r$. Birds move at a constant speed $v$ and are subject to rotational diffusion, characterized by the noise term $\eta$. This noise is assumed, for simplicity, to be completely uncorrelated in time and space: <\eta(\vec{r},t)\eta(\vec{r}',t')>=\delta. Here we consider intrinsic noise. That is, to calculate the new velocity the bird determines the mean orientation perfectly well, and then adds a perturbation intrinsic to its navegation (for the extrinsic noise case there is noise in the determination of the orientation).

# Algorithm
Calculating near neighbors of moving birds is in principle a slow process, as we have to check all possible pairs. A naive search thus scales as $N^2$. To avoid this here we break the simlulation space in squares of size $r$ and create a dictionary of the birds in each box. The neighbors are only calculated for neighboring boxes, which makes the process scale as $\sim N$. The price to pay is the need of a complex structure as the dictionary, as opposed to a simple NxN adjacency matrix.

# Running 
To run a simulation we have to choose a parameter set, create a  simulation, and  run it. For example, to try the array method:

```python
import vicsek_arr as vic
parametros = vic.param(T=3)
vic_simu   = vic.simulate(parametros)
vic_simu.run()
```

Alternatively we could have done:

```python
vic.simulate(parametros).run()
```

## Running several simulations
This structure makes it easy to run a series. For example, we can simulate a noise series with ten items by doing:

```python
noise_param=[ vic.param(n=1.-1./(1+t)) for t in range(10)]
[vic.simulate(noise_param[t]).run() for t in range(10)]
```

## Comparative timing
We can compare the speed of the array and object oriented methods in the following way:

```python
import vicsek_arr as vicarr
import vicsek_obj as vicobj
parametros = vicarr.param(T=10,dt=1,N=100)
time vicarr.simulate(parametros).run()
time vicobj.simulate(parametros).run()
```

Similarly, we can time different parts of the code, for example, how fast are the indeces retrieved when birds are objects?
```python
pajobj = vicobj.flock(parametros).birds
time vicobj.bucket_grid(pajobj,parametros).get_index(pajobj[0])
```
And similarly for arrays. Other processes to explore are, for example, the calculation of neighbours
```python
time vicobj.bucket_grid(pajobj,parametros).neighbours(pajobj[2])
```

