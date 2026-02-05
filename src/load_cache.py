import collections
import csv
import datetime
import sys
import requests
import os # Importar el módulo os para manejar archivos y directorios

raw_stations = sys.argv[1].split(",")
stations = []
for s in raw_stations:
    # NOAA station IDs are typically 11 digits. Pad with leading zeros if stripped.
    stations.append(s.zfill(11))
years = [int(year) for year in sys.argv[2].split("-")]
start_year = years[0]
end_year = years[1]

TEMPLATE_URL = "https://www.ncei.noaa.gov/data/global-hourly/access/{year}/{station}.csv"
TEMPLATE_FILE = "station_{station}_{year}.csv"

def download_data(station, year):
    file_name = TEMPLATE_FILE.format(station=station, year=year)
    # Verificar si el archivo ya existe antes de intentar descargarlo
    if os.path.exists(file_name):
        return

    my_url = TEMPLATE_URL.format(station=station, year=year)
    req = requests.get(my_url)
    if req.status_code != 200:
        return # not found
    
    with open(file_name, "wt") as w:
        w.write(req.text)

def download_all_data(stations, start_year, end_year):
    for station in stations:
        for year in range(start_year, end_year + 1):
            download_data(station, year)

def get_file_temperatures(file_name):
    with open(file_name, "rt") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            station = row[header.index("STATION")]
            # date = datetime.datetime.fromisoformat(row[header.index('DATE')])
            tmp = row[header.index("TMP")]
            temperature, status = tmp.split(",")
            if status != "1":
                continue
            temperature = int(temperature) / 10
            yield temperature

def get_all_temperatures(stations, start_year, end_year):
    temperatures = collections.defaultdict(list)
    for station in stations:
        for year in range(start_year, end_year + 1):
            file_name = TEMPLATE_FILE.format(station=station, year=year)
            if not os.path.exists(file_name):
                continue
            for temperature in get_file_temperatures(file_name):
                temperatures[station].append(temperature)
    return temperatures

def get_min_temperatures(all_temperatures):
    return {station: min(temperatures) for station, temperatures in
            all_temperatures.items()}

# Main execution block
if __name__ == "__main__":
    download_all_data(stations, start_year, end_year)
    all_temperatures = get_all_temperatures(stations, start_year, end_year)
    min_temperatures = get_min_temperatures(all_temperatures)
    print(min_temperatures)
