import requests
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.bubble import Bubble
from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import AsyncImage  # Usamos AsyncImage en lugar de Image
from kivy.metrics import dp
from kivymd.uix.pickers import MDTimePicker, MDDatePicker

from main.Clases.Quedada import Quedada
from pruebas.RobertoPruebas import conexion
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.label import MDLabel


class ConfigScreen(Screen):
    pass


class MainScreen(Screen):
    pass


def insertarCoordenadas(latitud, longitud):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Coordenadas (latitud, longitud) VALUES (%s, %s)", (latitud, longitud))
    conn.commit()
    conn.close()
    return cursor.lastrowid


def insertar_direccion(tipo_via, direccion, cp, numero):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Direccion (tipo_via, direccion, cp, numero_via) VALUES (%s, %s, %s, %s)",
                   (tipo_via, direccion, cp, numero))
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


def obtener_enlace_foto(quedada_id):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT enlace_foto FROM Fotos_quedada WHERE quedada_id = %s", (quedada_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def verificar_url_imagen(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False


def change_marker(map_view, lat, lon, text):
    marker = MapMarkerPopup(lat=lat, lon=lon)
    bubble = Bubble()
    box_layout = MDBoxLayout(padding="4dp")
    label = MDLabel(text=text, markup=True, halign="center")
    box_layout.add_widget(label)
    bubble.add_widget(box_layout)
    marker.add_widget(bubble)
    map_view.add_widget(marker)
    return marker


class ClickableMapView(MapView):
    current_marker = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.scroll_enabled = False
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            touch_lat, touch_lon = self.get_latlon_at(*touch.pos)
            if self.current_marker:
                self.remove_widget(self.current_marker)
            self.current_marker = change_marker(self, touch_lat, touch_lon, "You clicked here")
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.parent.scroll_enabled = True
        return super().on_touch_up(touch)


class MainApp(MDApp):
    historial_list = []
    dark_theme = True
    open_expansion_panels = []
    open_expansion_panel = None
    open_expansion_panel_height = None

    def open_config_screen(self):
        self.root.current = 'config'

    def go_back_to_main_screen(self):
        self.root.current = 'main'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        return Builder.load_file('bbar.kv')

    def toggle_theme(self):
        if self.dark_theme:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Amber"
        else:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "Amber"
        self.dark_theme = not self.dark_theme

    def on_start(self):
        quedadas = Quedada
        for quedada in quedadas:
            self.add_card(quedada)

    def add_card(self, quedada):
        enlace_foto = obtener_enlace_foto(quedada.id_quedada)
        imagen_url = enlace_foto if enlace_foto and verificar_url_imagen(enlace_foto) else "moto.jpg"

        card = MDCard(
            size_hint=(None, None),
            size=(dp(300), dp(360)),
            pos_hint={"center_x": 0.5},
            elevation=10,
            radius=[15],
        )
        if quedada.active == 0:
            card.opacity = 0.5
            sign_up_button_disabled = True
        else:
            sign_up_button_disabled = False

        box_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(2),
            size_hint_y=None,
            height=dp(360),
        )

        image = AsyncImage(  # Usamos AsyncImage para cargar la imagen de forma asíncrona
            source=imagen_url,
            size_hint_y=None,
            allow_stretch=True,
            height=dp(150),
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
            on_release=self.toggle_sign_up,
            disabled=sign_up_button_disabled
        )

        description_layout.add_widget(description_label)
        description_layout.add_widget(sign_up_button)

        panel_content = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        additional_info = [
            f'Fecha: {quedada.fecha}',
            f'Hora: {quedada.hora}',
            f'Máx. personas: {quedada.max_personas}',
            f'Dirección: {quedada.direccion}'
        ]
        for info in additional_info:
            panel_content.add_widget(MDLabel(text=info, size_hint_y=None, height=dp(20)))

        expansion_panel = MDExpansionPanel(
            content=panel_content,
            panel_cls=MDExpansionPanelOneLine(text='Mostrar más información')
        )
        expansion_panel.bind(on_open=self.on_panel_open)

        box_layout.add_widget(image)
        box_layout.add_widget(title_label)
        box_layout.add_widget(participants_label)
        box_layout.add_widget(description_layout)
        box_layout.add_widget(expansion_panel)

        card.add_widget(box_layout)
        card.data = {
            "id": quedada.id_quedada,
            "image": imagen_url,
            "title": quedada.nombre,
            "participants": f'Nº de participantes: {quedada.numero_personas}',
            "description": quedada.descripcion,
        }

        self.root.ids.card_list.add_widget(card)
        self.root.ids.card_list.height = card.height + dp(15)

    def toggle_sign_up(self, button):
        card = button.parent.parent.parent
        button_text = button.text
        if button_text == "Inscribirse":
            button.text = "Desapuntarse"
            card.opacity = 0.5
        else:
            button.text = "Inscribirse"
            card.opacity = 1

    def show_info_dialog(self, title, text):
        if not hasattr(self, 'info_dialog'):
            self.info_dialog = None
        if not self.info_dialog:
            self.info_dialog = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text="Cerrar",
                        on_release=self.close_info_dialog
                    )
                ],
            )
        self.info_dialog.open()

    def close_info_dialog(self, obj):
        if self.info_dialog:
            self.info_dialog.dismiss()

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.on_time_save, on_cancel=self.on_cancel)
        time_dialog.open()

    def on_time_save(self, instance, time):
        self.root.ids.time_label.text = str(time)

    def on_cancel(self, instance, time):
        self.root.ids.time_label.text = "You Clicked Cancel"

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.root.ids.date_label.text = str(value)

    def on_panel_open(self, instance_panel, instance_expansion):
        if self.open_expansion_panel and self.open_expansion_panel != instance_expansion:
            self.open_expansion_panel.collapse()
            self.open_expansion_panel_height = instance_expansion.height
        self.open_expansion_panel = instance_expansion


if __name__ == '__main__':
    MainApp().run()
