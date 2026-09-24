import argparse
from enum import Enum

from linkedin_solvers.zipsolver.solver import solve_zip


class PuzzleTypes(Enum):
    ZIP = "zip"

def parse_args():
    parser = argparse.ArgumentParser(
        description="Tool to complete LinkedIn puzzles"
    )

    parser.add_argument('puzzle', help="Puzzle to solve", type=PuzzleTypes, choices=list(PuzzleTypes))
    return parser.parse_args()

def main() -> None:
    puzzle_type = parse_args().puzzle

    match puzzle_type:
        case PuzzleTypes.ZIP:
            solve_zip()
        case _:
            raise argparse.ArgumentError()




if __name__ == "__main__":
    main()
