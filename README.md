# Game of Fifteen AI
Game of Fifteen using Pygame + AI.

The implementation of the solver is done in C++, since solving a 4x4 Puzzle is computationally expensive.

## How did I solve it?
Using bidirectional search with heuristics.

Heuristic: sum of Manhattan distances between tile positions and goal positions.

I also hashed the board into a 64-bit unsigned int.

Although this method is much faster than A star, it does (not) guarantee shortest path, unlike A star.

## Performance:
Average time = <b>0.6s</b> over 1000 random solvable 4x4 boards.

## Requirements:
- Python 3.x.
- Pygame: 
    ```
    pip install pygame
    ```
- g++ or msvc.

## Instructions:
1. Clone the repository:
    ```bash
    $ git clone https://github.com/abdulrahman-aj/Game-of-Fifteen-AI
    ``` 
2. cd into repo directory:
    ```bash
    $ cd Game-of-Fifteen-AI
    ```
3. Create Python C++ extension: 
    ```bash
    $ python scripts/setup.py
    ```
4. Run the game:
    ```bash
    $ python main.py
    ```
