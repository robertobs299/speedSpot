from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.metrics import dp
import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host="speedspot-db-do-user-16519834-0.c.db.ondigitalocean.com",
        port="25060",
        user="doadmin",
        password="AVNS_DCLwHjp1kyF7kj3AsHv",
        database="Speedspot"
    )
    return conn

class Quedada:
    def __init__(self, id_quedada, nombre, descripcion, user_organiza, fecha, hora, coordenadas, direccion_fin, max_personas, numero_personas):
        self.id_quedada = id_quedada
        self.nombre = nombre
        self.descripcion = descripcion
        self.user_organiza = user_organiza
        self.fecha = fecha
        self.hora = hora
        self.coordenadas = coordenadas
        self.direccion_fin = direccion_fin
        self.max_personas = max_personas
        self.numero_personas = numero_personas

    @staticmethod
    def get_last_five():
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id_quedada, nombre, descripcion, user_organiza, fecha, hora, coordenadas, direccion_fin, max_personas, numero_personas FROM Quedada LIMIT 5")
        result = cursor.fetchall()
        quedadas = []
        if result:
            for row in result:
                quedada = Quedada(*row)
                quedadas.append(quedada)
        conn.close()
        return quedadas

class MainApp(MDApp):
    historial_list = []

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        return Builder.load_file('bbar.kv')

    def on_start(self):
        quedadas = Quedada.get_last_five()
        for quedada in quedadas:
            self.add_card(quedada)

    def add_card(self, quedada):
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

MainApp().run()
