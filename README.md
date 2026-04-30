# NumberCruncher: Multi-Language Countdown Solver

## Overview
NumberCruncher is a comparative logic suite designed to solve the numeric portion of the Countdown game. It features three independent solvers written in **Python**, **Haskell**, and **Prolog**, orchestrated by a unified Text User Interface (TUI) for benchmarking and result comparison.


## Prerequisites & Installation

### Core Dependencies
To run the full suite, one must install the compilers and interpreters for all three languages.

| Platform | Command |
|----------|---------|
| **Debian / Ubuntu / Kali** | `sudo apt update && sudo apt install python3 ghc swi-prolog` |
| **Arch Linux** | `sudo pacman -Syu python ghc swi-prolog` |
| **macOS (Homebrew)** | `brew install python ghc swi-prolog` |

### Python Dependencies
The TUI requires the `rich` library. Install it using the provided requirements file:
```bash
pip install -r requirements.txt
```
#### If on Debian based systems 
```bash
sudo apt install python3-rich # much simpler
```

## Running the Project
The primary entry point is the interactive TUI. Run it from the project root:
```bash
python src/tui_wraper/tui.py
```
This will launch a menu to select difficulty levels or enter custom target numbers and values.
---
![TUI main](images/TUI_Selection_Page.png)

![TUI output](images/TUI_Output_Page.png)
---
## Documentation Index
Detailed technical references for every component are available in the repository:
- [Source Code Overview](src/README.md)
- [Python Solver Reference](docs/src_docs/countdown_py_doc.md)
- [Haskell Solver Reference](docs/src_docs/countdown_hs_doc.md)
- [Prolog Solver Reference](docs/src_docs/countdown_pl_doc.md)
- [TUI & Execution Orchestration Reference](docs/src_docs/tui_py_doc.md)

## Project Structure
- `src/python/`: Recursive search implementation in Python.
- `src/haskell/`: Expression tree search using Haskell.
- `src/prolog/`: Backtracking-based search in SWI-Prolog.
- `src/tui_wraper/`: Consolidation layer including `run_all.sh` and the TUI.