from algorithm.graph import result_to_string
from algorithm.puzzle import Puzzle
from algorithm.search import Search

print("Hello World!")

checkpoints = {
    0: 1,
    35: 2,
    25: 3,
    13: 4,
    22: 5,
    20: 6,
    10: 7,
    15: 8,
}

walls = {}

puzzle = Puzzle(
    width=6,
    height=6,
    checkpoints=checkpoints,
)

search = Search(puzzle)
result = search.find_path()
print(search.puzzle_graph)
print(result)
print(result_to_string(puzzle, result))
