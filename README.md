# Zip Solver
A program that can solve LinkedIn Zip program.

This isn't meant to be the fastest possible (Otherwise I'd use C, or rust),
I'm doing this to keep my Python skills up to scratch.

> [!NOTE]
> This program may be considered cheating, so use it at your own discretion.
> The solver runs using Chrome for Testing, meaning you won't be logged into LinkedIn and your results won't be saved to your account.
> 
> Please do not spam, abuse, or use this program for malicious purposes.

## Running the app
### Simple
> Requirements: Make sure you have Python 3.13 installed locally
For macOS/Linux run:
```shell
./run.sh
```

For windows (ew) run:
```
run.bat
```

### Advanced(ish)
The project was built using poetry since I haven't used it before - it's an excuse to move away from pipenv.

To get everything working run:
```shell
make install
```

Then to run the app run:
```shell
make run
```

If you make changes and want very very basic lint/format it use:
```shell
make lint # Runs lint checks

make format # auto applies fixes
```

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


## Interactive Screen
To grab the data from LinkedIn and to actually draw the result [Playwright](https://playwright.dev/python/docs/intro) 
is used.

### Scraping the data
The HTML from the page is used to determine where the walls and checkpoints are.

Thankfully all cells contain the attribute `data-testid="cell-<cell-number>"` with the cell number matching cell numbers used in the [algorith](#algorithm-).
We can use a css selector to get every cell `[data-testid^="cell-"]`.

Now we have a list of all the cells we can then iterate over them to get the info we need such as [Checkpoints](#checkpoints) and [Walls](#walls).

#### Checkpoints
All checkpoints have an `aria-label` with the checkpoint number (I presume for accessibility):
`aria-label="Number <checkpoint>`.

This data can be scraped and paired with the cell number, simple really.

#### Walls
Walls is not so simple. There is no label saying 'this is a wall'.
It appeared that the class names/labels (I'm no frontend dev so not sure what you call it), are hashed making my life harder.

However, walls can be identified by looking at the child elements of each cell and how big the border is.
The wall elements all have a consistent set of CSS classes which can be used to identify them, then the `::after` element contains the border which is used to render the wall.
So, each of the four border widths (top, right, bottom, left) can be checked and if they contain a 12px border then it's a wall.
This can be stored as well as the direction of the wall to determine the adjacent cell which is how walls are stored.

### Drawing on the screen
Once the puzzle has been solved, we can just use playwright to 'click and drag' the path result across the screen.