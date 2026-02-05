# Instrucciones para Bianca: Visualización con SnakeViz (Sección 2.2.1)

¡Hola Bianca!

Tu misión es transformar los datos crudos del profiling de `cProfile` en una representación visual que nos permita identificar rápidamente las funciones que consumen más tiempo de ejecución. Utilizaremos la herramienta **SnakeViz** para esta tarea.

## Tu Tarea

1.  **Localizar el archivo de perfilado:**
    *   Tus compañeros ya han generado un archivo llamado `profile_io.prof`. Este archivo contiene los resultados del `cProfile` del script `load.py` (sin caché). Debería estar en la raíz del proyecto.

2.  **Iniciar SnakeViz:**
    *   Abre tu terminal en la raíz del proyecto.
    *   Ejecuta el siguiente comando:
        ```bash
        snakeviz profile_io.prof
        ```
    *   Esto iniciará un servidor web local y abrirá automáticamente tu navegador web con la interfaz de SnakeViz.

3.  **Análisis Visual en SnakeViz:**
    *   Dentro de la interfaz de SnakeViz, verás una representación gráfica (normalmente un gráfico de "Icicle" o "Sunburst").
    *   **Identifica las funciones que ocupan la mayor área visual.** Estas son las funciones que más tiempo consumen en la ejecución del programa. Presta especial atención a las funciones relacionadas con operaciones de red (`requests`, `socket`, etc.) que deberían dominar el perfil de `load.py`.

4.  **Captura de Evidencia:**
    *   Toma una captura de pantalla del gráfico interactivo de SnakeViz.
    *   En la captura, asegúrate de resaltar o señalar visualmente la función o las funciones que ocupan la mayor "porción" del tiempo de ejecución. Esto servirá como evidencia de tu análisis.

## ¿Por qué SnakeViz?

`cProfile` nos da datos en bruto (tablas), pero **SnakeViz** nos ayuda a interpretar esos datos de forma intuitiva. Los gráficos de Icicle o Sunburst visualizan la jerarquía de llamadas y el tiempo acumulado de cada función, haciendo muy fácil ver dónde se está gastando la mayor parte del tiempo, lo que es clave para identificar cuellos de botella.

¡Mucha suerte con el análisis!
