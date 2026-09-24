from dataclasses import dataclass, field


@dataclass(frozen=True)
class Wall:
    node_a: tuple[int, int]
    node_b: tuple[int, int]

    def __post_init__(self):
        # Canonicalize the two positions
        # makes my life easier when checking walls :)
        a, b = sorted((self.node_a, self.node_b))
        object.__setattr__(self, "node_a", a)
        object.__setattr__(self, "node_b", b)


@dataclass
class Puzzle:
    width: int
    height: int
    checkpoints: dict[int, int]
    walls: set[Wall] = field(default_factory=set)

    @property
    def size(self) -> int:
        return self.width * self.height

    @property
    def starting_cell(self) -> int:
        for cell, number in self.checkpoints.items():
            if number == 1:
                return cell
        raise ValueError("No checkpoint numbered 1 found in puzzle")
