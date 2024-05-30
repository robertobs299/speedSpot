from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.bubble import Bubble
from kivy.uix.image import Image
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.filemanager import MDFileManager

from main.Clases import conexion
from main.Clases.Quedada import Quedada

KV = """
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"

        Carousel:
            id: carousel
            size_hint_y: None
            height: "150dp"

        MDRaisedButton:
            text: "Añadir Imagen"
            pos_hint: {"center_x": .5}
            on_release: app.file_manager_open()

        MDBoxLayout:
            orientation: 'vertical'
            padding: "20dp"
            spacing: "20dp"
            MDLabel:
                id: nombre
                text: "Nombre: "
                theme_text_color: "Custom"
                text_color: (1, 0.843, 0, 1)
                font_style: "H5"

            MDLabel:
                id: descripcion
                text: "Descripción: "
                theme_text_color: "Custom"
                text_color: (1, 0.843, 0, 1)

            MDLabel:
                id: user_organiza
                text: "Organizador: "
                theme_text_color: "Custom"
                text_color: (1, 0.843, 0, 1)

            MDLabel:
                id: fecha
                text: "Fecha: "
                theme_text_color: "Custom"
                text_color: (1, 0.843, 0, 1)

            MDLabel:
                id: hora
                text: "Hora: "
                theme_text_color: "Custom"
                text_color: (1, 0.843, 0, 1)

            MDLabel:
                id: direccion
                text: "Dirección: "
                theme_text_color: "Custom"
                text_color: (1, 0.843, 0, 1)

            MDLabel:
                id: max_personas
                text: "Máximo de personas: "
                theme_text_color: "Custom"
                text_color: (1, 0.843, 0, 1)

            MDLabel:
                id: numero_personas
                text: "Número de personas: "
                theme_text_color: "Custom"
                text_color: (1, 0.843, 0, 1)

            MDLabel:
                id: active
                text: "Activo: "
                theme_text_color: "Custom"
                text_color: (1, 0.843, 0, 1)

        ClickableMapView:
            id: map_view
            lat: 50.6
            lon: 3.05
            zoom: 13
            size_hint: .9, .5
            pos_hint: {"center_x": .5, "center_y": .4}
"""


class ClickableMapView(MapView):
    current_marker = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.scroll_enabled = False
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            touch_lat, touch_lon = self.get_latlon_at(*touch.pos)
            if self.current_marker:
                self.remove_widget(self.current_marker)
            self.current_marker = self.change_marker(touch_lat, touch_lon, "You clicked here")
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.parent.scroll_enabled = True
        return super().on_touch_up(touch)

    def change_marker(self, lat, lon, text):
        marker = MapMarkerPopup(lat=lat, lon=lon)
        bubble = Bubble()
        box_layout = MDBoxLayout(padding="4dp")
        label = MDLabel(text=text, markup=True, halign="center")
        box_layout.add_widget(label)
        bubble.add_widget(box_layout)
        marker.add_widget(bubble)
        self.add_widget(marker)
        return marker


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        Clock.schedule_interval(self.change_slide, 5)
        return Builder.load_string(KV)

    def obtener_coordenadas(self):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT c.latitud, c.longitud FROM Coordenadas c JOIN Direccion d ON c.id_direccion = d.id_direccion JOIN Quedada q ON d.id_quedada = q.id_quedada WHERE q.id_quedada = %s",
            (self.id_quedada,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result  # Retorna una tupla (latitud, longitud) o None si no se encontraron coordenadas
    def on_start(self):
        # Obtén la primera quedada de la base de datos
        primera_quedada = Quedada.get_last_five()[0]  # Suponiendo que el método devuelve una lista

        # Muestra la información de la quedada en la interfaz
        self.display_quedada(primera_quedada)

    def display_quedada(self, quedada):
        # Actualiza los widgets con la información de la quedada
        self.root.ids.nombre.text += quedada.nombre
        self.root.ids.descripcion.text += quedada.descripcion
        self.root.ids.user_organiza.text += str(quedada.user_organiza)
        self.root.ids.fecha.text += str(quedada.fecha)  # Asegúrate de formatear la fecha según tus necesidades
        self.root.ids.hora.text += str(quedada.hora)
        self.root.ids.direccion.text += str(quedada.direccion)
        self.root.ids.max_personas.text += str(quedada.max_personas)
        self.root.ids.numero_personas.text += str(quedada.numero_personas)
        self.root.ids.active.text += "Sí" if quedada.active else "No"

    def change_slide(self, dt):
        if len(self.root.ids.carousel.slides) > 1:
            self.root.ids.carousel.load_next()

    def file_manager_open(self):
        self.file_manager.show('/')

    def select_path(self, path):
        self.exit_manager()
        self.add_image_to_carousel(path)

    def exit_manager(self, *args):
        self.file_manager.close()

    def add_image_to_carousel(self, path):
        image = Image(source=path)
        self.root.ids.carousel.add_widget(image)


if __name__ == '__main__':
    MainApp().run()
