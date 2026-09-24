import math

from linkedin_solvers.zipsolver.algorithm.puzzle import Puzzle, Wall


def _get_board_data(cells) -> list[dict]:
    """Gets the raw per-cell board data."""
    board_data = cells.evaluate_all("""
        cells => {
            const WALL_CLASSES = [
                "cd9d9487",
                "_8dd2f5e9",
                "_6234152e",
                "_2637fcf2",
                "f0c1d351"
            ];

            return cells.map(cell => {
                const idx = Number(cell.dataset.cellIdx);
                const rect = cell.getBoundingClientRect();

                const walls = [];

                for (const child of cell.children) {


                    const isWallElement =
                        WALL_CLASSES.every(
                            cls => child.classList.contains(cls)
                        );

                    if (!isWallElement) {
                        continue;
                    }

                    const style =
                        getComputedStyle(child, "::after");

                    const childRect =
                        child.getBoundingClientRect();

                    const borders = {
                        top: parseFloat(style.borderTopWidth),
                        right: parseFloat(style.borderRightWidth),
                        bottom: parseFloat(style.borderBottomWidth),
                        left: parseFloat(style.borderLeftWidth),
                    };

                    for (const [direction, size] of Object.entries(borders)) {
                        if (size !== 12) {
                            continue;
                        }

                        walls.push({
                            direction,

                            cellX: rect.x,
                            cellY: rect.y,
                            cellWidth: rect.width,
                            cellHeight: rect.height,

                            x: childRect.x,
                            y: childRect.y,
                            width: childRect.width,
                            height: childRect.height,

                            top: style.top,
                            right: style.right,
                            bottom: style.bottom,
                            left: style.left,
                        });
                    }
                }

                return {
                    idx,
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height,
                    walls,
                };
            });
        }
        """)

    return board_data


def scrape_puzzle(page) -> tuple[Puzzle, list[dict]]:
    """Scrapes the current page for the puzzle grid, checkpoints and walls.

    Returns:
        tuple[Puzzle, list[dict]]: The parsed puzzle, plus the raw
        per-cell board data (needed later for drag coordinates).
    """

    cells = page.locator('[data-testid^="cell-"]')

    cells.first.wait_for(
        state="attached",
        timeout=10000,
    )

    cell_count = cells.count()

    puzzle_width = int(math.sqrt(cell_count))
    puzzle_height = cell_count // puzzle_width

    checkpoints: dict[int, int] = {}

    for i in range(cell_count):
        cell = cells.nth(i)

        label = cell.get_attribute("aria-label")

        if label and label.startswith("Number "):
            checkpoints[i] = int(label.removeprefix("Number "))

    board_data = _get_board_data(cells)

    first_cell = board_data[0]

    board_x = first_cell["x"]
    board_y = first_cell["y"]

    cell_width = first_cell["width"]
    cell_height = first_cell["height"]

    walls: set[Wall] = set()

    for cell in board_data:
        for wall_data in cell["walls"]:

            direction = wall_data["direction"]

            cell_x = wall_data["cellX"]
            cell_y = wall_data["cellY"]

            if direction in ("top", "bottom"):

                if direction == "top":
                    boundary_y = cell_y
                else:
                    boundary_y = cell_y + cell_height

                wall_row = round((boundary_y - board_y) / cell_height)

                wall_col = round((cell_x - board_x) / cell_width)

                if not (0 < wall_row < puzzle_height):
                    continue

                if not (0 <= wall_col < puzzle_width):
                    continue

                wall = Wall(
                    (wall_row - 1, wall_col),
                    (wall_row, wall_col),
                )

                walls.add(wall)

            elif direction in ("left", "right"):

                if direction == "left":
                    boundary_x = cell_x
                else:
                    boundary_x = cell_x + cell_width

                wall_col = round((boundary_x - board_x) / cell_width)

                wall_row = round((cell_y - board_y) / cell_height)

                if not (0 < wall_col < puzzle_width):
                    continue

                if not (0 <= wall_row < puzzle_height):
                    continue

                wall = Wall(
                    (wall_row, wall_col - 1),
                    (wall_row, wall_col),
                )

                walls.add(wall)

    puzzle = Puzzle(
        width=puzzle_width,
        height=puzzle_height,
        checkpoints=checkpoints,
        walls=walls,
    )

    return puzzle, board_data


def _get_cell_center(board_data, cell_idx: int) -> tuple[float, float]:
    """Gets the cell center cord of the board."""
    cell = board_data[cell_idx]
    return (
        cell["x"] + cell["width"] / 2,
        cell["y"] + cell["height"] / 2,
    )


def draw_path(page, board_data, path: list[int]) -> None:
    """Drags the mouse through each cell in `path`, in order."""

    if len(path) < 2:
        return

    start_x, start_y = _get_cell_center(board_data, path[0])

    page.mouse.move(start_x, start_y)
    page.mouse.down()

    for cell_idx in path[1:]:
        x, y = _get_cell_center(board_data, cell_idx)
        page.mouse.move(x, y)

    page.mouse.up()
