# GeoMap: Photo Geolocation Heatmap Generator

This script analyzes a directory of photos, extracts GPS coordinates from their EXIF metadata, and generates an interactive heatmap and a statistical PDF report based on the locations where the photos were taken.

## Features

-	**Interactive Heatmap:** Generates an HTML file (`heatmap.html`) with a world map displaying photo locations.
-	**Clustered Markers:** Individual markers for each photo are grouped into clusters for better visualization. Clicking on a marker shows the date, filename, and city.
-	**Geolocation Analysis:** Uses `geopy` to reverse-geocode coordinates and identify the city where each photo was taken.
-	**Statistical PDF Report:** Creates a PDF file (`estadisticas_fotos.pdf`) with:
    -	A summary of total photos analyzed vs. photos with GPS data.
    -	A Top 10 list of the most frequent photo locations (cities).
    -	A chronological list of all geolocated photos.
-	**Error Logging:** Records any issues encountered during processing (e.g., missing GPS data) in `errores_log.txt`.
-	**Broad File Support:** Processes a wide range of image and video file types.

## Requirements

You need to install the following Python libraries:

```bash
pip install folium exifread geopy reportlab
```

## Usage

1.	**Set the Photo Directory:**
    Open the `GeoMap.py` script and find the following section at the end of the file:

    ```python
    if __name__ == "__main__":
        # IMPORTANTE: Modifica la siguiente línea para indicar la ruta a tu carpeta de fotos.
        # Puede ser una ruta local (ej. "C:/Users/TuUsuario/Pictures") o de red (ej. r"\\servidor\fotos").
        photo_dir = r"\\DS1522\homes\marc\Photos"
    ```
    
    Change the `photo_dir` variable to point to the directory containing your photos.

2.	**Run the script:**
    Execute the script from your terminal:
    ```bash
    python GeoMap.py
    ```

3.	**View the Output:**
    The script will generate the following files in the same directory:
    -	`heatmap.html`: An interactive map that will open automatically in your web browser.
    -	`estadisticas_fotos.pdf`: A PDF document with statistics.
    -	`errores_log.txt`: A log file with details of any processing errors.

---

# GeoMap: Generador de Mapa de Calor de Geolocalización de Fotos

Este script analiza un directorio de fotografías, extrae las coordenadas GPS de sus metadatos EXIF y genera un mapa de calor interactivo y un informe estadístico en PDF basados en las ubicaciones donde se tomaron las fotos.

## Características

-	**Mapa de Calor Interactivo:** Genera un archivo HTML (`heatmap.html`) con un mapa del mundo que muestra las ubicaciones de las fotos.
-	**Marcadores Agrupados:** Los marcadores individuales de cada foto se agrupan en clústeres para una mejor visualización. Al hacer clic en un marcador, se muestra la fecha, el nombre del archivo y la ciudad.
-	**Análisis de Geolocalización:** Utiliza `geopy` para realizar geocodificación inversa de las coordenadas e identificar la ciudad donde se tomó cada foto.
-	**Informe Estadístico en PDF:** Crea un archivo PDF (`estadisticas_fotos.pdf`) con:
    -	Un resumen del total de fotos analizadas frente a las fotos con datos GPS.
    -	Un Top 10 de las ubicaciones (ciudades) más frecuentes.
    -	Un listado cronológico de todas las fotos geolocalizadas.
-	**Registro de Errores:** Guarda cualquier problema encontrado durante el procesamiento (por ejemplo, datos GPS ausentes) en `errores_log.txt`.
-	**Amplio Soporte de Archivos:** Procesa una gran variedad de tipos de archivos de imagen y vídeo.

## Requisitos

Necesitas instalar las siguientes librerías de Python:

```bash
pip install folium exifread geopy reportlab
```

## Uso

1.	**Establecer el Directorio de Fotos:**
    Abre el script `GeoMap.py` y busca la siguiente sección al final del archivo:

    ```python
    if __name__ == "__main__":
        # IMPORTANTE: Modifica la siguiente línea para indicar la ruta a tu carpeta de fotos.
        # Puede ser una ruta local (ej. "C:/Users/TuUsuario/Pictures") o de red (ej. r"\\servidor\fotos").
        photo_dir = r"\\DS1522\homes\marc\Photos"
    ```
    
    Cambia la variable `photo_dir` para que apunte al directorio que contiene tus fotos.

2.	**Ejecutar el script:**
    Ejecuta el script desde tu terminal:
    ```bash
    python GeoMap.py
    ```

3.	**Ver los Resultados:**
    El script generará los siguientes archivos en el mismo directorio:
    -	`heatmap.html`: Un mapa interactivo que se abrirá automáticamente en tu navegador web.
    -	`estadisticas_fotos.pdf`: Un documento PDF con las estadísticas.
    -	`errores_log.txt`: Un archivo de registro con los detalles de los errores de procesamiento.
