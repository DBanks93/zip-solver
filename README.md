# Zip Solver
A program that can solve LinkedIn Zip program.

This isn't meant to be the fastest possible (Otherwise I'd use C, or rust),
I'm doing this to keep my Python skills up to scratch.

## Algorithm 
The 'solver' is essentally a fancy DFS (or if DFS and A* had a child...)

Each neighbouring node is given a score and the algorithm traverses the node with the best score.

The board it's a [Hamiltonian path](https://en.wikipedia.org/wiki/Hamiltonian_path)