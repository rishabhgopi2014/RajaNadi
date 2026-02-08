# pyswisseph Installation Guide for Windows

## Issue
`pyswisseph` requires C++ compilation which often fails on Windows without proper build tools.

## Solutions (Try in order)

### Option 1: Install Pre-built Wheel (Recommended)
Download the appropriate wheel for your Python version from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyswisseph

Example for Python 3.11 (64-bit):
```bash
pip install pyswisseph-2.10.3.2-cp311-cp311-win_amd64.whl
```

### Option 2: Install Microsoft C++ Build Tools
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Restart terminal
4. Run: `pip install pyswisseph`

### Option 3: Use Anaconda
```bash
conda install -c conda-forge pyswisseph
```

### Option 4: Alternative Package
Use `astropy` instead (requires code changes):
```bash
pip install astropy skyfield
```

## Temporary Workaround
For testing without Swiss Ephemeris, I'll create a mock implementation.
