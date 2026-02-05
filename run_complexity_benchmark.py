#!/usr/bin/env python3
"""
Automated benchmark script for Edgardo and Papudex
Runs distance calculations with varying numbers of stations
and measures execution time
"""

import subprocess
import time
import sys
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Different test cases
TEST_CASES = [
    {
        "name": "Set Pequeño (2 estaciones)",
        "stations": "01044099999,02293099999",
        "expected_comparisons": 1
    },
    {
        "name": "Set Mediano (5 estaciones)", 
        "stations": "01044099999,02293099999,03772099999,04018099999,05415099999",
        "expected_comparisons": 10
    },
    {
        "name": "Set Grande (10 estaciones)",
        "stations": "01044099999,02293099999,03772099999,04018099999,05415099999,06610099999,07149099999,08203099999,09267099999,10328099999",
        "expected_comparisons": 45
    }
]

def run_benchmark(stations, name, expected_comparisons):
    """Run a single benchmark test"""
    print(f"\n{'='*70}")
    print(f"Ejecutando: {name}")
    print(f"Estaciones: {len(stations.split(','))}")
    print(f"Comparaciones esperadas: {expected_comparisons}")
    print(f"{'='*70}")
    
    # Run with time measurement
    start_time = time.time()
    
    try:
        result = subprocess.run(
            ["python3", "src/distance_cache.py", stations, "2021-2021"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        elapsed_time = time.time() - start_time
        
        print(result.stdout)
        if result.stderr:
            print("Errores:", result.stderr)
        
        print(f"\n⏱️  Tiempo de ejecución: {elapsed_time:.3f} segundos")
        
        return {
            "name": name,
            "stations": len(stations.split(',')),
            "comparisons": expected_comparisons,
            "time": elapsed_time,
            "success": result.returncode == 0
        }
        
    except subprocess.TimeoutExpired:
        print("❌ Timeout - el proceso tomó más de 30 segundos")
        return {
            "name": name,
            "stations": len(stations.split(',')),
            "comparisons": expected_comparisons,
            "time": -1,
            "success": False
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "name": name,
            "stations": len(stations.split(',')),
            "comparisons": expected_comparisons,
            "time": -1,
            "success": False
        }

def print_summary(results):
    """Print a summary table of all results"""
    print("\n" + "="*80)
    print("📊 RESUMEN DE RESULTADOS - ANÁLISIS DE COMPLEJIDAD")
    print("="*80)
    print(f"\n{'N° Estaciones':<15} {'Comparaciones':<15} {'Tiempo (s)':<15} {'Factor':<15}")
    print("-" * 80)
    
    baseline_time = None
    for r in results:
        if not r['success']:
            continue
            
        if baseline_time is None:
            baseline_time = r['time']
            factor = 1.0
        else:
            factor = r['time'] / baseline_time if baseline_time > 0 else 0
        
        print(f"{r['stations']:<15} {r['comparisons']:<15} {r['time']:<15.3f} {factor:<15.1f}x")
    
    print("\n" + "="*80)
    print("✅ Análisis completado")
    print("="*80)
    
    # Calculate theoretical complexity
    print("\n📐 Análisis de Complejidad Teórica:")
    if len(results) >= 2 and results[0]['success'] and results[-1]['success']:
        first = results[0]
        last = results[-1]
        
        stations_ratio = last['stations'] / first['stations']
        time_ratio = last['time'] / first['time']
        theoretical_ratio = stations_ratio ** 2
        
        print(f"  - Incremento de estaciones: {stations_ratio:.1f}x")
        print(f"  - Incremento de tiempo observado: {time_ratio:.1f}x")
        print(f"  - Incremento teórico O(n²): {theoretical_ratio:.1f}x")
        print(f"  - Confirmación de complejidad: {'✅ O(n²)' if abs(time_ratio - theoretical_ratio) / theoretical_ratio < 0.5 else '⚠️  Revisar'}")

def generate_graphs(results):
    """Generate visualization graphs for the complexity analysis"""
    successful_results = [r for r in results if r['success']]
    
    if len(successful_results) < 2:
        print("\n⚠️  No hay suficientes datos para generar gráficos")
        return
    
    stations = [r['stations'] for r in successful_results]
    times = [r['time'] for r in successful_results]
    comparisons = [r['comparisons'] for r in successful_results]
    
    # Create figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Análisis de Complejidad Algorítmica - Edgardo y Papudex', 
                 fontsize=16, fontweight='bold')
    
    # Graph 1: Stations vs Time (Actual Results)
    ax1.plot(stations, times, 'o-', linewidth=2, markersize=10, 
             color='#2E86AB', label='Tiempo Real')
    ax1.set_xlabel('N° de Estaciones', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
    ax1.set_title('Estaciones vs Tiempo de Ejecución', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Add value labels on points
    for i, (x, y) in enumerate(zip(stations, times)):
        ax1.annotate(f'{y:.3f}s', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    # Graph 2: Stations vs Time with O(n²) theoretical curve
    ax2.plot(stations, times, 'o-', linewidth=2, markersize=10, 
             color='#2E86AB', label='Tiempo Real')
    
    # Calculate theoretical O(n²) curve
    if times[0] > 0:
        # Normalize to first point
        baseline_stations = stations[0]
        baseline_time = times[0]
        theoretical_times = [(s/baseline_stations)**2 * baseline_time for s in stations]
        
        ax2.plot(stations, theoretical_times, '--', linewidth=2, 
                color='#A23B72', label='O(n²) Teórico')
    
    ax2.set_xlabel('N° de Estaciones', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
    ax2.set_title('Comparación: Real vs Teórico O(n²)', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Graph 3: Comparisons vs Time
    ax3.plot(comparisons, times, 's-', linewidth=2, markersize=10, 
             color='#F18F01', label='Tiempo por Comparaciones')
    ax3.set_xlabel('N° de Comparaciones', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
    ax3.set_title('Comparaciones vs Tiempo', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Add value labels
    for i, (x, y) in enumerate(zip(comparisons, times)):
        ax3.annotate(f'{y:.3f}s', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    plt.tight_layout()
    
    # Save the figure
    filename = 'complexity_analysis_graphs.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\n📊 Gráficos guardados en: {filename}")
    
    # Create a second figure with bar chart
    fig2, ax4 = plt.subplots(figsize=(10, 6))
    
    # Bar chart for time comparison
    colors = ['#06A77D', '#2E86AB', '#A23B72']
    bars = ax4.bar(range(len(stations)), times, color=colors[:len(stations)], 
                   alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax4.set_xlabel('N° de Estaciones', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
    ax4.set_title('Tabla Comparativa: N° Estaciones vs Tiempo Total de Ejecución', 
                  fontsize=14, fontweight='bold')
    ax4.set_xticks(range(len(stations)))
    ax4.set_xticklabels([f'{s} estaciones\n({c} comp.)' 
                         for s, c in zip(stations, comparisons)])
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (bar, time_val, comp) in enumerate(zip(bars, times, comparisons)):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{time_val:.3f}s',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    filename2 = 'time_comparison_bar_chart.png'
    plt.savefig(filename2, dpi=300, bbox_inches='tight')
    print(f"📊 Gráfico de barras guardado en: {filename2}")
    
    print("\n✅ Visualizaciones generadas exitosamente")

def main():
    print("🚀 Benchmark Automático - Análisis de Complejidad Algorítmica")
    print("    Autores: Edgardo y Papudex")
    print("    Proyecto: CA1.U2 - Profiling de Aplicaciones\n")
    
    results = []
    
    for test_case in TEST_CASES:
        result = run_benchmark(
            test_case["stations"],
            test_case["name"],
            test_case["expected_comparisons"]
        )
        results.append(result)
        time.sleep(1)  # Small pause between tests
    
    print_summary(results)
    
    # Generate graphs
    generate_graphs(results)
    
    print("\n💾 Próximo paso: Ejecutar profiling detallado")
    print("    Comando: python3 -m cProfile -s cumulative src/distance_cache.py [estaciones] 2021-2021")

if __name__ == "__main__":
    main()
