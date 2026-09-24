from zipsolver.algorithm.puzzle import Puzzle, Wall


def check_wall(puzzle: Puzzle, pos_1: tuple[int, int], pos_2: tuple[int, int]) -> bool:
    """Checks if there's a wall between two cells."""
    return Wall(pos_1, pos_2) in puzzle.walls


def build_graph(puzzle: Puzzle) -> dict[int, list[int]]:
    """Builds an adjacency list to represent the puzzle as a graph."""
    graph: dict[int, list[int]] = {}

    for cell in range(puzzle.size):
        row = cell // puzzle.width
        col = cell % puzzle.width
        neighbours = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (drow, dcol)

        for drow, dcol in directions:
            nrow = row + drow
            ncol = col + dcol
            if 0 <= nrow < puzzle.height and 0 <= ncol < puzzle.width:
                neighbour = nrow * puzzle.width + ncol

                if not check_wall(puzzle, (row, col), (nrow, ncol)):
                    neighbours.append(neighbour)
        graph[cell] = neighbours
    return graph


def result_to_string(puzzle: Puzzle, result: list[int]) -> str:
    """Converts the puzzle, and it's result into a more human-readable format."""
    grid = [[" " for _ in range(puzzle.width)] for _ in range(puzzle.height)]

    for cell in result:
        x = cell % puzzle.width
        y = cell // puzzle.width
        grid[y][x] = (
            str(puzzle.checkpoints[cell]) if cell in puzzle.checkpoints else "#"
        )

    return "\n".join([" ".join(row) for row in grid])
