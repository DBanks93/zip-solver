from algorithm.graph import build_graph
from algorithm.puzzle import Puzzle

STARTING_CHECKPOINT = 1

# TODO: Add optimiastion such like weights and rejection
class Search:
    """A search class that implements a DFS search algorithm.

    Attributes:
        puzzle (Puzzle): The puzzle to search.
        puzzle_graph (dict[int, list[list[int]]]): The adjecent graph of the puzzle.
        next_checkpoint (int): The next checkpoint of the puzzle to visit.
        visited (set[int]): Set of all cells visited.
        path (list[int]): Path through the puzzle.

    Methods:
        find_path
    """

    def __init__(self, puzzle: Puzzle) -> None:
        self.puzzle = puzzle
        self.puzzle_graph: dict[int, list[int]] = build_graph(puzzle)
        self.next_checkpoint = STARTING_CHECKPOINT
        self.visited: set[int] = set()
        self.path: list[int] = []

    def _visit_starting_cell(self) -> None:
        self.visited.add(self.puzzle.starting_cell)
        self.path.append(self.puzzle.starting_cell)
        self.next_checkpoint += 1

    def _is_at_last_checkpoint(self) -> bool:
        return self.next_checkpoint > len(self.puzzle.checkpoints)

    def _backtrack(self, cell) -> None:
        self.visited.remove(cell)
        self.path.pop()

        if cell in self.puzzle.checkpoints:
            checkpoint = self.puzzle.checkpoints[cell]

            if checkpoint < self.next_checkpoint:
                self.next_checkpoint -= 1

    def find_path(self) -> list[int] | None:
        """Finds a path through the puzzle and connects all checkpoints.

        Returns:
            list[int] | None: Returns the path through the puzzle if path exists.

        """

        def dfs(cell: int) -> bool:
            """Completes a DFS recursively."""
            self.visited.add(cell)
            self.path.append(cell)

            if cell in self.puzzle.checkpoints:
                if self.puzzle.checkpoints[cell] == self.next_checkpoint:
                    self.next_checkpoint += 1
                    if self._is_at_last_checkpoint():
                        return True
                else:
                    self._backtrack(cell)
                    return False

            for neighbour in self.puzzle_graph[cell]:
                if neighbour not in self.visited and dfs(neighbour):
                    return True

            self._backtrack(cell)
            return False

        self._visit_starting_cell()

        for neighbour in self.puzzle_graph[self.puzzle.starting_cell]:
            if dfs(neighbour):
                return self.path

        return None
