import csv
import math


try:
    profile  # type: ignore[name-defined]
except NameError:  # pragma: no cover

    def profile(func):  # type: ignore[no-redef]
        return func


def get_locations(file_path: str = "locations.csv"):
    with open(file_path, "rt", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            station = row[header.index("STATION")]
            lat = float(row[header.index("LATITUDE")])
            lon = float(row[header.index("LONGITUDE")])
            yield station, (lat, lon)


@profile
def get_distance(p1, p2):
    lat1, lon1 = p1
    lat2, lon2 = p2

    # Haversine formula
    lat_dist = math.radians(lat2 - lat1)
    lon_dist = math.radians(lon2 - lon1)
    a = math.sin(lat_dist / 2) * math.sin(lat_dist / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(lon_dist / 2) * math.sin(lon_dist / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    earth_radius = 6371
    dist = earth_radius * c
    return dist


def get_distances(stations, locations):
    distances = {}
    for first_i in range(len(stations) - 1):
        first_station = stations[first_i]
        first_location = locations[first_station]
        for second_i in range(first_i, len(stations)):
            second_station = stations[second_i]
            second_location = locations[second_station]
            distances[(first_station, second_station)] = get_distance(
                first_location, second_location
            )
    return distances


if __name__ == "__main__":
    locations = {station: (lat, lon) for station, (lat, lon) in get_locations()}
    stations = sorted(locations.keys())
    distances = get_distances(stations, locations)
    # Prevent the optimizer/interpreter from potentially skipping work.
    print(len(distances))
