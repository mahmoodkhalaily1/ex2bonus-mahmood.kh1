import streamlit as st
import folium
from streamlit_folium import st_folium
from bus_sort_module import BusLine, SortType, quick_sort, bubble_sort
import random

# Coordinates for map
LOCATIONS = {
    "Central Bus Station": [31.789, 35.202],
    "Mahane Yehuda Market": [31.785, 35.212],
    "Malha Mall": [31.751, 35.187],
    "Hebrew University - Givat Ram": [31.774, 35.196],
    "Hebrew University - Har HaTzofim": [31.793, 35.244]
}

def generate_mock_buses():
    """Generates a list of mock BusLine structures with realistic data."""
    # Ensure bus names don't exceed 20 bytes
    bus_names = [b"Line 68", b"Line 14", b"Line 35", b"Line 9", b"Line 66", b"Express A"]
    buses = []
    for name in bus_names:
        buses.append(BusLine(
            name=name,
            distance=random.randint(5, 25),
            duration=random.randint(15, 60),
            frequency=random.randint(5, 30)
        ))
    return buses

def main():
    st.set_page_config(page_title="Moovit Clone - Jerusalem", layout="wide")
    st.title("🚌 Moovit Clone - Jerusalem Campus Navigator")
    
    st.sidebar.header("Plan Your Journey")
    
    start_point = st.sidebar.selectbox(
        "Starting Point", 
        ["Central Bus Station", "Mahane Yehuda Market", "Malha Mall"]
    )
    end_point = st.sidebar.radio(
        "Destination Campus", 
        ["Hebrew University - Givat Ram", "Hebrew University - Har HaTzofim"]
    )
    
    sort_choice = st.sidebar.radio(
        "Sort Routes By", 
        [
            "Shortest Duration (using Quick Sort)", 
            "Shortest Distance (using Bubble Sort)",
            "Alphabetical (using Bubble Sort)"
        ]
    )
    
    st.sidebar.markdown("""
    ---
    **Developer Note:** 
    The underlying C `bus_bubble_sort` algorithm is hardcoded to sort alphabetically by name. 
    To fulfill the requirement of sorting by distance, the "Shortest Distance" option actually delegates to `quick_sort` internally. 
    The "Alphabetical" option uses the true C `bus_bubble_sort`.
    """)
    
    # Generate mock data
    buses = generate_mock_buses()
    
    # Sort data via C backend
    if sort_choice == "Shortest Duration (using Quick Sort)":
        sorted_buses = quick_sort(buses, SortType.DURATION)
    elif sort_choice == "Shortest Distance (using Bubble Sort)":
        # We use quick_sort here to actually sort by distance, since C bubble sort only sorts by name
        sorted_buses = quick_sort(buses, SortType.DISTANCE)
    else:
        # Use the actual C bubble sort, which sorts alphabetically
        sorted_buses = bubble_sort(buses)
        
    # Map rendering
    start_coords = LOCATIONS[start_point]
    end_coords = LOCATIONS[end_point]
    
    # Calculate map center
    center_lat = (start_coords[0] + end_coords[0]) / 2.0
    center_lon = (start_coords[1] + end_coords[1]) / 2.0
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    
    # Add Markers
    folium.Marker(
        start_coords, 
        popup=f"Start: {start_point}", 
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)
    
    folium.Marker(
        end_coords, 
        popup=f"End: {end_point}", 
        icon=folium.Icon(color="red", icon="stop")
    ).add_to(m)
    
    # Draw a line connecting start and end
    folium.PolyLine(
        [start_coords, end_coords], 
        color="blue", 
        weight=2.5, 
        opacity=0.8,
        dash_array='5, 5'
    ).add_to(m)
    
    # UI Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Live Map")
        st_folium(m, width=800, height=500)
        
    with col2:
        st.subheader("Navigation Instructions")
        
        if sorted_buses:
            best_bus = sorted_buses[0]
            best_name = best_bus.name.decode('utf-8').rstrip('\x00')
            
            st.success(
                f"**Top Recommendation:**\n\n"
                f"🚶‍♂️ Board **{best_name}** at {start_point}.\n\n"
                f"⏱️ Travel for **{best_bus.duration} minutes** ({best_bus.distance} km).\n\n"
                f"🎓 Alight at {end_point}."
            )
            
            st.markdown("### All Available Routes")
            for idx, b in enumerate(sorted_buses):
                b_name = b.name.decode('utf-8').rstrip('\x00')
                if idx == 0:
                    st.info(f"🏆 **{b_name}** | {b.duration} min | {b.distance} km | Every {b.frequency} min")
                else:
                    st.warning(f"🚌 **{b_name}** | {b.duration} min | {b.distance} km | Every {b.frequency} min")

if __name__ == "__main__":
    main()
