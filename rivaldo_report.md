# Reporte de Rivaldo: Análisis de Latencia de Red e I/O y Optimización con Caché

Este reporte detalla las tareas realizadas por Rivaldo, enfocadas en el análisis del impacto de las operaciones de red en el rendimiento del script `load.py` y la demostración de la efectividad de una estrategia de caché local.

## Objetivo

La misión principal de Rivaldo era analizar la latencia de red y el impacto de las operaciones de I/O en el rendimiento del programa, así como demostrar cómo una estrategia de caché local puede mejorar significativamente los tiempos de ejecución.

## Problema Identificado y Resolución

Durante la fase inicial de ejecución y perfilado del script `load.py`, se identificó un problema crítico: los IDs de estación proporcionados en los argumentos de línea de comandos (`01044099999,02293099999`) estaban causando errores `404 Not Found` al intentar descargar los archivos CSV de la NOAA. La depuración reveló que el problema radicaba en que los ceros iniciales de los IDs de estación se eliminaban durante el procesamiento de los argumentos del script, lo que resultaba en URLs incorrectas (e.g., `1044099999` en lugar de `01044099999`).

**Solución Implementada:**
Se modificó la lógica de procesamiento de los IDs de estación en ambos scripts (`src/load.py` y `src/load_cache.py`) para asegurar que todos los IDs sean tratados como cadenas y se rellenen con ceros iniciales hasta alcanzar una longitud de 11 caracteres (ej: `s.zfill(11)`). Esta corrección garantizó que las URLs se formaran correctamente, permitiendo la descarga exitosa de los datos.

## Comparativa de Tiempos de Ejecución

Se realizaron mediciones de tiempo de ejecución para el script original (`load.py`) y la versión con caché (`load_cache.py`) para demostrar el impacto de la caché local. Los datos se obtuvieron utilizando los IDs de estación `01044099999,02293099999` para el año `2021`.

| Escenario                                           | Tiempo de Ejecución (segundos) | Observaciones                                                                          |
| :-------------------------------------------------- | :----------------------------- | :------------------------------------------------------------------------------------- |
| `load.py` (sin caché - descarga siempre)            | **16.273**                     | Muestra el rendimiento cuando todas las operaciones de I/O de red son necesarias.      |
| `load_cache.py` (primera ejecución - descarga y cachea) | **6.520**                      | La ejecución inicial llena el caché local. Es más rápida que `load.py` sin caché.     |
| `load_cache.py` (segunda ejecución - usa caché local) | **0.932**                      | Demuestra la mejora drástica al leer los datos directamente del disco local (caché). |

## Conclusión

La comparativa de tiempos de ejecución resalta claramente que la **E/S de red** es el principal cuello de botella en el script original. La implementación de una estrategia de caché local en `load_cache.py` resultó en una **mejora de rendimiento de más de un orden de magnitud** en las ejecuciones subsiguientes (de 16.273 segundos a 0.932 segundos).

Este cambio traslada el principal punto de contención de la red al **acceso a disco local**, que es significativamente más rápido y predecible.

## Archivo de Profiling Generado

Para las próximas etapas del proyecto, se ha generado el archivo de perfilado `profile_io.prof` para el script `load.py` utilizando `cProfile`. Este archivo está listo para ser utilizado por Bianca para la visualización con SnakeViz.
