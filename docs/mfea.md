# Multifactorial Evolutionary Algorithm (MFEA)
This section summaries this paper [@gupta2015multifactorial]
## Multifactorial Optimization (MFO)
The purpose of MFO is not to find optimum trade-offs among the constitutive^[(adj) forming a part of something; components] objective functions. Rather, the goal is to fully and concurrently optimize each task, aided by the implicit parallelism of population-based search. 

Within the aforementioned scope, consider a situation wherein K optimization tasks are to be performed simultaneously. Without loss of generality, all tasks are assumed to be minimization problems. The $j^{th}$ task, denoted $T_j$, is considered to have a search space $X_j$ on which the objective function is defined as $f_j : X_j \rightarrow R$

MFO is the problem that aim of finding $\\{x_1, x_2, ...., x_{K-1}, x_K\\} = argmin {f_1(x), f_2(x), ...., f_{K-1}(x), f_K(x)}$. Herein, each $f_j$ is treated as an additional factor influencing the evolution of a single population of individuals. For this reason, the composite problem is referred to hereafter as a K-factorial problem.

Notations: 

* $P$: population, a set of properties for every individual $p_i$, where $i \in {1, 2, ..., |P|}$.
* $p_i$: an individual, encoded in a unified search space encompassing $X_1, ..., X_K$ and can be decoded into a task-specific solution representation with respect to each of the K optimization tasks.
* $\Psi^i_j$: *Factorial cost* (similar to fitness) of individual $p_i$ in task $T_j$. $\Psi_j^i = \lambda * \delta_j^i + f_j^i$ where $\lambda$ is a large penalizing multiplier, $f_j^i$ and $\delta^i_j$ are the objective value and the total constraint violation, respectively, of pi with respect to T.
* $r_j^i$: *Factorial rank* of $p_i$ on task $T_j$ the index of $p_i$ in the list of population members sorted in ascending order with respect to $\Psi_j^i$.
* $\varphi_i = 1 / min_{j\in1..K}\\{r_j^i\\}$: *Scalar fitness*, the best rank over all task of individual $p_i$.
* $\tau_i = argmin_j \\{r_j^i\\}$: *Skill factor* of individual $p_i$ is the one task, amongst all other tasks in MFO, on which the individual is most effective.

$p_a$ is considered to dominate $p_b$ ($p_a >> p_b$) in a multifactorial sense simply if $\varphi_a > \varphi_b$. If an individual $p_\*$ maps to the global optimum of any task, then, $\varphi^\* \geq \varphi_i$ for all $i \in \\{1, 2,..., |P|\\}$. Therefore, it can be said that the proposed technique is indeed consistent with the ensuing definition of multifactorial optimality. An individual $p_\*$, with a list of objective values ${f_1 , f_2 , ..., f_K }$, is considered optimum in multifactorial sense if $\exists j \in \\{1, 2, ..., K\\}$ such that $f_j^\* \leq f_j(x_j)$, for all feasible $x_j \in X_j$.

## Multifactorial Evolutionary Algorithm (MFEA)
The basic structure of the MFEA (most similar to GA's structure, the differents are on algorithm 2 and 3)

``` latex
#. Generate an initial population of individuals and store it in current-pop (P).
#. Evaluate every individual with respect to every optimization task in the multitasking environment.
#. Computetheskillfactor($\tau$)of each individual.
#. while (stopping conditions are not satisfied) do
- Apply genetic operators on current-pop to generate an offspring-pop (C). Refer to Algorithm 2.
- Evaluate the individuals in offspring-pop for selected optimization tasks only (see Algorithm 3).
- Concatenate offspring-pop and current-pop to form an intermediate-pop $(P C)$.
- Update the scalar fitness ($\varphi$) and skill factor ($\tau$) of every individual in intermediate-pop.
- Select the fittest individuals from intermediate-pop to form the next current-pop (P).
#. end while
```

### Individual Encoding
* Assume that that in K optimization tasks to be performed simultaneously, and we encode the individuals by the dimensionality of the $j^{th}$ task is given by $D_j$. 

* Dimensionality of unified search space $D_{multitask} = max_{j=1...k} \\{D_j\\}$

* The $i_{th}$ dimension of the unified search space is represented by a random-key $y_i$, and the fixed range represents the box-constraint of the unified space. While addressing task $T_j$, we simply refer to the first $D_j$ random-keys of the chromosome.

**Summary**:

* assume that we encode the individuals by the dimensionality of the $j^{th}$ task is given by $D_j$. 
* the dimensionality of unified search space 
        \\[D_{m} = max_{j=1...k} \\{D_j\\}\\]
* Unified space represented by $Y = \{y \; | \; |y| = D_m \}$. 
    - $y = \\{y_1,...y_{D_m}\\}$ can understand as encoded chromosome(individual) in $Y$
    - $y_i \in \[0,1\]$ is called random-key (value).
* the first $D_j$ random-keys $\\{y_1,...y_{D_j}\\}$ is representation of individual $y$ in task $j^{th}$.

### Individual Decoding
Consider the ith variable ($x_i$) of the actual problem to be bounded within the range $\[L_i, U_i\]$. If the corresponding random-key of an individual takes a value $y_i$, then it's mapping into the search space of the actual problem is given by $x_i = L_i + (U_i - L_i)\times y_i$. In contrast, for the case of discrete optimization, the chromosome decoding scheme is usually problem dependent

**Summary**

Decoding $\\{y_1,...y_{D_j}\\}$ for task $T_j$:
* $x^{(j)} = \{x_1^{(j)},...x_{D_j}^{(j)}\} \in X_j$: is the representation of individual in actual space $X_j$ of the problem. 
* $x_i^{(j)} \in \[L_i^{(j)}, U_i^{(j)}\]$ is domain of $x_i^{(j)}$.
* For continuous problem: 
    \\[\rightarrow x_i = L_i + (U_i - L_i)\times y_i \\]
* For discrete problem: depend on each problem.

### Population initialization
* Dimensionality of unified search space $D_{multitask} = max_{j=1...k} \\{D_j\\}$. Reasons:
    - circumvent the curse of dimensionality.
    - discovery and implicit transfer of useful genetic material from one task to another in an efficient manner. A single individual in the population may inherit genetic building blocks corresponding to multiple optimization tasks.

### Genetic mechanisms (Assortative mating)
A key feature of the MFEA is that certain conditions must be satisfied for two randomly selected parent candidates to undergo crossover. The principle followed is that of nonrandom or assortative^[denoting or involving the preferential mating of animals or marring of people with similar] mating  which states that individuals prefer to mate with those belonging to the same cultural background. In the MFEA, the skill factor ($\tau$) is viewed as a computational representation of an individual’s cultural bias.

**Algorithm 2: Assortative mating**

``` latex
    Consider two parent candidates pa and pb randomly selected from current-pop.
    1. Generate a random number rand between 0 and 1.
    2. if ($\Tau_b$ == $\Tau_b$) or (rand < rmp) then
    i. Parents pa and pb crossover to give two offspring individuals ca and cb.
    3. else
    i. Parent p_a is mutated slightly to give an offspring ca.
    ii. Parent p_b is mutated slightly to give an offspring cb. 4. end if
```

The term ```($\Tau_b$ == $\Tau_b$) or (rand < rmp)``` conversely means if their skill factors differ, crossover only occurs as per a prescribed random mating probability (```rmp```), or else mutation kicks in. the parameter ```rmp``` is used to balance exploitation and exploration of the search space.

Finally, while choosing crossover and mutation operators, it must be kept in mind that the random-keys presented earlier are always interpreted as continuous variables, even if the underlying optimization problem is discrete. This encourages the use of existing real-coded genetic operators, or the design of new operators for improved navigation of the composite landscapes associated with MFO.

### Selective evaluation
A question is posed when reviewing the general structure of MFEA.\\\\
**Question**: Why offsprings are evaluated for only one task? \\\\
Evaluating every individual for every problem being solved will often be computationally too expensive, and is therefore undesirable. An important observation we have made is that an individual generated in the MFEA is unlikely to be high performing across all tasks.

The algorithm 3, which is named as *selective imitating*, said that the offspring is evaluated only for one task. If the offspring is inherited from two parents then randomly choosing the parent which the offspring imitate to.

**Another question**: Why do not evaluate offspring at both parents' tasks? 

**Algorithm 3: Selective imitating**

```latex
An offspring ‘c’ will either have two parents (pa and pb) or a single parent (pa or pb) - see Algorithm 2.
1.
if (‘c’ has 2 parents) then
i. Generate a random number rand between 0 and 1.
ii. if (rand < 0.5) then
‘c’ imitates pa $\rightarrow$ The offspring is evaluated only for task $\tau_a$ (the skill factor of p_a).
iii. else
‘c’ imitates pb $\rightarrow$ The offspring is evaluated only for task $\tau_b$ (the skill factor of p_b).
iv. end if 2. else
i. ‘c’ imitates its single parent $\rightarrow$ The offspring is evaluated only for that task which is its parent’s skill factor.
3. end if
4. Factorial costs of ‘c’ with respect to all unevaluated tasks are
artificially set to infinity (a very large number).
```

### Selection Operation
The MFEA follows an elitist strategy which ensures that the best individuals survive through the generations.

### The salient features of MFEA
An important question in the whole paper is "Why multifactorial optimization is effective? and Why should we use MFEA?". The author does not specify the theoretical evidence that shows the efficiency of MFEA. The author repeatedly uses "implicit" and "salient" to describe the strongness of MFEA. The author demonstrates by numerical experiments instead.

*"Standard EAs typically generate a large population of candidate solutions, all of which are unlikely to be competent for the task at hand. In contrast, in a multitasking environment, it is intuitively more probable that a randomly generated or genetically modified individual is competent for at least one task. The mechanism of the MFEA builds on this observation by effectively splitting the population into different skill groups, each excelling at a different task. More interestingly and important, the genetic material created within a particular group may turn out to be useful for another task as well. Thus, in such situations, the scope for genetic transfer across tasks can potentially lead to the discovery of otherwise hard to find global optima"*

