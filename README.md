# Artificial Intelligence Projects – Berkeley Pacman & Constraint Satisfaction

A collection of academic projects developed as part of an Artificial Intelligence course, exploring fundamental AI concepts, problem-solving techniques, search algorithms, adversarial decision-making, and Constraint Satisfaction Problems (CSPs).

The repository includes implementations based on the UC Berkeley Pacman AI projects, alongside a solver for the Radio Link Frequency Assignment Problem (RLFA).

## Project Overview

The repository is organized into three main areas:

### 1. Search Algorithms – Pacman

Implementation of classical search algorithms to solve pathfinding and navigation problems in the Pacman environment.

**Implemented algorithms and techniques:**
- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- Uniform Cost Search (UCS)
- A* Search
- Heuristic-based search

**Pacman search problems:**
- Position Search: Finding paths between positions in a maze.
- Corners Problem: Finding a path that visits all four corners of a maze.
- Food Search Problem: Finding a path that collects all remaining food.

The project also explores heuristic design, including Manhattan and Euclidean distance, to guide the search process.

### 2. Multi-Agent Search – Adversarial Decision-Making

Implementation of AI agents that make decisions in a competitive environment, where Pacman interacts with multiple ghost agents.

**Implemented agents and algorithms:**
- Reflex Agent: Selects actions using a state evaluation function.
- Minimax Agent: Applies adversarial search to select actions against competing agents.
- Alpha-Beta Pruning: Optimizes Minimax by pruning branches that cannot influence the final decision.
- Expectimax Agent: Models opponents as agents making random decisions.
- Better Evaluation Function: Evaluates game states using factors such as remaining food, ghost positions, and game score.

These implementations explore game-tree search, adversarial reasoning, decision-making, and state evaluation.

### 3. Radio Link Frequency Assignment Problem (RLFA)

Implementation of a Constraint Satisfaction Problem (CSP) solver for the Radio Link Frequency Assignment Problem.

The objective is to assign frequencies to radio links while satisfying constraints between variables.

Each problem instance is represented through three input files:
- `var`: Defines the variables and their associated domains.
- `dom`: Defines the available values for each domain.
- `ctr`: Defines the constraints between variables.

The constraints are expressed in the form:

- `|x - y| > k`
- `|x - y| = k`

**Implemented algorithms and techniques:**
- Backtracking Search
- Forward Checking (FC)
- Maintaining Arc Consistency (MAC)
- AC-3 Constraint Propagation
- Conflict-Directed Backjumping (CBJ)
- Min-Conflicts
- Minimum Remaining Values (MRV)
- Domain-over-Weighted-Degree (dom/wdeg) variable selection

The solver also implements weighted constraint handling and conflict tracking to improve the search process.

**Performance evaluation:**

The implementation records and compares:
- Number of variable assignments.
- Number of constraint checks.
- Execution time.

Multiple RLFA problem instances of different sizes are included for experimentation.

## Technologies & Concepts

**Programming Language**
- Python

**Core AI Concepts**
- Uninformed and Informed Search
- Heuristic Search
- A* Search
- Adversarial Search
- Game Theory and Decision-Making
- Constraint Satisfaction Problems (CSP)
- Constraint Propagation
- Arc Consistency
- Backtracking and Conflict-Directed Backjumping
- Local Search and Optimization

## Repository Structure

```text
Berkeley-AI-Pacman/
│
├── search/
│   ├── search.py
│   ├── searchAgents.py
│   ├── pacman.py
│   ├── layouts/
│   └── test_cases/
│
├── multiagent/
│   ├── multiAgents.py
│   ├── pacman.py
│   ├── ghostAgents.py
│   ├── layouts/
│   └── test_cases/
│
├── RLFA/
│   ├── csp.py
│   ├── main.py
│   ├── rlfa.py
│   ├── search.py
│   ├── utils.py
│   └── rlfap/
│       ├── var*.txt
│       ├── dom*.txt
│       └── ctr*.txt
│
├── theoritical/
│   ├── ex1/
│   ├── ex2/
│   ├── ex3/
│   └── ex4/
│
├── tutorial/
│
└── README.md
```

## Getting Started

### Prerequisites

- Python
- NumPy (required by the RLFA implementation)

### Running the Pacman Search Project

Navigate to the search directory:

```bash
cd search
```

Run Pacman with a search agent using A*:

```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=aStarSearch
```

You can also experiment with other search algorithms, such as DFS and BFS, by changing the search function.

### Running the Multi-Agent Project

Navigate to the multiagent directory:

```bash
cd multiagent
```

Run Pacman using the Minimax agent:

```bash
python pacman.py -p MinimaxAgent -a depth=2
```

Other available agents include:

```bash
python pacman.py -p AlphaBetaAgent -a depth=2
```

```bash
python pacman.py -p ExpectimaxAgent -a depth=2
```

### Running the RLFA Solver

Navigate to the RLFA directory:

```bash
cd RLFA
```

Before running the solver, update the dataset directory path in `main.py` to match the local location of the `rlfap` folder.

Execute:

```bash
python main.py
```

The program displays the available problem instances and prompts the user to select an instance and an algorithm.

Available algorithm options:

```text
fc
mac
fc-cbj
min_conflicts
```

The solver displays the resulting assignment (when available), the number of assignments, constraint checks, and execution time.

## Learning Outcomes

Through these projects, I gained practical experience in:

- Designing and implementing classical AI algorithms in Python.
- Understanding the differences between uninformed and informed search strategies.
- Developing heuristic functions for efficient problem-solving.
- Implementing adversarial search algorithms for multi-agent environments.
- Applying constraint satisfaction techniques to complex assignment problems.
- Improving search efficiency through constraint propagation, variable ordering, and backjumping.
- Evaluating algorithm performance using execution time and computational metrics.

## Acknowledgements

The Pacman search and multi-agent frameworks are based on the educational AI projects developed by [UC Berkeley](http://ai.berkeley.edu/).

The original Berkeley attribution and licensing notices are retained in the relevant source files.
