import ctypes
import os
from enum import IntEnum

# Map the SortType enum
class SortType(IntEnum):
    DISTANCE = 0
    DURATION = 1
    FREQUENCY = 2

# Map the BusLine struct
class BusLine(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_char * 21),
        ("distance", ctypes.c_int),
        ("duration", ctypes.c_int),
        ("frequency", ctypes.c_int)
    ]
    
    def __init__(self, name: bytes = b"", distance: int = 0, duration: int = 0, frequency: int = 0):
        # Enforce maximum length of 20 characters to ensure the 21st byte is always '\0'
        if len(name) > 20:
            raise ValueError(f"BusLine name cannot exceed 20 bytes to reserve space for the null terminator. Got {len(name)} bytes.")
        super().__init__(name=name, distance=distance, duration=duration, frequency=frequency)
    
    def __repr__(self):
        # Decode the byte string to normal string for printing
        name_str = self.name.decode('utf-8', errors='ignore').rstrip('\x00')
        return f"BusLine(name='{name_str}', distance={self.distance}, duration={self.duration}, freq={self.frequency})"

# Load the shared library
lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libbus.so")

# Explicitly raise an error if the library doesn't exist, preventing silent failures
if not os.path.exists(lib_path):
    raise OSError(f"Shared library not found at: {lib_path}. Please compile sort_bus_lines.c first.")

libbus = ctypes.CDLL(lib_path)

# void bus_bubble_sort(BusLine *start, BusLine *end);
libbus.bus_bubble_sort.argtypes = [ctypes.POINTER(BusLine), ctypes.POINTER(BusLine)]
libbus.bus_bubble_sort.restype = None

# void bus_quick_sort(BusLine *start, BusLine *end, SortType sort_type);
libbus.bus_quick_sort.argtypes = [ctypes.POINTER(BusLine), ctypes.POINTER(BusLine), ctypes.c_int]
libbus.bus_quick_sort.restype = None

def bubble_sort(lines: list[BusLine]):
    if not lines:
        return lines
    
    # Create a C array from the Python list
    arr_type = BusLine * len(lines)
    c_array = arr_type(*lines)
    
    # Get pointer to the start
    start_ptr = ctypes.cast(c_array, ctypes.POINTER(BusLine))
    
    # Calculate pointer to the end (memory address of the *last* element, not one-past-the-end)
    end_address = ctypes.addressof(c_array) + (len(lines) - 1) * ctypes.sizeof(BusLine)
    end_ptr = ctypes.cast(end_address, ctypes.POINTER(BusLine))
    
    # Call the C function
    libbus.bus_bubble_sort(start_ptr, end_ptr)
    
    # Copy the sorted values back into the Python list
    for i in range(len(lines)):
        lines[i] = c_array[i]
    return lines

def quick_sort(lines: list[BusLine], sort_type: SortType):
    if not lines:
        return lines
        
    arr_type = BusLine * len(lines)
    c_array = arr_type(*lines)
    
    start_ptr = ctypes.cast(c_array, ctypes.POINTER(BusLine))
    
    # Point to the last element
    end_address = ctypes.addressof(c_array) + (len(lines) - 1) * ctypes.sizeof(BusLine)
    end_ptr = ctypes.cast(end_address, ctypes.POINTER(BusLine))
    
    # Call the C function with the enum value
    libbus.bus_quick_sort(start_ptr, end_ptr, sort_type.value)
    
    for i in range(len(lines)):
        lines[i] = c_array[i]
    return lines
