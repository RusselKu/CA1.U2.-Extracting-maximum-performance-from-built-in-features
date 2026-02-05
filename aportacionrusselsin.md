# Aportación de Russel: Configuración y Línea Base (Sección 2.1.1)

¡Hola equipo! Aquí os dejo un resumen de las tareas completadas en la fase de "Configuración y Línea Base", junto con una pequeña guía para asegurar una transición fluida a vuestras próximas etapas.

## Resumen de Tareas Completadas por Russel

### 1. Instalación de Dependencias
Se han instalado las dependencias necesarias (`snakeviz`, `line_profiler`, `requests`) en el entorno del proyecto.

**Problema encontrado:** Inicialmente, los archivos `.py` en `src/` estaban vacíos, lo que impedía la ejecución directa del script `load.py`.
**Solución:** Se transcribió el código de `load.py` directamente desde las páginas 3 y 4 del "Chapter 2. Profiling.pdf" al archivo `src/load.py`.

### 2. Ejecución y Verificación del Script `load.py`
Se ejecutó el script `src/load.py` para verificar que descarga los datos climáticos de la NOAA.

**Problema encontrado:** Los IDs de estación y el año especificados en la instrucción original (`01044099999,02293099999 2021-2021`) y en el PDF (`01494099999`) resultaron en errores `404 Not Found` al intentar descargar los datos del servidor de la NOAA. Esto indicaba que las URLs no eran válidas o los datos no estaban disponibles para esos parámetros.
**Solución:** Tras una investigación (búsqueda web y análisis de `isd-history.txt`), se encontró un ID de estación y año que funcionan correctamente: `72403093738` para el año `2019`.
**Ejecución de verificación exitosa:**
```bash
python src/load.py 72403093738 2019-2019
```
**Output de verificación:**
```
Attempting to download from URL: https://www.ncei.noaa.gov/data/global-hourly/access/2019/72403093738.csv
Status code for https://www.ncei.noaa.gov/data/global-hourly/access/2019/72403093738.csv: 200
Writing to file: station_72403093738_2019.csv
{'72403093738': -15.0}
```
*Nota: Se eliminaron los `print` de depuración una vez verificada la funcionalidad.*

### 3. Profiling General con `cProfile`
Se realizó el primer profiling general del script `load.py` utilizando `cProfile` con los parámetros funcionales.

**Comando ejecutado:**
```bash
python -m cProfile -s cumulative src/load.py 72403093738 2019-2019
```

**Evidencia: Tabla de `cProfile` (columnas `cumulative` resaltadas)**

```
         256829 function calls (252110 primitive calls) in 2.542 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    146/1    0.001    0.000    2.542    2.542 {built-in method builtins.exec}
        1    0.000    0.000    2.542    2.542 load.py:1(<module>)
        1    0.001    0.001    2.207    2.207 load.py:24(download_all_data)
        1    0.000    0.000    2.206    2.206 load.py:15(download_data)
        1    0.000    0.000    2.168    2.168 api.py:62(get)
        1    0.000    0.000    2.168    2.168 api.py:14(request)
        1    0.000    0.000    2.168    0.000    2.168 sessions.py:500(request)
        1    0.000    0.000    2.166    2.166 sessions.py:673(send)
     1587    0.002    0.000    1.533    0.001 socket.py:706(readinto)
     1587    0.003    0.000    1.529    0.001 ssl.py:1289(recv_into)
     1587    0.001    0.000    1.526    0.001 ssl.py:1129(read)
     1587    1.524    0.001    1.524    0.001 {method 'read' of '_ssl._SSLSocket' objects}
... (se muestra solo la parte superior, el resto del output es muy extenso)
```
**Observación:** Como era de esperar, las operaciones de descarga de datos (`download_all_data`, `download_data` y las funciones subyacentes de red) consumen la mayor parte del tiempo acumulado, indicando un cuello de botella de I/O.

## Guía para el Resto del Equipo

Para continuar con vuestras tareas, es **fundamental** que cada uno siga estos pasos para configurar su entorno:

1.  **Crear y Activar el Entorno Virtual:**
    Aseguraos de tener un entorno virtual aislado para vuestro trabajo.
    ```bash
    python -m venv .venv
    # Para activar en Windows (PowerShell):
    & .\.venv\Scripts\Activate.ps1
    # Para activar en Windows (Command Prompt):
    # .venv\Scripts\activate.bat
    # Para activar en Linux/macOS:
    # source .venv/bin/activate
    ```
2.  **Instalar Dependencias:**
    Una vez activado el entorno, instalad todas las librerías necesarias desde `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Archivos Python:**
    Los archivos Python en `src/` ya contienen el código transcrito del libro. No es necesario reescribirlos.
    *   **`src/load.py`:** Contiene la lógica para descargar y procesar datos, utilizando el ID de estación `72403093738` y el año `2019`.

¡Mucha suerte con vuestras próximas fases de profiling y optimización!
