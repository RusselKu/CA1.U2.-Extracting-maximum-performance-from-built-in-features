# CA1.U2 - Application Profiling: Performance Analysis

This project focuses on identifying I/O and CPU bottlenecks in a Python application that processes NOAA climate data. We use standard Python profiling tools like `cProfile`, `line_profiler`, and `snakeviz` to analyze and pinpoint performance issues.

## Project Structure

The project has been reorganized for clarity:

- `src/`: Contains all the Python source code.
  - `load.py`: Original script to download data.
  - `load_cache.py`: Script with a caching mechanism for network requests.
  - `distance.py`: Original script for distance calculations.
  - `distance_cache.py`: Script for distance calculations, prepared for line-by-line profiling.
- `profiling_results/`: Directory to store the output from profiling tools.
  - `cprofile/`: Stores `.prof` files from cProfile.
  - `line_profiler/`: Stores `.lprof` files from line_profiler.
- `report/`: Contains the final technical report.
- `Instructivo_todos.md`: The original project guide with role assignments.

## Setup

1.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Profiling Tasks

All commands should be run from the root of the project.

### 1. Baseline Profile (cProfile)

This task establishes a baseline for the original `load.py` script.

```bash
python -m cProfile -s cumulative src/load.py 01044099999,02293099999 2021-2021
```

### 2. I/O and Network Latency Analysis (cProfile)

This task analyzes the impact of network operations by generating a `.prof` file that can be visualized later.

```bash
python -m cProfile -o profiling_results/cprofile/profile_io.prof src/load.py 01044099999,02293099999 2021-2021
```
You can compare the execution time with the cached version:
```bash
python src/load_cache.py 01044099999,02293099999 2021-2021
```

### 3. Visualizing Profiling Data (SnakeViz)

Use the `.prof` file generated in the previous step to create a visual representation of the call stack.

```bash
snakeviz profiling_results/cprofile/profile_io.prof
```

### 4. Line-by-Line CPU Analysis (line_profiler)

This task pinpoints the exact lines of code that are CPU-intensive in the `distance_cache.py` script. The `@profile` decorator is already added to the `get_distance` function in `src/distance_cache.py`.

1.  **Generate the profiling data:**
    ```bash
    kernprof -l -o profiling_results/line_profiler/distance_cache.py.lprof src/distance_cache.py
    ```

2.  **View the results in the console:**
    ```bash
    python -m line_profiler profiling_results/line_profiler/distance_cache.py.lprof
    ```
