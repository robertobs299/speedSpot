from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.metrics import dp

class MainApp(MDApp):
    historial_list = []

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        return Builder.load_file('bbar.kv')

    def on_start(self):
        # Agregar algunas tarjetas al iniciar la app
        for i in range(5):
            self.add_card()

    def add_card(self):
        card = MDCard(
            size_hint=(None, None),
            size=(dp(400), dp(460)),  # Aumentamos la altura para que la imagen tenga más espacio
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
            source='moto.jpg',
            size_hint_y=None,
            allow_stretch=True,  # Permite que la imagen se estire para llenar el espacio disponible
            height=dp(250),  # Ajustamos la altura de la imagen
        )

        title_label = MDLabel(
            text='Quedada en Chernobyl',
            halign='center',
            size_hint_y=None,
            height=dp(30),
        )

        participants_label = MDLabel(
            text='Nº de participantes: 5',
            size_hint_y=None,
            height=dp(30),
        )

        description_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
        )

        description_label = MDLabel(
            text='Vamos a dar una vueltecilla por el Guadalquivir y si eso nos fumamos unos porrillos o lo que la situación requiera jejejejeje',
            size_hint_x=0.85,
        )

        # Crear el botón de inscripción
        sign_up_button = MDRaisedButton(
            text='Inscribirse',
            md_bg_color=self.theme_cls.primary_color,
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
            "image": 'moto.jpg',
            "title": 'Quedada en Chernobyl',
            "participants": 'Nº de participantes: 5',
            "description": 'Vamos a dar una vueltecilla por el Guadalquivir y si eso nos fumamos unos porrillos o lo que la situación requiera jejejejeje',
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
