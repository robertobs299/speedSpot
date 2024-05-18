from kivy.lang import Builder
from kivy.uix.bubble import Bubble
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

from pruebas.RobertoPruebas import conexion


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
        if self.collide_point(*touch.pos):
            # Desactivar el desplazamiento del ScrollView
            self.parent.scroll_enabled = False
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


    def on_touch_up(self, touch):
        # Reactivar el desplazamiento del ScrollView
        self.parent.scroll_enabled = True
        return super().on_touch_up(touch)

KV = '''
BoxLayout:
    orientation: "vertical"

    MDLabel:
        text: "Crear Quedada"
        theme_text_color: "Primary"
        halign: "center"
        font_style: "H5"
        size_hint_y: 0.1

    ScrollView:
        scroll_enabled: True
        size_hint_y: 0.9
        bar_width: '10dp'
        BoxLayout:
            orientation: "vertical"
            padding: "10dp"
            spacing: "2dp"

            MDTextField:
                id: nombre
                hint_text: "Nombre de la quedada"
                mode: "rectangle"
                size_hint_y: 0.1

            MDTextField:
                id: descripcion
                hint_text: "Descripción"
                mode: "rectangle"
                multiline: True
                size_hint_y: 0.2

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "2dp"
                size_hint_y: 0.1

                MDRaisedButton:
                    id: fecha
                    text: "Fecha"
                    on_release: app.show_date_picker()

                MDRaisedButton:
                    id: hora
                    text: "Hora"
                    on_release: app.show_time_picker()

            MDTextField:
                id: max_personas
                hint_text: "Cantidad de personas"
                mode: "rectangle"
                input_type: "number"
                size_hint_y: 0.1

            MDTextField:
                id: direccion
                hint_text: "Dirección"
                mode: "rectangle"
                multiline: True
                size_hint_y: 0.1

            MDRelativeLayout:
                size_hint_y: 0.4
                ClickableMapView:
                    id: map_view
                    lat:50.6
                    lon:3.05
                    zoom:13
                    size_hint: 1, 1
                    size: self.parent.size

            MDRaisedButton:
                text: "Crear Quedada"
                pos_hint: {"center_x": 0.5}
                on_release: app.create_meetup()
                size_hint_y: 0.1
                on_release: app.create_meetup()
'''


def insertarCoordenadas(latitud, longitud):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Coordenadas (latitud, longitud) VALUES (%s, %s)", (latitud, longitud))
def crear_quedada(nombre, descripcion, fecha, hora, max_personas,idCoordenadas):

    #AL iniciar sesion habria que guardar los datos del usuario en alguna variable para poder hacer consultas posteriormente
    id_user = 1
    conn = conexion.connect_to_database()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Quedada (user_organiza, descripcion, fecha, hora, max_personas,coordenadas) VALUES (%s,%s, %s, %s, %s, %s, %s)", (id_user,nombre, descripcion, fecha, hora, max_personas,idCoordenadas))


class MainApp(MDApp):
    fecha = ""
    hora = ""
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        return Builder.load_string(KV)

    def show_time_picker(self):
        time_picker = MDTimePicker()
        time_picker.bind(on_save=self.on_time_save, on_cancel=self.on_time_cancel)
        time_picker.open()

    def on_time_save(self, instance, value):
        print(f"The selected time is: {value}")
        self.hora = value

    def on_time_cancel(self, instance, value):
        print("Time selection has been cancelled")
    def show_date_picker(self):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_date_save, on_cancel=self.on_date_cancel)
        date_picker.open()

    def on_date_save(self, instance, value, date_range):
        print(f"La fecha seleccionada es: {value}")
        self.fecha = value

    def on_date_cancel(self, instance, value):
        print("La selección de fecha ha sido cancelada")

    def create_meetup(self):
        nombre = self.root.ids.nombre.text
        descripcion = self.root.ids.descripcion.text
        max_personas = self.root.ids.max_personas.text
        direccion = self.root.ids.direccion.text
        latitud = self.root.ids.map_view.lat
        longitud = self.root.ids.map_view.lon
        insertarCoordenadas(latitud, longitud)

        print(f"Nombre: {nombre}"
              f"Descripcion: {descripcion}"
              f"Fecha: {self.fecha}"
              f"Hora: {self.hora}"
              f"Max_personas: {max_personas}"
              f"Direccion: {direccion}"
              f"Latitud: {latitud}"
              f"Longitud: {longitud}")

if __name__ == '__main__':
    MainApp().run()