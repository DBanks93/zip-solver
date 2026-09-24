# LinkedIn Solvers

This project contains solvers for [LinkedIn puzzles](https://www.linkedin.com/games).

They aren't meant to be the fastest possible (Otherwise I'd use C, or rust), I'm doing this to keep my Python skills up to scratch.

## Current solvers:
- [Zip](linkedin_solvers/zipsolver/README.md)

## How to run:
### Simple
> Requirements: Make sure you have Python 3.13 installed locally
For macOS/Linux run:
```shell
./run.sh <solver name>
```

For windows (ew) run:
```
run.bat <solver name>
```

### Advanced(ish)
The project was built using poetry since I haven't used it before - it's an excuse to move away from pipenv.

To get everything working run:
```shell
make install
```

Then to run the app run:
```shell
make run_<solver>
```

If you make changes and want very very basic lint/format it use:
```shell
make lint # Runs lint checks

make format # auto applies fixes
```
