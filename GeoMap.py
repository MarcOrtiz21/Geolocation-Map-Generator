import os
import glob
import exifread
import folium
from folium.plugins import HeatMap, MarkerCluster
import webbrowser
from datetime import datetime
from collections import Counter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def get_decimal_coords(tags):
    def convert_to_degrees(value):
        d, m, s = value.values
        return float(d.num) / float(d.den) + (float(m.num) / float(m.den) / 60.0) + (float(s.num) / float(s.den) / 3600.0)
    
    if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
        lat = convert_to_degrees(tags['GPS GPSLatitude'])
        lon = convert_to_degrees(tags['GPS GPSLongitude'])
        
        if tags['GPS GPSLatitudeRef'].values[0] != 'N':
            lat = -lat
        if tags['GPS GPSLongitudeRef'].values[0] != 'E':
            lon = -lon
        
        return lat, lon
    return None

def get_exif_date(tags):
    date_tag = 'EXIF DateTimeOriginal'
    if date_tag in tags:
        return str(tags[date_tag])
    return 'Fecha desconocida'

def get_location_name(lat, lon, geolocator):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, language='es')
        return location.raw.get('address', {}).get('city', 'Ubicación desconocida')
    except:
        return "No se pudo determinar la ciudad"

def extract_photo_data(photo_dir):
    geolocator = Nominatim(user_agent="photo_mapper_app")
    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

    extensions = [
        "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.heic",
        "*.heif", "*.dng", "*.raw", "*.cr2", "*.nef", "*.arw", "*.orf",
        "*.sr2", "*.mov", "*.mp4", "*.m4v", "*.3gp"
    ]
    
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(photo_dir, "**", ext.lower()), recursive=True))
        image_files.extend(glob.glob(os.path.join(photo_dir, "**", ext.upper()), recursive=True))
        
    image_files = list(set(image_files))
    locations_data = []
    errors = []

    print(f"Procesando {len(image_files)} imágenes. Esto puede tardar...")

    for i, image in enumerate(image_files):
        print(f"  > Procesando imagen {i+1}/{len(image_files)}: {os.path.basename(image)}")
        try:
            with open(image, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                coords = get_decimal_coords(tags)
                if coords:
                    date = get_exif_date(tags)
                    city = get_location_name(coords[0], coords[1], geolocator)
                    locations_data.append({'lat': coords[0], 'lon': coords[1], 'date': date, 'filename': os.path.basename(image), 'city': city})
                else:
                    errors.append((os.path.basename(image), "Sin datos GPS"))
        except Exception as e:
            errors.append((os.path.basename(image), str(e)))

    with open('errores_log.txt', 'w') as log_file:
        for error in errors:
            log_file.write(f"{error[0]} - Error: {error[1]}\n")

    return locations_data, len(image_files), len(errors)

def generate_heatmap(locations, output_file="heatmap.html"):
    if not locations:
        print("No se encontraron ubicaciones GPS en las fotos.")
        return

    avg_lat = sum(loc['lat'] for loc in locations) / len(locations)
    avg_lon = sum(loc['lon'] for loc in locations) / len(locations)

    map_ = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(map_)

    for loc in locations:
        popup_info = f"Fecha: {loc['date']}<br>Archivo: {loc['filename']}<br>Ciudad: {loc['city']}"
        folium.Marker([loc['lat'], loc['lon']], popup=popup_info).add_to(marker_cluster)

    heat_data = [[loc['lat'], loc['lon']] for loc in locations]
    HeatMap(heat_data, radius=15).add_to(map_)

    map_.save(output_file)
    print(f"\nMapa de calor guardado en {output_file}")
    webbrowser.open(output_file)

def generate_pdf_report(locations, total_files, errors_count, output_file="estadisticas_fotos.pdf"):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(inch, height - inch, "Informe Estadístico de Fotografías")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, height - 1.5 * inch, "Resumen General")
    c.setFont("Helvetica", 12)
    c.drawString(inch, height - 1.8 * inch, f"Total de imágenes analizadas: {total_files}")
    c.drawString(inch, height - 2.0 * inch, f"Imágenes con datos GPS: {len(locations)}")
    c.drawString(inch, height - 2.2 * inch, f"Imágenes sin datos GPS o con errores: {errors_count}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, height - 2.7 * inch, "Top 10 Ubicaciones Más Frecuentes")
    city_counts = Counter(loc['city'] for loc in locations if loc['city'] != "Ubicación desconocida")
    
    c.setFont("Helvetica", 12)
    y_position = height - 3.0 * inch
    for i, (city, count) in enumerate(city_counts.most_common(10)):
        c.drawString(inch, y_position, f"{i+1}. {city}: {count} fotos")
        y_position -= 0.25 * inch
        if y_position < inch:
            c.showPage()
            y_position = height - inch

    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, height - inch, "Listado Cronológico de Fotos")
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(inch, height - 1.3 * inch, "Fecha y Hora")
    c.drawString(4 * inch, height - 1.3 * inch, "Ubicación (Ciudad)")
    c.setFont("Helvetica", 9)
    
    y_position = height - 1.5 * inch
    locations_sorted = sorted(locations, key=lambda x: x['date'])

    for loc in locations_sorted:
        c.drawString(inch, y_position, loc['date'])
        c.drawString(4 * inch, y_position, loc['city'])
        y_position -= 0.20 * inch
        if y_position < inch:
            c.showPage()
            c.setFont("Helvetica-Bold", 14)
            c.drawString(inch, height - inch, "Listado Cronológico (cont.)")
            c.setFont("Helvetica-Bold", 10)
            c.drawString(inch, height - 1.3 * inch, "Fecha y Hora")
            c.drawString(4 * inch, height - 1.3 * inch, "Ubicación (Ciudad)")
            c.setFont("Helvetica", 9)
            y_position = height - 1.5 * inch
            
    c.save()
    print(f"Informe PDF guardado en {output_file}")

if __name__ == "__main__":
    # IMPORTANTE: Modifica la siguiente línea para indicar la ruta a tu carpeta de fotos.
    # Puede ser una ruta local (ej. "C:/Users/TuUsuario/Pictures") o de red (ej. r"\\servidor\fotos").
    photo_dir = r"\\DS1522\homes\marc\Photos"

    if not os.path.isdir(photo_dir):
        print(f"Error: La ruta de red '{photo_dir}' no es accesible o no existe.")
        print("Asegúrate de que estás conectado a la red y la ruta es correcta.")
    else:
        locations, total_files, errors_count = extract_photo_data(photo_dir)
        
        if locations:
            generate_heatmap(locations)
            generate_pdf_report(locations, total_files, errors_count)
        else:
            print("\nFinalizado. No se encontraron fotos con datos GPS para generar el mapa o el informe.")
