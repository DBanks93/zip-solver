from algorithm.graph import build_graph
from algorithm.puzzle import Puzzle

STARTING_CHECKPOINT = 1


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

    def _all_checkpoints_visited(self) -> bool:
        return self.next_checkpoint > len(self.puzzle.checkpoints)

    def _is_solved(self) -> bool:
        return self._all_checkpoints_visited() and len(self.path) == self.puzzle.size

    def _backtrack(self, cell) -> None:
        self.visited.remove(cell)
        self.path.pop()

        if cell in self.puzzle.checkpoints:
            checkpoint = self.puzzle.checkpoints[cell]

            if checkpoint < self.next_checkpoint:
                self.next_checkpoint -= 1

    def _get_valid_neighbours(self, current_cell: int) -> list[int]:
        return [
            n
            for n in self.puzzle_graph[current_cell]
            if n not in self.visited
            and (
                n not in self.puzzle.checkpoints
                or self.puzzle.checkpoints[n] == self.next_checkpoint
            )
        ]

    def _would_create_deadend(self, entering_cell: int) -> bool:
        for neighbour in self.puzzle_graph[entering_cell]:
            if neighbour in self.visited:
                continue
            remaining_exits = sum(
                1
                for nn in self.puzzle_graph[neighbour]
                if nn not in self.visited and nn != entering_cell
            )
            if remaining_exits == 0 and len(self.path) + 2 != self.puzzle.size:
                return True
        return False

    def _order_neighbours(self, neighbours: list[int]) -> tuple[list[int], bool]:
        """Single pass: drops deadend candidates, detects a forced move or a
        contradiction, and orders the rest by remaining degree (Warnsdorff).

        Returns (ordered_candidates, is_contradiction).
        """
        scored = []
        forced = []

        for n in neighbours:
            if self._would_create_deadend(n):
                continue

            degree = sum(1 for nn in self.puzzle_graph[n] if nn not in self.visited)
            scored.append((degree, n))
            if degree <= 1:
                forced.append(n)

        if len(forced) > 1:
            return [], True
        if len(forced) == 1:
            return forced, False

        scored.sort(key=lambda pair: pair[0])
        return [n for _, n in scored], False

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
                else:
                    self._backtrack(cell)
                    return False

            if self._is_solved():
                return True

            neighbours = self._get_valid_neighbours(cell)
            ordered, contradiction = self._order_neighbours(neighbours)

            if contradiction:
                self._backtrack(cell)
                return False

            for neighbour in ordered:
                if dfs(neighbour):
                    return True

            self._backtrack(cell)
            return False

        self._visit_starting_cell()

        for neighbour in self.puzzle_graph[self.puzzle.starting_cell]:
            if dfs(neighbour):
                return self.path

        return None
