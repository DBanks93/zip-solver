
from algorithm.puzzle import Puzzle, Wall


def check_wall(puzzle: Puzzle, pos_1: tuple[int, int], pos_2: tuple[int, int]) -> bool:
    """Checks if there's a wall between two cells."""
    return Wall(pos_1, pos_2) in puzzle.walls


def build_graph(puzzle: Puzzle) -> dict[int, list[int]]:
    """Builds an adjency list to represent the puzzle as graph."""
    graph: dict[int, list[int]] = {}

    for cell in range(puzzle.size):
        x = cell % puzzle.width
        y = cell // puzzle.width
        neighbours = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < puzzle.width and 0 <= ny < puzzle.height:
                neighbour = ny * puzzle.width + nx

                if not check_wall(puzzle, (x, y), (nx, ny)):
                    neighbours.append(neighbour)
        graph[cell] = neighbours
    return graph


# def solve():
