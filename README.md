# Moovit-Style Campus Navigator & Bus Sorting Tool

This project provides a robust integration of high-performance C sorting algorithms with a modern Python interface. It features a complete `ctypes` binding layer, an interactive text-based execution visualizer, and a graphical Moovit-style web application built with Streamlit and Folium.

**GitHub Repository:** `[https://github.com/mahmoodkhalaily1/ex2bonus-mahmood.kh1.git]`

## Implemented Parts

### Part A: Python Bindings
A robust `ctypes` interface (`bus_sort_module.py`) that securely bridges Python and the underlying C sorting library (`libbus.so`). It maps C structures to Python classes, handles memory management safely, and is validated by a comprehensive suite of automated tests (`test_bus_sort.py`).

### Part B: Memory Visualization Hook
An interactive, text-based execution tracker (`visualize_memory.py`). A global callback hook was cleanly integrated into the C `bus_bubble_sort` algorithm without breaking its core logic. The Python script attaches to this hook, calculating exact memory offsets dynamically to provide a step-by-step visual representation of pointer movements (`start`, `end`, `i`, `j`) directly in the terminal.

### Part C: Moovit-Style GUI with Streamlit
A fully-featured graphical web application (`moovit_app.py`). It simulates a campus navigation app where users can select starting points in Jerusalem and target destinations at the Hebrew University campuses. It generates realistic mock route data, sorts it via the C backend, and visualizes the journey on an interactive OpenStreetMap.

---

## Project Structure

* **`sort_bus_lines.c` & `sort_bus_lines.h`**: The core C implementation containing the Bubble Sort and Quick Sort algorithms, as well as the instrumentation hook for memory tracking.
* **`bus_sort_module.py`**: The `ctypes` wrapper module that exposes the C functions and structures to Python securely.
* **`test_bus_sort.py`**: The pytest suite that verifies the correctness of the sorting bindings and handles edge cases.
* **`visualize_memory.py`**: The interactive CLI visualization script (Part B).
* **`moovit_app.py`**: The Streamlit web application with Folium map integration (Part C).
* **`libbus.so`**: The compiled shared library generated from the C code.

---

## How to Run

### Prerequisites
Before running the interactive apps, ensure the shared library is compiled:
```bash
gcc -shared -fPIC -o libbus.so sort_bus_lines.c
```

### Running Part B: Execution Visualizer
To interactively watch the memory pointers during the execution of the C Bubble Sort:
1. Open your terminal.
2. Run the visualization script:
   ```bash
   python visualize_memory.py
   ```
3. Press `Enter` to advance through each iteration step.

### Running Part C: Moovit Streamlit App
To launch the graphical campus navigator application:
1. Activate your virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Make sure you have the required UI dependencies installed:
   ```bash
   pip install streamlit folium streamlit-folium
   ```
3. Start the Streamlit server:
   ```bash
   streamlit run moovit_app.py
   ```
4. The application will automatically open in your default web browser.
