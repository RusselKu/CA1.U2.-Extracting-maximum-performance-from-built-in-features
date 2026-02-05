import argparse
import csv
import os
import random
import time
from dataclasses import dataclass

import matplotlib.pyplot as plt

from distance_cache import get_distance, get_distances


@dataclass(frozen=True)
class BenchmarkRow:
    n_stations: int
    n_pairs: int
    seconds: float


def _make_synthetic_locations(n: int, seed: int):
    rng = random.Random(seed)
    locations = {}
    stations = []
    for i in range(1, n + 1):
        station = str(i).zfill(11)
        lat = rng.uniform(-90.0, 90.0)
        lon = rng.uniform(-180.0, 180.0)
        locations[station] = (lat, lon)
        stations.append(station)
    return stations, locations


def _time_one_run(stations, locations):
    start = time.perf_counter()
    distances = get_distances(stations, locations)
    # consume result so work can't be skipped
    _ = len(distances)
    end = time.perf_counter()
    return end - start


def run_benchmark(sizes, max_locations, seed, repeats):
    stations_all, locations = _make_synthetic_locations(max_locations, seed)

    rows: list[BenchmarkRow] = []
    for n in sizes:
        stations = stations_all[:n]
        # Quick sanity: force at least one call to get_distance
        _ = get_distance(locations[stations[0]], locations[stations[-1]])

        times = [_time_one_run(stations, locations) for _ in range(repeats)]
        best = min(times)
        n_pairs = (
            n * (n + 1)
        ) // 2 - 1  # matches loop in get_distances (upper triangle)
        rows.append(BenchmarkRow(n_stations=n, n_pairs=n_pairs, seconds=best))

    return rows


def write_csv(rows, csv_path):
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n_stations", "n_pairs", "seconds_best"])
        for r in rows:
            writer.writerow([r.n_stations, r.n_pairs, f"{r.seconds:.6f}"])


def write_table_png(rows, png_path, title):
    col_labels = ["N° estaciones", "Pares", "Tiempo (s) (mejor)"]
    cell_text = [[str(r.n_stations), str(r.n_pairs), f"{r.seconds:.6f}"] for r in rows]

    fig_height = 0.6 + 0.35 * (len(rows) + 1)
    fig, ax = plt.subplots(figsize=(8.5, fig_height))
    ax.axis("off")
    ax.set_title(title, pad=12)

    table = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        loc="center",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.35)

    fig.tight_layout()
    fig.savefig(png_path, dpi=200)
    plt.close(fig)


def parse_sizes(value: str):
    parts = [p.strip() for p in value.split(",") if p.strip()]
    sizes = [int(p) for p in parts]
    if any(n < 2 for n in sizes):
        raise argparse.ArgumentTypeError("All sizes must be >= 2")
    if sorted(sizes) != sizes:
        raise argparse.ArgumentTypeError("Sizes must be sorted ascending")
    return sizes


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark de complejidad (n^2) para cálculo de distancias"
    )
    parser.add_argument(
        "--sizes",
        type=parse_sizes,
        default=[50, 100, 200, 400, 800],
        help="Lista de N separados por coma (ej. 50,100,200)",
    )
    parser.add_argument(
        "--max-locations",
        type=int,
        default=800,
        help="Cantidad de ubicaciones sintéticas a generar (>= max(sizes))",
    )
    parser.add_argument("--seed", type=int, default=0, help="Semilla RNG")
    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="Repeticiones por tamaño (se toma el mejor)",
    )
    parser.add_argument(
        "--out-dir",
        default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        help="Directorio de salida para CSV/PNG",
    )

    args = parser.parse_args()

    max_size = max(args.sizes)
    if args.max_locations < max_size:
        raise SystemExit("--max-locations must be >= max(--sizes)")

    rows = run_benchmark(args.sizes, args.max_locations, args.seed, args.repeats)

    os.makedirs(args.out_dir, exist_ok=True)
    csv_path = os.path.join(args.out_dir, "tabla_complejidad.csv")
    png_path = os.path.join(args.out_dir, "tabla_complejidad.png")

    write_csv(rows, csv_path)
    write_table_png(
        rows,
        png_path,
        title="Comparativa de complejidad: N° estaciones vs Tiempo total",
    )

    print(f"Wrote {csv_path}")
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()
