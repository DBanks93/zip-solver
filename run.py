from algorithm.graph import build_graph
from algorithm.puzzle import Puzzle, Wall

print("Hello World!")

print(
    build_graph(
        Puzzle(
            width=4,
            height=4,
            checkpoints={},
            walls={Wall(node_a=(0, 0), node_b=(1, 0))},
        )
    )
)
