from bus_sort_module import BusLine, SortType, bubble_sort, quick_sort

if __name__ == "__main__":
    # Create hardcoded list for Bubble Sort
    # Note: names must be passed as byte strings (b"...") due to c_char array
    lines_for_bubble = [
        BusLine(name=b"Line A", distance=100, duration=60, frequency=2),
        BusLine(name=b"Line B", distance=50, duration=45, frequency=5),
        BusLine(name=b"Line C", distance=150, duration=90, frequency=1)
    ]
    
    print("=== Original Array (Bubble Sort) ===")
    for line in lines_for_bubble:
        print(line)
        
    print("\n=== After Bubble Sort ===")
    bubble_sort(lines_for_bubble)
    for line in lines_for_bubble:
        print(line)
        
    print("-" * 40)
        
    # Create hardcoded list for Quick Sort
    lines_for_quick = [
        BusLine(name=b"Express 1", distance=200, duration=30, frequency=10),
        BusLine(name=b"Local 2", distance=10, duration=40, frequency=15),
        BusLine(name=b"Night Bus", distance=300, duration=15, frequency=1)
    ]
    
    print("\n=== Original Array (Quick Sort) ===")
    for line in lines_for_quick:
        print(line)
        
    print("\n=== After Quick Sort (by FREQUENCY) ===")
    quick_sort(lines_for_quick, SortType.FREQUENCY)
    for line in lines_for_quick:
        print(line)
