# Guía Detallada del Proyecto: CA1.U2 - Optimización de Código

¡Hola equipo!

Este documento es nuestra guía central para el proyecto de optimización de código. El objetivo es aplicar las técnicas de profiling vistas para identificar y resolver cuellos de botella en un caso de estudio práctico.

---

## 🚨 ¡MUY IMPORTANTE! 🚨

Antes de empezar, es **fundamental** que todos revisen el material complementario y las instrucciones que el profesor ha subido a **Microsoft Teams**. Puede haber detalles o requisitos adicionales allí que no estén en este documento.

---

## 🎯 FASE 1: Línea Base de Rendimiento

El primer paso es para **Russel**, pero todos deben entenderlo. Necesitamos establecer una línea base para saber cuánto mejoramos. Esto implica ejecutar el código original sin ninguna optimización.

**Scripts a ejecutar:**
1.  `load.py`: Descarga los datos de las estaciones meteorológicas NOAA.
2.  `distance.py`: Calcula las distancias entre estaciones (usando el algoritmo de complejidad n²).

El rendimiento medido en esta fase es nuestro punto de partida.

---

## 👥 Distribución de Tareas y Roles

Este es el reparto oficial del equipo. Cada persona tiene una misión clara. ¡La comunicación es clave!

### 🧑‍💻 **Russel — Configuración y Profiling General (cProfile)**

**Misión:** Eres el punto de partida. Tu rol es asegurar que el entorno funcione para todos y realizar el primer análisis para encontrar los cuellos de botella generales a nivel de funciones.

**Tareas:**
1.  **Instalar dependencias:** Abre una terminal en la raíz del proyecto y ejecuta:
    ```bash
    pip install snakeviz line_profiler requests
    ```
2.  **Ejecutar Scripts Originales:** Corre los scripts `load.py` y `distance.py` sin modificaciones para asegurar que todo funcione.
3.  **Profiling con cProfile:**
    *   Ejecuta el siguiente comando para ver en consola qué funciones consumen más tiempo. Analiza la columna `cumulative`.
        ```bash
        python -m cProfile -s cumulative load.py 01044099999,02293099999 2021-2021
        ```
    *   Guarda los resultados del profiling en un archivo que Rivaldo usará.
        ```bash
        python -m cProfile -o profiling/cprofile/profile.prof load.py 01044099999,02293099999 2021-2021
        ```

**📸 Evidencia que debes entregar a Joni:**
1.  Screenshot de la ejecución normal de los scripts originales.
2.  Screenshot de la tabla de `cProfile` donde se vean claramente las funciones que más tiempo acumulado consumen (ej. `download_data`, `get_all_temperatures`, etc.).

**📝 Observaciones que debes escribir para Joni:**
*   ¿El tiempo de ejecución se concentra más en operaciones de red (IO), de disco (IO) o de cómputo (CPU)?
*   ¿Qué función específica es la que domina el tiempo total de ejecución?

---

### 📊 **Rivaldo — Visualización con SnakeViz**

**Misión:** "Traducir" los datos crudos de cProfile a un formato visual e intuitivo que nos permita entender fácilmente dónde está el problema.

**Tareas:**
1.  Usa el archivo `profile.prof` que generó Russel.
2.  Desde la terminal, en la raíz del proyecto, ejecuta:
    ```bash
    snakeviz profiling/cprofile/profile.prof
    ```
3.  Esto abrirá una visualización en tu navegador. Analiza los gráficos (Sunburst o Icicle).

**📸 Evidencia que debes entregar a Joni:**
1.  Screenshot del gráfico de SnakeViz (Sunburst o Icicle) donde se vea claramente cuál es el bloque de función que más área ocupa.

**📝 Observaciones que debes escribir para Joni:**
*   ¿Cuál es el bloque más grande en el gráfico y qué función representa?
*   Basado en la visualización, ¿el problema principal parece ser la descarga de datos o el cálculo/procesamiento de esos datos?

---

### 🔬 **Bianca — Análisis Detallado con Line Profiler**

**Misión:** Ir un paso más allá del análisis de funciones y encontrar las líneas de código *exactas* que son lentas dentro de las funciones más problemáticas identificadas por Russel y Rivaldo.

**Tareas:**
1.  Identifica la función más costosa (probablemente `get_distance()` en `distance.py` o una similar).
2.  Copia el script original (ej. `distance.py`) a `profiling/line_profiler/distance_cache.py` y modifícalo para añadir el decorador `@profile` encima de la función que quieres analizar.
    ```python
    # En distance_cache.py
    # No olvides importar el decorador si es necesario, aunque kernprof lo inyecta.

    @profile
    def get_distance(station1, station2):
        # ... código de la función ...
    ```
3.  Ejecuta `kernprof` para generar el archivo de análisis:
    ```bash
    kernprof -l profiling/line_profiler/distance_cache.py
    ```
4.  Muestra los resultados del análisis en la consola:
    ```bash
    python -m line_profiler profiling/line_profiler/distance_cache.py.lprof
    ```

**📸 Evidencia que debes entregar a Joni:**
1.  Screenshot de la salida de `line_profiler` donde se vean las columnas: `Line #`, `Hits`, `Time`, `Per Hit`, `% Time`.

**📝 Observaciones que debes escribir para Joni:**
*   ¿Qué líneas de código específicas consumen el mayor porcentaje de tiempo?
*   ¿Qué operaciones (matemáticas, de asignación, etc.) son las más costosas?
*   ¿Hay líneas que se ejecutan una cantidad excesiva de veces (alto número de `Hits`)?

---

### 🧠 **Rama — Optimización con Estructuras de Datos**

**Misión:** Aplicar optimizaciones prácticas usando estructuras de datos más eficientes (como `sets` o `dicts` en lugar de `lists`) basadas en los hallazgos del profiling.

**Tareas:**
1.  Busca en el código original un lugar donde se realicen búsquedas repetitivas sobre una lista (ej. `if item in my_list:`).
2.  Modifica el código para usar una estructura más adecuada, como un `set`, para acelerar esas búsquedas.
3.  Mide y compara el tiempo de ejecución antes y después del cambio. Puedes usar `%timeit` en un notebook o simplemente medir el tiempo de ejecución del script.

**📸 Evidencia que debes entregar a Joni:**
1.  Screenshot o dato del tiempo de ejecución **antes** del cambio (con la lista).
2.  Screenshot o dato del tiempo de ejecución **después** del cambio (con el set).
3.  El fragmento de código modificado (`antes` y `después`).

**📝 Observaciones que debes escribir para Joni:**
*   ¿Cuánto mejoró el rendimiento (en porcentaje o en segundos)?
*   Explica brevemente *por qué* un `set` es más rápido para búsquedas que una `list` (pista: tiene que ver con el hashing y O(1) vs O(n)).

---

### 🧮 **Edgardo — Optimización de Uso de Memoria**

**Misión:** Demostrar cómo una elección incorrecta de tipos de datos puede malgastar memoria y cómo solucionarlo.

**Tareas:**
1.  Crea un script de prueba donde leas el contenido de un archivo grande de dos maneras:
    *   **Versión ineficiente:** `content_list = list(f.read())`
    *   **Versión eficiente:** `content_bytes = f.read()`
2.  Usa el módulo `sys` para medir el tamaño en memoria de los objetos resultantes.
    ```python
    import sys
    # ... leer archivo ...
    print(f"Tamaño del objeto (lista): {sys.getsizeof(content_list)} bytes")
    print(f"Tamaño del objeto (bytes): {sys.getsizeof(content_bytes)} bytes")
    ```

**📸 Evidencia que debes entregar a Joni:**
1.  Screenshot mostrando el tamaño en memoria del objeto `list`.
2.  Screenshot mostrando el tamaño en memoria del objeto `bytes`.
3.  Una captura donde se vea la diferencia abismal entre ambos.

**📝 Observaciones que debes escribir para Joni:**
*   Explica el concepto de "overhead" de los objetos en Python (por qué cada número en la lista ocupa más memoria que solo el valor).
*   Explica por qué la cadena de `bytes` es mucho más compacta y eficiente en memoria.

---

### 💤 **Papudex — Generadores y Evaluación Perezosa (Lazy Evaluation)**

**Misión:** Ilustrar el poder de los generadores (`yield`) para procesar grandes volúmenes de datos sin consumir toda la memoria RAM.

**Tareas:**
1.  Busca una función en el código original que devuelva una lista grande de resultados (ej. `get_all_temperatures`).
2.  Crea dos versiones de esa función:
    *   **Versión original:** `def get_temps_list(...): return [...]`
    *   **Versión con generador:** `def get_temps_gen(...): for item in data: yield item`
3.  Compara el tamaño en memoria de lo que devuelve cada función.
    ```python
    import sys
    lista_temps = get_temps_list(...)
    gen_temps = get_temps_gen(...)
    print(f"Tamaño de la lista: {sys.getsizeof(lista_temps)} bytes")
    print(f"Tamaño del generador: {sys.getsizeof(gen_temps)} bytes")
    ```

**📸 Evidencia que debes entregar a Joni:**
1.  Screenshot mostrando el tamaño en memoria de la **lista** completa.
2.  Screenshot mostrando el tamaño en memoria del **objeto generador**.

**📝 Observaciones que debes escribir para Joni:**
*   Explica por qué el generador usa una cantidad de memoria tan pequeña y constante.
*  Describe el concepto de "evaluación perezosa" (lazy evaluation): los datos se procesan uno por uno, solo cuando se necesitan.
*   Menciona en qué escenarios es más útil usar generadores (ej. archivos muy grandes, streams de datos).

---

## ✍️ **Joni — Documentación y Consolidación del Reporte**

**Misión:** Eres el arquitecto de la información. Tu trabajo es recopilar los hallazgos de todos y ensamblarlos en un reporte técnico final que sea claro, profesional y siga la estructura requerida. **No haces pruebas técnicas**, te enfocas 100% en la calidad del documento.

**Tareas:**
1.  Crear el archivo `report/CA1_U2_Technical_Report.md`.
2.  Recopilar todas las capturas de pantalla y observaciones de Russel, Rivaldo, Bianca, Rama, Edgardo y Papudex.
3.  Organizar toda la información en el `report.md` siguiendo la estructura definida a continuación.
4.  Asegurarte de que el formato sea impecable: títulos, secciones, bloques de código bien indentados, e inserción correcta de las imágenes.

---

## 🔄 Flujo de Trabajo Recomendado

1.  **Del 1 al 6 (Russel a Papudex):** Cada uno realiza su parte asignada y guarda sus capturas de pantalla y notas.
2.  **Cada uno escribe un resumen:** Un texto breve (media página aprox.) explicando qué hizo, qué encontró y qué conclusiones sacó.
3.  **Todos envían su material a Joni:** Le mandan las capturas y el texto resumen.
4.  **Joni:** Consolida todo en el `report/CA1_U2_Technical_Report.md` final, dándole formato y coherencia.

---

## 📑 Estructura del Reporte Técnico Final (para Joni)

El archivo `report/CA1_U2_Technical_Report.md` debe seguir esta estructura:

\`\`\`markdown
# CA1.U2 – Code Optimization Report

## Introducción
- Objetivo del proyecto: optimizar el rendimiento de un caso de estudio usando técnicas de profiling.
- Breve descripción del problema (código lento).

## Metodología
- Herramientas utilizadas (cProfile, SnakeViz, line_profiler).
- Breve explicación de para qué sirve cada una.

## Resultados: Análisis de Rendimiento
### Antes de Optimizar (Línea Base)
- Incluir las capturas de Russel (cProfile) y Rivaldo (SnakeViz).
- Incluir las capturas de Bianca (line_profiler).
- Resumir los hallazgos: identificar los cuellos de botella principales (CPU vs IO, funciones y líneas específicas).

### Optimización Aplicada y Resultados
#### 1. Optimización con Estructuras de Datos (Aporte de Rama)
- Explicar el cambio de `list` a `set`.
- Mostrar evidencia del "antes" y "después" en rendimiento.

#### 2. Optimización de Uso de Memoria (Aporte de Edgardo)
- Explicar la comparación entre `list` de enteros y `bytes`.
- Mostrar la evidencia del ahorro de memoria.

#### 3. Optimización con Generadores (Aporte de Papudex)
- Explicar el cambio a `yield`.
- Mostrar la evidencia de la reducción drástica en el uso de memoria.

## Observaciones Generales
- ¿Qué optimización tuvo el mayor impacto en el rendimiento/memoria?
- ¿Qué optimización tuvo un impacto menor?
- ¿Cuál era el tipo de cuello de botella principal en este caso de estudio (CPU, IO, memoria)?

## Conclusiones
- Resaltar la importancia del profiling para evitar la "optimización prematura" (adivinar dónde está el problema).
- Concluir cómo pequeños cambios (ej. en estructuras de datos) pueden tener un gran impacto.
- Reflexión final del equipo.
\`\`\`
