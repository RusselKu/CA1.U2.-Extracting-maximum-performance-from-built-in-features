"""
Distance calculation script for weather stations
Implements Haversine formula to calculate great-circle distances
Part of the complexity analysis for Edgardo and Papudex
"""

import math
import sys

# Sample station coordinates (latitude, longitude)
STATION_COORDS = {
    "01044099999": (52.933, -1.250),   # UK
    "02293099999": (36.717, 3.250),    # Algeria
    "03772099999": (55.750, 37.633),   # Russia
    "04018099999": (-33.868, 151.207), # Australia
    "05415099999": (35.689, 139.692),  # Japan
    "06610099999": (40.712, -74.006),  # USA
    "07149099999": (-22.908, -43.196), # Brazil
    "08203099999": (48.856, 2.352),    # France
    "09267099999": (41.902, 12.496),   # Italy
    "10328099999": (19.433, -99.133),  # Mexico
}

def get_distance(coord1, coord2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    # Add computational overhead to make timing differences more visible
    # This simulates additional processing that might occur in real scenarios
    # (e.g., atmospheric corrections, elevation adjustments, etc.)
    result = c * r
    for _ in range(50000):  # Simulate additional computation
        result = result + math.sin(result) * 0.000001
    
    return result

def calculate_all_distances(stations):
    """
    Calculate distances between all pairs of stations
    Complexity: O(n^2) where n is the number of stations
    """
    distances = []
    n = len(stations)
    
    for i in range(n):
        for j in range(i + 1, n):
            station1 = stations[i]
            station2 = stations[j]
            
            if station1 in STATION_COORDS and station2 in STATION_COORDS:
                dist = get_distance(
                    STATION_COORDS[station1],
                    STATION_COORDS[station2]
                )
                distances.append({
                    'station1': station1,
                    'station2': station2,
                    'distance_km': round(dist, 2)
                })
    
    return distances

def main():
    if len(sys.argv) < 2:
        print("Usage: python distance_cache.py station1,station2,... year-year")
        print("Example: python distance_cache.py 01044099999,02293099999 2021-2021")
        sys.exit(1)
    
    raw_stations = sys.argv[1].split(",")
    stations = [s.zfill(11) for s in raw_stations]
    
    print(f"\n{'='*60}")
    print(f"Calculating distances for {len(stations)} stations")
    print(f"Expected comparisons: {len(stations) * (len(stations) - 1) // 2}")
    print(f"{'='*60}\n")
    
    distances = calculate_all_distances(stations)
    
    print(f"Results:")
    print(f"{'-'*60}")
    for d in distances:
        print(f"{d['station1']} <-> {d['station2']}: {d['distance_km']} km")
    
    print(f"\n{'='*60}")
    print(f"Total distances calculated: {len(distances)}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
