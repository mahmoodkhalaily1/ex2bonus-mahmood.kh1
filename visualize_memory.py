import ctypes
import os
import sys

# Import the definitions from the module
from bus_sort_module import BusLine, libbus, bubble_sort

# Define the callback type
# typedef void (*BubbleTracer)(BusLine *start, BusLine *end, BusLine *i, BusLine *j);
TracerCallbackType = ctypes.CFUNCTYPE(
    None, 
    ctypes.POINTER(BusLine), 
    ctypes.POINTER(BusLine), 
    ctypes.POINTER(BusLine), 
    ctypes.POINTER(BusLine)
)

def tracer_callback(start_ptr, end_ptr, i_ptr, j_ptr):
    try:
        # We need to access the underlying memory address to calculate the indices
        start_addr = ctypes.addressof(start_ptr.contents)
        end_addr = ctypes.addressof(end_ptr.contents)
        i_addr = ctypes.addressof(i_ptr.contents)
        j_addr = ctypes.addressof(j_ptr.contents)

        item_size = ctypes.sizeof(BusLine)

        # Calculate exact indices
        total_elements = (end_addr - start_addr) // item_size + 1
        i_idx = (i_addr - start_addr) // item_size
        j_idx = (j_addr - start_addr) // item_size

        print("\n" + "="*50)
        print(f"Step: i={i_idx}, j={j_idx}")
        print("="*50)

        # Cast start_ptr to an array of BusLines so we can iterate and read data
        arr_type = BusLine * total_elements
        bus_array = ctypes.cast(start_ptr, ctypes.POINTER(arr_type)).contents

        for idx in range(total_elements):
            bus = bus_array[idx]
            name_str = bus.name.decode('utf-8', errors='ignore').rstrip('\x00')
            
            # Formatting the visual string
            bus_info = f"[{idx:2d}] {name_str:<12} (Dist: {bus.distance:3d})"
            
            # Adding pointers (arrows)
            pointers = []
            if idx == 0:
                pointers.append("start")
            if idx == total_elements - 1:
                pointers.append("end")
            if idx == i_idx:
                pointers.append("i")
            if idx == j_idx:
                pointers.append("j")
                
            if pointers:
                pointer_str = " <--- " + ", ".join(pointers)
                print(f"{bus_info}{pointer_str}")
            else:
                print(f"{bus_info}")
                
        # Interactive pause
        input("\nPress [Enter] to continue to the next step...")
        
    except Exception as e:
        print(f"Error in callback: {e}")

# Create the callback instance (must keep a reference so it doesn't get garbage collected)
tracer_instance = TracerCallbackType(tracer_callback)

def setup_visualization():
    # Access the global variable bubble_sort_tracer from the shared library
    tracer_ptr = ctypes.c_void_p.in_dll(libbus, "bubble_sort_tracer")
    
    # Cast our python callback to a void pointer and assign it
    cb_ptr = ctypes.cast(tracer_instance, ctypes.c_void_p)
    tracer_ptr.value = cb_ptr.value

def run_demo():
    setup_visualization()
    
    # Create some dummy data
    buses = [
        BusLine(b"Express 10", distance=50),
        BusLine(b"Local 3", distance=20),
        BusLine(b"City 42", distance=10),
        BusLine(b"NightBus", distance=80),
        BusLine(b"Airport", distance=100)
    ]
    
    print("Starting visualizer. Initial state:")
    for b in buses:
        print(b)
        
    print("\nStarting Bubble Sort... (Sorts alphabetically by name)")
    print("Trace starting...\n")
    
    # We call the wrapper
    bubble_sort(buses)
    
    print("\n" + "="*50)
    print("Sorting Complete!")
    print("="*50)
    for b in buses:
        print(b)

if __name__ == "__main__":
    run_demo()
