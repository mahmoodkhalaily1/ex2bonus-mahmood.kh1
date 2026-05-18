import pytest
from bus_sort_module import BusLine, SortType, bubble_sort, quick_sort

@pytest.fixture
def sample_lines():
    """Returns a fresh list of BusLines for each test."""
    return [
        BusLine(name=b"Zebra Bus", distance=100, duration=60, frequency=2),
        BusLine(name=b"Apple Line", distance=50, duration=45, frequency=5),
        BusLine(name=b"Monkey Express", distance=150, duration=90, frequency=1)
    ]

def test_bubble_sort_by_name(sample_lines):
    """Verifies that bubble sort correctly sorts by name alphabetically."""
    sorted_lines = bubble_sort(sample_lines)
    
    # Check the names in alphabetical order
    assert sorted_lines[0].name.decode('utf-8').rstrip('\x00') == "Apple Line"
    assert sorted_lines[1].name.decode('utf-8').rstrip('\x00') == "Monkey Express"
    assert sorted_lines[2].name.decode('utf-8').rstrip('\x00') == "Zebra Bus"

def test_quick_sort_by_distance(sample_lines):
    """Verifies that quick sort correctly sorts by distance."""
    sorted_lines = quick_sort(sample_lines, SortType.DISTANCE)
    
    assert sorted_lines[0].distance == 50
    assert sorted_lines[1].distance == 100
    assert sorted_lines[2].distance == 150

def test_quick_sort_by_duration(sample_lines):
    """Verifies that quick sort correctly sorts by duration."""
    sorted_lines = quick_sort(sample_lines, SortType.DURATION)
    
    assert sorted_lines[0].duration == 45
    assert sorted_lines[1].duration == 60
    assert sorted_lines[2].duration == 90

def test_quick_sort_by_frequency(sample_lines):
    """Verifies that quick sort correctly sorts by frequency."""
    sorted_lines = quick_sort(sample_lines, SortType.FREQUENCY)
    
    assert sorted_lines[0].frequency == 1
    assert sorted_lines[1].frequency == 2
    assert sorted_lines[2].frequency == 5

# ================= Edge Cases =================

def test_edge_case_empty_list():
    """Verifies that the module robustly handles empty lists without crashing."""
    assert bubble_sort([]) == []
    assert quick_sort([], SortType.DISTANCE) == []

def test_edge_case_single_item():
    """Verifies that sorting a single item works correctly."""
    lines = [BusLine(name=b"Single", distance=10, duration=10, frequency=1)]
    
    res_bubble = bubble_sort(lines.copy())
    assert res_bubble[0].name.decode('utf-8').rstrip('\x00') == "Single"
    
    res_quick = quick_sort(lines.copy(), SortType.DURATION)
    assert res_quick[0].distance == 10

def test_edge_case_identical_items():
    """Verifies that the sort algorithms can handle identical elements."""
    lines = [
        BusLine(name=b"Same", distance=10, duration=10, frequency=1),
        BusLine(name=b"Same", distance=10, duration=10, frequency=1)
    ]
    
    sorted_lines = quick_sort(lines, SortType.DISTANCE)
    assert len(sorted_lines) == 2
    assert sorted_lines[0].distance == 10
    assert sorted_lines[1].distance == 10
