from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.bubble import Bubble
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

from pruebas.RobertoPruebas import conexion
from pruebas.RobertoPruebas.Clases.Quedada import Quedada


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


KV = """
#:import MapSource kivy_garden.mapview.MapSource

MDFloatLayout:
    MDCard:
        size_hint: 1, 1
        pos_hint: {"center_x": .5, "center_y": .5}
        Carousel:
            id: slide
            MDFloatLayout:
                MDTextField:
                    id: nombre
                    hint_text: "Nombre"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    size_hint_x: .8
                MDTextField:
                    id: descripcion
                    hint_text: "Descripcion"
                    pos_hint: {"center_x": .5, "center_y": .45}
                    size_hint_x: .8
                    size_hint_y: .2
                    multiline: True
                MDTextField:
                    id: max_personas
                    hint_text: "Maximos Participantes"
                    pos_hint: {"center_x": .5, "center_y": .3}
                    size_hint_x: .8
                MDRaisedButton:
                    id: fecha
                    text: "Fecha"
                    pos_hint: {"center_x": .3, "center_y": .2}
                    size_hint_x: .39
                    on_release: app.show_date_picker()
                MDRaisedButton:
                    id: hora
                    text: "Hora"
                    pos_hint: {"center_x": .7, "center_y": .2}
                    size_hint_x: .39
                    on_release: app.show_time_picker()
                MDRaisedButton:
                    id: next1
                    text: "Siguiente"
                    pos_hint: {"center_x": .5, "center_y": .1}
                    size_hint_x: .8
                    on_release: app.next1()

            MDFloatLayout:
                Spinner:
                    id: tipo_via
                    text: "Tipo de vía"
                    values: ["Calle", "Avenida", "Plaza", "Paseo", "Camino"]
                    pos_hint: {"center_x": .5, "center_y": .6}
                    size_hint_x: .8 
                    size_hint_y: .1
                    text_align: "left"                 

                MDTextField:
                    id: direccion
                    hint_text: "Direccion"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    size_hint_x: .8
                MDTextField:
                    id: cp
                    hint_text: "Codigo Postal"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    size_hint_x: .8 
                MDTextField:
                    id: numero
                    hint_text: "numero"
                    pos_hint: {"center_x": .5, "center_y": .3}
                    size_hint_x: .8 
                MDLabel:
                    id: error_cp
                    text: "El código postal no es válido"
                    pos_hint: {"center_x": .5, "center_y": .25}
                    halign: "center"         
                    theme_text_color: "Error" 
                    opacity: 0        
                MDRaisedButton:
                    text: "Anterior"
                    pos_hint: {"center_x": .3, "center_y": .2}
                    size_hint_x: .39
                    on_release: app.previous1()
                MDRaisedButton:
                    id: next2
                    text: "Siguiente"
                    pos_hint: {"center_x": .7, "center_y": .2}
                    size_hint_x: .39
                    on_release: app.next2()

            MDFloatLayout:
                MDRelativeLayout:
                    ClickableMapView:
                        id: map_view
                        lat:50.6
                        lon:3.05
                        zoom:13 
                        size_hint: .9, .5  # Ajusta el tamaño del mapa
                        pos_hint: {"center_x": .5, "center_y": .4}
                MDRaisedButton:
                    text: "Anterior"
                    pos_hint: {"center_x": .3, "center_y": .1}
                    size_hint_x: .39
                    on_press: app.previous2()
                MDRaisedButton:
                    text: "Registrar"
                    pos_hint: {"center_x": .7, "center_y": .1}
                    size_hint_x: .39
                    on_release: app.crear_quedada()
    
    MDLabel:
        text: "Crear Quedada"
        bold: True
        pos_hint: {"center_x": .8, "center_y": .9}    
        font_style: "H4" 
    MDIconButton:
        id: icon1_progreso
        icon: "information"
        pos_hint: {"center_x": .14, "center_y": .75}
        user_font_size: "50sp"
        theme_text_color: "Custom"
    MDProgressBar:
        id: progress1
        size_hint_x: .3
        size_hint_y: .015
        pos_hint: {"center_x": .315, "center_y": .75}

    MDIconButton:
        id: icon2_progreso
        icon: "map-marker"
        pos_hint: {"center_x": .5, "center_y": .75}
        user_font_size: "50sp"
        theme_text_color: "Custom"
    MDProgressBar:
        id: progress2
        size_hint_x: .3
        size_hint_y: .015
        pos_hint: {"center_x": .68, "center_y": .75}

    MDIconButton:
        id: icon3_progreso
        icon: "map"
        pos_hint: {"center_x": .86, "center_y": .75}
        user_font_size: "50sp"
        theme_text_color: "Custom" 

"""

def insertarCoordenadas(latitud, longitud):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Coordenadas (latitud, longitud) VALUES (%s, %s)", (latitud, longitud))
    conn.commit()
    conn.close()
    return cursor.lastrowid
def insertar_direccion(tipo_via,direccion, cp, numero):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Direccion (tipo_via, direccion, cp, numero_via) VALUES (%s, %s, %s, %s)", (tipo_via, direccion, cp, numero))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def actualizar_coordenadas_direccion(id_direccion, id_coordenadas):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Direccion SET coordenadas = %s WHERE id_direccion = %s", (id_coordenadas, id_direccion))
    conn.commit()
    conn.close()


def obtener_id_cp(cp):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cp FROM Postal_code WHERE cp = %s", (cp,))
    result = cursor.fetchone()
    conn.close()
    return result[0]
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

    def next1(self):
        self.root.ids.slide.load_next(mode="next")
        self.root.ids.icon1_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.ids.progress1)
        self.root.ids.icon1_progreso.icon = "check-circle"

    def next2(self):
        if not self.root.ids.cp.text or not self.root.ids.direccion.text or not self.root.ids.numero.text:
            # Si alguno de los campos está vacío, agitar el botón y salir del método
            anim = Animation(x=self.root.ids.nombre.x + 10, duration=0.1) + Animation(x=self.root.ids.nombre.x - 10,
                                                                                      duration=0.1)
            anim.repeat = 3
            anim.start(self.root.ids.next2)
            return

        self.root.ids.slide.load_next(mode="next")
        self.root.ids.icon2_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.ids.progress2)
        self.root.ids.icon2_progreso.icon = "check-circle"

    def previous1(self):
        self.root.ids.slide.load_previous()
        self.root.ids.icon1_progreso.text_color = 0, 0, 0, 1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.ids.progress1)
        self.root.ids.icon1_progreso.icon = "numeric-1-circle"

    def previous2(self):
        self.root.ids.slide.load_previous()
        self.root.ids.icon2_progreso.text_color = 0, 0, 0, 1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.ids.progress2)
        self.root.ids.icon2_progreso.icon = "numeric-2-circle"

    def crear_quedada(self):
        id_cp = obtener_id_cp(self.root.ids.cp.text)

        id_direccion = insertar_direccion(self.root.ids.tipo_via.text, self.root.ids.direccion.text, id_cp, self.root.ids.numero.text)

        id_corrdenadas = insertarCoordenadas(self.root.ids.map_view.lat, self.root.ids.map_view.lon)

        actualizar_coordenadas_direccion(id_direccion, id_corrdenadas)

        quedada = Quedada(None, self.root.ids.nombre.text, self.root.ids.descripcion.text, 1, self.fecha, self.hora, id_direccion, self.root.ids.max_personas.text, 0, 1)

        quedada.insertar_quedada()


if __name__ == '__main__':
    MainApp().run()