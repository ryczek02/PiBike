from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarker
from kivy_garden.mapview.geojson import GeoJsonMapLayer
import csv
from app.config import CONFIG
from app.utils.logger import log
from app.sensors.gps_l76g import GPS

class GPSApp(App):
    def build(self):
        self.gps_sensor = GPS()
        self.layout = BoxLayout(orientation='vertical')
        self.mapview = MapView(zoom=12, lat=0, lon=0)
        self.marker = None

        self.load_button = Button(text="📂 Wczytaj plik GPS")
        self.load_button.bind(on_press=self.load_gps_file)

        self.label = Label(text="Aktualna pozycja: -", size_hint_y=0.1)

        self.layout.add_widget(self.load_button)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.mapview)

        Clock.schedule_interval(self.update_gps_position, CONFIG["SENSOR_DELAY"])

        return self.layout

    def update_gps_position(self, dt):
        try:
            # data = self.gps_sensor.read()
            # lat, lon = data["gps_lat"], data["gps_lon"]
            lat, lon = 50.0, 20.0
            self.label.text = f"Aktualna pozycja: {lat:.5f}, {lon:.5f}"

            if self.marker:
                self.mapview.remove_marker(self.marker)
            self.marker = MapMarker(lat=lat, lon=lon)
            self.mapview.add_marker(self.marker)
            self.mapview.center_on(lat, lon)
        except Exception as e:
            log(f"Błąd aktualizacji pozycji: {e}", level="WARNING")

    def load_gps_file(self, instance):
        filechooser = FileChooserIconView(path="/home/ryczek02")
        filechooser.bind(on_submit=self.on_file_selected)
        self.layout.clear_widgets()
        self.layout.add_widget(filechooser)

    def on_file_selected(self, filechooser, selection, touch):
        if not selection:
            return

        filepath = selection[0]
        self.layout.clear_widgets()
        self.layout.add_widget(self.load_button)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.mapview)

        if filepath.endswith(".csv"):
            self.load_csv_file(filepath)
        elif filepath.endswith(".gpx"):
            self.load_gpx_file(filepath)
            
    def load_csv_file(self, filepath):
        try:
            with open(filepath, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        lat = float(row.get("gps_lat", 0))
                        lon = float(row.get("gps_lon", 0))
                        if lat != 0 and lon != 0:
                            marker = MapMarker(lat=lat, lon=lon)
                            self.mapview.add_marker(marker)
                    except:
                        continue
        except Exception as e:
            log(f"Błąd odczytu pliku CSV: {e}", level="ERROR")

    def load_gpx_file(self, filepath):
        import xml.etree.ElementTree as ET
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            namespace = {'default': 'http://www.topografix.com/GPX/1/1'}
            trkpts = root.findall(".//default:trkpt", namespace)

            coords = [(float(pt.attrib['lon']), float(pt.attrib['lat'])) for pt in trkpts]

            if coords:
                first_lat = coords[0][1]
                first_lon = coords[0][0]
                self.mapview.center_on(first_lat, first_lon)
                self.label.text = "Załadowano trasę z GPX (GeoJSON)"

                # Tworzymy GeoJSON jako Python dict
                geojson_data = {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "LineString",
                                "coordinates": coords
                            },
                            "properties": {
                                "name": "Trasa GPX",
                                "stroke": "#FF0000",
                                "stroke-width": 3
                            }
                        }
                    ]
                }

                self.add_geojson_layer(geojson_data)

        except Exception as e:
            log(f"Błąd odczytu pliku GPX: {e}", level="ERROR")

            
    def add_geojson_layer(self, geojson_data):
        for child in self.mapview.children[:]:
            if isinstance(child, GeoJsonMapLayer):
                self.mapview.remove_widget(child)

        geojson_layer = GeoJsonMapLayer()
        geojson_layer.geojson = geojson_data
        self.mapview.add_widget(geojson_layer)

    def draw_path_line(self, coords):
        from kivy.graphics import Color, Line

        mapview = self.mapview

        # Wyczyszczenie starych linii (jeśli są)
        mapview.canvas.after.clear()

        with mapview.canvas.after:
            Color(1, 0, 0, 1)  # czerwona linia
            points = []
            for lat, lon in coords:
                x, y = mapview.get_window_xy_from(lat, lon, mapview.zoom)
                points.extend([x, y])
            Line(points=points, width=2)



