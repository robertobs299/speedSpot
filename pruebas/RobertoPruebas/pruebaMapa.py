from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.bubble import Bubble
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.lang import Builder

def change_marker(map_view, lat, lon, text):
    # Crear un nuevo MapMarkerPopup
    marker = MapMarkerPopup(lat=lat, lon=lon)

    # Crear un Bubble para el popup del marcador
    bubble = Bubble()

    # Crear un BoxLayout para el contenido del popup
    box_layout = MDBoxLayout(padding="4dp")

    # Crear un Label para el texto del popup
    label = MDLabel(text=text, markup=True, halign="center")

    # Añadir el Label al BoxLayout
    box_layout.add_widget(label)

    # Añadir el BoxLayout al Bubble
    bubble.add_widget(box_layout)

    # Añadir el Bubble al MapMarkerPopup
    marker.add_widget(bubble)

    # Añadir el MapMarkerPopup al MapView
    map_view.add_widget(marker)

    return marker


class ClickableMapView(MapView):
    current_marker = None

    def on_touch_down(self, touch):
        # Si el toque ocurre dentro del MapView y es un doble clic
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            # Convertir las coordenadas del toque a coordenadas de latitud y longitud
            touch_lat, touch_lon = self.get_latlon_at(*touch.pos)

            # Si ya hay un marcador, eliminarlo
            if self.current_marker:
                self.remove_widget(self.current_marker)

            # Agregar un marcador en las coordenadas del toque
            self.current_marker = change_marker(self, touch_lat, touch_lon, "You clicked here")
            return True
        # Si el toque ocurre fuera del MapView o no es un doble clic, devolver el resultado de super().on_touch_down(touch)
        return super().on_touch_down(touch)

KV = """
#:import MapSource kivy_garden.mapview.MapSource

MDRelativeLayout:
 ClickableMapView:
  id: map_view
  lat:50.6
  lon:3.05
  zoom:13
"""

class MyApp(MDApp):
 def build(self):
  return Builder.load_string(KV)

MyApp().run()