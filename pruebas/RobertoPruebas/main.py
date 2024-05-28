from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.bubble import Bubble
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.metrics import dp
from kivymd.uix.pickers import MDTimePicker, MDDatePicker
from pruebas.RobertoPruebas import conexion
from pruebas.RobertoPruebas.Clases.Quedada import Quedada


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


class MainApp(Screen):
    historial_list = []
    dark_theme = True

    def build(self):
        App.get_running_app().theme_cls.theme_style = "Dark"
        App.get_running_app().theme_cls.primary_palette = "Amber"
        Builder.load_file('main.kv')
        return self

    def toggle_theme(self):
        if self.dark_theme:
            self.theme_cls.theme_style = "Light"  # Cambia al tema claro
            self.theme_cls.primary_palette = "Amber"

        else:
            self.theme_cls.theme_style = "Dark"  # Cambia al tema oscuro
            self.theme_cls.primary_palette = "Amber"

        self.dark_theme = not self.dark_theme  # Cambia el estado del tema
    def on_start(self):
        quedadas = Quedada.get_last_five()
        for quedada in quedadas:
            self.add_card(quedada)

    def add_card(self, quedada):
        card = MDCard(
            size_hint=(1, None),
            height=dp(460),
            pos_hint={"center_x": 0.5},
            elevation=10,
            radius=[15],
        )

        box_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(10),
        )

        image = Image(
            source="moto.jpg",  # Reemplazar con quedada.imagen_url si se tiene la URL de la imagen
            size_hint_y=None,
            allow_stretch=True,
            height=dp(250),
        )

        title_label = MDLabel(
            text=quedada.nombre,
            halign='center',
            size_hint_y=None,
            height=dp(30),
        )

        participants_label = MDLabel(
            text=f'Nº de participantes: {quedada.numero_personas}',
            size_hint_y=None,
            height=dp(30),
        )

        description_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
        )

        description_label = MDLabel(
            text=quedada.descripcion,
            size_hint_x=0.85,
        )

        sign_up_button = MDRaisedButton(
            text='Inscribirse',
            md_bg_color=self.theme_cls.primary_color,
            size_hint_x=0.15,
            on_release=self.toggle_sign_up
        )

        description_layout.add_widget(description_label)
        description_layout.add_widget(sign_up_button)

        box_layout.add_widget(image)
        box_layout.add_widget(title_label)
        box_layout.add_widget(participants_label)
        box_layout.add_widget(description_layout)

        card.add_widget(box_layout)
        card.data = {
            "id": quedada.id_quedada,
            "image": "default_image.jpg",  # Reemplazar con quedada.imagen_url si se tiene la URL de la imagen
            "title": quedada.nombre,
            "participants": f'Nº de participantes: {quedada.numero_personas}',
            "description": quedada.descripcion,
        }

        self.root.ids.card_list.add_widget(card)
        self.root.ids.card_list.height += card.height + dp(15)  # Update height of BoxLayout

    def toggle_sign_up(self, instance):
        parent_card = instance.parent.parent.parent
        card_data = parent_card.data

        if instance.text == 'Inscribirse':
            instance.text = 'Desapuntarse'
            instance.md_bg_color = (1, 0, 0, 1)  # Rojo
            self.historial_list.insert(0, card_data)
        else:
            instance.text = 'Inscribirse'
            instance.md_bg_color = self.theme_cls.primary_color  # Ámbar
            self.historial_list.remove(card_data)

        self.update_historial()

    def update_historial(self):
        historial_container = self.root.ids.historial_list
        historial_container.clear_widgets()

        for event in self.historial_list:
            card = MDCard(
                size_hint=(None, None),
                size=(dp(400), dp(460)),
                pos_hint={"center_x": 0.5},
                elevation=10,
                radius=[15],
            )

            box_layout = MDBoxLayout(
                orientation='vertical',
                padding=dp(10),
                spacing=dp(10),
            )

            image = Image(
                source=event['image'],
                size_hint_y=None,
                allow_stretch=True,
                height=dp(250),
            )

            title_label = MDLabel(
                text=event['title'],
                halign='center',
                size_hint_y=None,
                height=dp(30),
            )

            participants_label = MDLabel(
                text=event['participants'],
                size_hint_y=None,
                height=dp(30),
            )

            description_layout = MDBoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(60),
            )

            description_label = MDLabel(
                text=event['description'],
                size_hint_x=0.85,
            )

            description_layout.add_widget(description_label)

            box_layout.add_widget(image)
            box_layout.add_widget(title_label)
            box_layout.add_widget(participants_label)
            box_layout.add_widget(description_layout)

            card.add_widget(box_layout)
            historial_container.add_widget(card)
            historial_container.height += card.height + dp(15)  # Update height of BoxLayout

    fecha = ""
    hora = ""

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

        id_direccion = insertar_direccion(self.root.ids.tipo_via.text, self.root.ids.direccion.text, id_cp,
                                          self.root.ids.numero.text)

        id_corrdenadas = insertarCoordenadas(self.root.ids.map_view.lat, self.root.ids.map_view.lon)

        actualizar_coordenadas_direccion(id_direccion, id_corrdenadas)

        quedada = Quedada(None, self.root.ids.nombre.text, self.root.ids.descripcion.text, 1, self.fecha, self.hora,
                          id_direccion, self.root.ids.max_personas.text, 0, 1)

        quedada.insertar_quedada()



# MainApp().run()
