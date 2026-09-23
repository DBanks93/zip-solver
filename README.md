# Zip Solver
A program that can solve LinkedIn Zip program.

This isn't meant to be the fastest possible (Otherwise I'd use C, or rust),
I'm doing this to keep my Python skills up to scratch.

## Algorithm 
The 'solver' is essentally a fancy DFS.

The board it's a [Hamiltonian path](https://en.wikipedia.org/wiki/Hamiltonian_path),
to traverse it we can use a simple DFS and essntally brute force all possible routes.

The only difference is that for each neighbor it checks if it's not the next checkpoint,
or if the path doesn't use all the cells if so it will backtrack.

### Optimisation
There are some improvements to the DFS, the following checks are done before trying each neighbour: 
1. Gets only _'valid'_ neighbors i.e. neighbors that haven't been visited
2. Prunes neighbors if by going to the neighbor it causes a deadlock
3. Forces the search to go to a neighbor if that neighbor has only one unvisited neighbor
4. Orders neighbors based on the least 'moves' the path can take out of that neighbor