# Introduction
Simulation of the vicsek model. The goal is to learn good coding practices, such as how to use git, github, and create a proper program structure.

For example, we will learn how to upload changes, and how to download changes (made by someone else, myself from another computer, or on the web).

# Vicsek's model
In the Vicsek model birds, or boids, align with the average flying direction of the neighbors in a range $r$. Birds move at a constant speed $v$ and are subject to rotational diffusion, characterized by the noise term $\eta$. This noise is assumed, for simplicity, to be completely uncorrelated in time and space: <\eta(\vec{r},t)\eta(\vec{r}',t')>=\delta

# Algorithm
Calculating near neighbors of moving birds is in principle a slow process, as we have to check all possible pairs. A naive search thus scales as $N^2$. To avoid this here we break the simlulation space in squares of size $r$ and keep track of the birds in each box. The neighbors are only calculated for neighboring boxes, which makes the process scale as $\sim N$.

# Running 
To run a simulation we have to choose a parameter set, create a flock, and then run the simulation. For example:

```python
import vicsek as mivic
bandada = mivic.flock(parametros)
vic_simu =mivic.simulate(bandada)
vic_simu.run()
```

Alternatively we could have done
```python
mivic.simulate(bandada).run()
```

