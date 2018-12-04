# Modeling and Simulation of Social Systems Fall 2018 – Research Plan

> * Group Name: tea-tan
> * Group participants names: Nico Burger, Leo Fent, Pascal Lieberherr, Jérôme Landtwing
> * Project Title: Implementation of a Traffic Light System at the Tannenbar-Intersection
> * Programming language: Python

## General Introduction
The intersection between the Tannenstrasse and the Universitätsstrasse is something all ETH students are well familiar with. It is located in a traffic hotspot with pedestrians, cars and trams all use the road simultaneously. This leads to conflict especially at peak times. During lecture breaks, early in the morning and at noon, the students from the surrounding university building desire to cross the street at the same time. As a consequence congestion and traffic holdups can be observed. 
Since we encounter this phenomenon close to every day, our goal is to find out whether changes in pedestrian and traffic behaviour can optimise the flow of people and traffic. We intend to implement these changes by simulating the effect traffic lights would have on the system.

## The Model
Our model will focus on the flow of our different agents during the rush hours. We will split the agents into three different groups: pedestrians, cars and trams. All agents will strictly adhere to traffic laws and interact with each other correspondingly. This results in a hierarchical structure:
Trams are always allowed to move
Pedestrians are allowed to crosswalk except if a tram approaches
Cars stop for trams and pedestrians
We are interested in the advantages and disadvantages for the agents caused by different solutions. The goal is to find a solution that benefits all three groups equally. The success of a solution is measured by the average time a pedestrian or car has to wait due to congestion or interaction with other agents.
The Agents will be spawned outside the system boundaries and have a set destination from the get-go. Spawn points will correspond to real-life spawn points, namely exits of nearby buildings as well as streets. By varying the spawn density, we will have a good approximation of the real world but will still be able to keep our system relatively simple.

## Fundamental Questions
We pose three guiding questions for our idea:
How good is the current solution?
As described earlier, large traffic jams can be observed during peak times. Is this necessary for smooth pedestrian flow? What would change if pedestrians stopped once in a while to let cars pass?
Could the situation be improved by adding traffic lights? 
Traffic lights would force either the cars of the pedestrians to let the opposite party pass. How would that affect car waiting time? How much longer would pedestrians have to wait?
What would be the best possible solution for all agents?
Is there an ideal solution (e.g. using traffic lights only at peak times)? What would it look like?

## Expected Results
Using our model we will simulate different possible states of the situation.
The current solution is probably not satisfactory and we expect to be able to improve on it.
We expect that adding traffic lights will improve the traffic flow for cars without causing major disadvantages for pedestrians.
The optimal solution would minimize the combined travel time of our agents.
This might cause pedestrians having to be a bit more patient, while cars do not end up in a total traffic jam.

## References					
Helbing, D. and Schreckenberg, M. (1999). Cellular automata simulating experimental properties of traffic flow. Rapid Communications, 063-651X/99/59(3)/2505(4)	 	 Lämmer, S. and Helbing, D. (2008). Self-control of traffic lights and vehicle flows in urban road networks. J. Stat. Mech. P04019

Similar project: https://github.com/nuhro/Intersection-Problem


## Research Methods
Just like previous groups that simulated similar situations, we will implement cellular automata on our agents in order to create our model.
We will also neglect the varying velocities of our agents, therefore reducing their movements to a stop-and-go state. In order to compensate for this restriction, we might try to implement the Schreckenberg-model in a second step.

## Other
Tram Schedule: https://www.zvv.ch/zvv/de/home.html

# Reproducibility

