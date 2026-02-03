# Guía del Proyecto: CA1.U2 - Profiling de Aplicaciones (Secciones 2.1 y 2.2)

¡Hola equipo! Esta es nuestra guía actualizada. Nos enfocaremos exclusivamente en **identificar cuellos de botella** de Entrada/Salida (IO) y de Procesamiento (CPU) usando las herramientas profesionales de profiling de Python.

---

## 🎯 OBJETIVO
Completar el análisis de rendimiento del sistema de datos climáticos de la NOAA, identificando por qué el código es lento y dónde se pierde tiempo exactamente.

---

## 👥 Roles y Tareas del Equipo

### 🧑‍💻 Russel — Configuración y Línea Base (Sección 2.1.1)
**Misión:** Establecer el punto de partida y asegurar que el entorno sea funcional.
- **Tareas:**
  1. Instalar dependencias: `pip install snakeviz line_profiler requests`.
  2. Ejecutar el script original `load.py` para verificar que descarga los datos.
  3. Realizar el primer profiling general con:
     `python -m cProfile -s cumulative load.py 01044099999,02293099999 2021-2021`
- **Evidencia:** Captura de la tabla de `cProfile` en consola, resaltando la columna `cumulative`.

### 📊 Rivaldo — Análisis de Latencia de Red e IO (Sección 2.1.2)
**Misión:** Analizar el impacto de las operaciones de red en el rendimiento.
- **Tareas:**
  1. Ejecutar el script `load_cache.py` (proporcionado en el material) para comparar el tiempo de ejecución con y sin caché.
  2. Generar el archivo de profiling: 
     `python -m cProfile -o profile_io.prof load.py 01044099999,02293099999 2021-2021`
- **Evidencia:** Comparativa de tiempos (segundos) entre la versión que descarga siempre y la versión que usa caché local.

### 🍦 Bianca — Visualización con SnakeViz (Sección 2.2.1)
**Misión:** Traducir los datos crudos a una estructura visual para identificar jerarquías de llamadas.
- **Tareas:**
  1. Usar el archivo `.prof` generado por sus compañeros.
  2. Ejecutar `snakeviz profile_io.prof`.
  3. Identificar en el gráfico (Icicle o Sunburst) qué funciones ocupan la mayor área visual.
- **Evidencia:** Captura de pantalla del gráfico interactivo de SnakeViz detallando el "ancho" de la función más costosa.

### 🔬 Rama — Profiling de CPU a Nivel de Línea (Sección 2.2.2)
**Misión:** Encontrar la línea exacta de código que frena el cálculo de distancias.
- **Tareas:**
  1. Tomar el script `distance_cache.py`.
  2. Añadir el decorador `@profile` a la función `get_distance`.
  3. Ejecutar: `kernprof -l distance_cache.py` y luego visualizar con:
     `python -m line_profiler distance_cache.py.lprof`
- **Evidencia:** Captura de la tabla de `line_profiler` mostrando el `% Time` de cada línea de la función.

### 🧮 Edgardo y Papudex — Análisis de Complejidad y Comparativa
**Misión:** Determinar el impacto del crecimiento de los datos en el tiempo de CPU.
- **Tareas:**
  1. Ejecutar el script de distancias con un set pequeño de estaciones y luego con uno más grande.
  2. Documentar cómo el tiempo aumenta de forma no lineal (debido a la complejidad $n^2$ mencionada en el libro).
- **Evidencia:** Tabla comparativa: "N° Estaciones vs Tiempo Total de Ejecución".

### ✍️ Joni — Documentación y Consolidación (Technical Report)
**Misión:** Unificar los hallazgos en el reporte final para entrega.
- **Tareas:** Recopilar todas las capturas y notas de los demás. Estructurar el reporte final siguiendo las secciones 2.1 y 2.2 del libro.

---

## 📑 Estructura del Reporte Final (para Joni)

1. **Introducción:** Resumen del problema de datos climáticos de la NOAA.
2. **Profiling de IO (Sección 2.1):**
   - Resultados de `cProfile`.
   - Explicación de cómo el caché mitiga el cuello de botella de la red.
3. **Profiling de CPU (Sección 2.2):**
   - Visualización de SnakeViz (análisis macro).
   - Resultados de `line_profiler` (análisis micro de `get_distance`).
4. **Conclusión:** Resumen de por qué el profiling es vital antes de intentar optimizar a ciegas.