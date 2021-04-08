# Game of Fifteen AI
Game of Fifteen + AI solver.

Solver implementation is done in C++, since solving a 4x4 Puzzle is computationally expensive.

## Method I used to solve:
Bidirectional A*.

Heuristic: sum of Manhattan distances.

Nodes (board states) in the search are hashed into a uint64.

Although this method is quite faster than normal A*, it does (not) guarantee optimal solution, unlike A*.

<img src="https://i.imgur.com/rV7Kc8N.gif" alt="game demo">

## Performance:
<b>0.6s</b> avg over 1000 random solvable 4x4 boards.

## Requirements:
- python 3.x.
- gcc / clang / msvc.

## Instructions:
1. clone the repo:
    ```bash
    git clone https://github.com/abdulrahman-aj/Game-of-Fifteen-AI
    ``` 
2. cd into the repo directory:
    ```bash
    cd Game-of-Fifteen-AI
    ```

3. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

4. Create Python C++ extension: 

    using make:
    ```bash
    make
    ```
    
    or manually
    ```bash
    python scripts/setup.py
    ```

5. Run:
    ```bash
    python main.py
    ```
