# geneticpython

A simple and friendly Python framework for genetic-based algorithms (strongly supports tree-encoding)

* Supported algorithms: Genetic Algorithm (`GAEngine`), NSGA-ii (`NSGAIIEngine`).
* An [example](https://github.com/ngocjr7/geneticpython/tree/master/examples) on ZDT1 problem:    

![alt tag](https://raw.githubusercontent.com/ngocjr7/geneticpython/master/examples/zdt1/solutions.gif)

## Installation

This package requires `python 3.6` or later.
```
pip install geneticpython
```

## Getting started

We can quickly design a genetic algorithm in the following steps:

1. define a template individual with specific encoding

```python
from geneticpython.models import BinaryIndividual
indv_temp = BinaryIndividual(length=100)
```

2. define population based on this population can uniformly initialize a population or you can define your own by passing `init_population` argument function

```python
from geneticpython import Population
population = Population(indv_temp, pop_size=100)
```
3. define some core operators in genetic algorithm

```python
from geneticpython.core.operators import RouletteWheelSelection, UniformCrossover, \
                                        FlipBitMutation, RouletteWheelReplacement
selection = RouletteWheelSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitMutation(pm=0.1)
# this function decides which individuals will be survived
replacement = RouletteWheelReplacement()
```

4. create an engine and register the defined population and operators

```python
from geneticpython import GAEngine
engine = GAEngine(population, selection=selection,
                  selection_size=100,
                  crossover=crossover,
                  mutation=mutation,
                  replacement=replacement)
```

5. register fitness function which gets an individual and returns its fitness value

```python
@engine.maximize_objective
def fitness(indv):
    return fitness_of_indv
```

6. run engine

```python
engine.create_seed(seed)
history = engine.run(generations=1000)
```

7. get results and plot history

```python
ans = engine.get_best_indv()
print(ans)
plot_single_objective_history({'geneticpython': history})
```

You can find more examples [here](https://github.com/ngocjr7/geneticpython/tree/master/examples)

## TODO
- [] Create extensive documentation and docs and comments in source-code
- [] Implement other algorithms: `PSO, DE, MOED/A, MOPSO, MODE,...`
- [] Implement other operators: `PMX crossover, ...`

## Issues and Contribution
This project is in development, if you find any issues, please create an issue [here](https://github.com/ngocjr7/geneticpython/issues).

If you are interested in contributing this project, feel free to create pull request [here](https://github.com/ngocjr7/geneticpython/pulls). We appreciate any contributions from you.

## Acknowledgements
Special thanks to https://github.com/PytLab/gaft for getting me started a great API design.

This repository includes adaptions of the following repositories as baselines:

* https://github.com/msu-coinlab/pymoo
* https://github.com/tensorflow/tensorflow
