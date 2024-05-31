from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
import conexion

KV = '''
<MyCard@MDSwiperItem>:
    blanco: ''
    image_source: ''
    vehicle_name: ''
    vehicle_year: ''
    vehicle_power: ''

    MDCard:
        orientation: 'vertical'
        size_hint: None, None
        size: dp(225), dp(225)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        padding: dp(7.5)
        spacing: dp(7.5)

        MDLabel:
            text: root.blanco
            theme_text_color: 'Primary'
            size_hint_y: None
            height: dp(18)
            halign: 'center'

        Image:
            source: root.image_source
            size_hint_y: 2
            height: dp(150)

        MDLabel:
            text: root.vehicle_name
            theme_text_color: 'Primary'
            size_hint_y: None
            height: dp(18)
            halign: 'center'

        MDLabel:
            text: root.vehicle_year
            theme_text_color: 'Primary'
            size_hint_y: None
            height: dp(18)
            halign: 'center'

        MDLabel:
            text: root.vehicle_power
            theme_text_color: 'Primary'
            size_hint_y: None
            height: dp(18)
            halign: 'center'


<MyQuedadaCard@MDCard>:
    image_source: ''
    quedada_name: ''
    location: ''
    date: ''
    participants: ''

    orientation: 'horizontal'
    size_hint: None, None
    size: dp(300), dp(150)
    padding: dp(10)
    spacing: dp(10)

    Image:
        source: root.image_source
        size_hint: None, None
        size: dp(100), dp(100)

    MDBoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height

        MDLabel:
            text: root.quedada_name
            theme_text_color: 'Primary'
            size_hint_y: None
            height: dp(24)
            halign: 'left'

        MDLabel:
            text: root.location
            theme_text_color: 'Primary'
            size_hint_y: None
            height: dp(24)
            halign: 'left'

        MDLabel:
            text: root.date
            theme_text_color: 'Primary'
            size_hint_y: None
            height: dp(24)
            halign: 'left'

        MDLabel:
            text: root.participants
            theme_text_color: 'Primary'
            size_hint_y: None
            height: dp(24)
            halign: 'left'


MDScreen:

    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(7.5)
            spacing: dp(7.5)
            size_hint_y: None
            height: self.minimum_height

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(187.5)
                spacing: dp(7.5)

                FloatLayout:
                    size_hint_x: 0.2
                    size_hint_y: None
                    height: dp(187.5)
                    spacing: dp(7.5)
                    canvas:
                        Color:
                            rgb: 1, 1, 1
                        Ellipse:
                            pos: self.pos
                            size: 187.5, 187.5
                            source: 'Bichoplaya.png'
                            angle_start: 0
                            angle_end: 360

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(3.75)
                    size_hint_x: 0.8
                    height: self.minimum_height

                    MDLabel:
                        id: username_label
                        text: app.username
                        halign: 'center'
                        color: 1, 0.84, 0, 1
                        font_size: '18sp'
                        font_bold: True
                        font_font_name: 'Roboto-Bold'
                        size_hint_y: None

                    MDLabel:
                        id: organized_label
                        text: f'Quedadas organizadas: {app.quedadas_organizadas}'
                        halign: 'center'
                        theme_text_color: 'Secondary'
                        size_hint_y: None
                        height: dp(18)
                        font_size: '10sp'  

                    MDLabel:
                        id: attended_label
                        text: f'Quedadas visitadas: {app.quedadas_visitadas}'
                        halign: 'center'
                        theme_text_color: 'Secondary'
                        size_hint_y: None
                        height: dp(18)
                        font_size: '10sp'

            Widget:
                size_hint_y: None
                height: dp(1.5)
                canvas:
                    Color:
                        rgba: 0.5, 0.5, 0.5, 1
                    Rectangle:
                        size: self.size
                        pos: self.pos

            BoxLayout:
                padding: dp(22.5)
                size_hint_y: None
                height: dp(24) + dp(22.5) * 2

                MDLabel:
                    text: 'Vehículos:'
                    font_style: 'H4'
                    size_hint_y: None
                    height: dp(24)
                    halign: 'left'

            MDSwiper:
                id: swiper
                size_hint_y: None
                height: dp(225)

            Widget:
                size_hint_y: None
                height: dp(20)

            BoxLayout:
                padding: dp(22.5)
                size_hint_y: None
                height: dp(24) + dp(22.5) * 2

                MDLabel:
                    text: 'Mejor quedada organizada:'
                    font_style: 'H4'
                    size_hint_y: None
                    height: dp(24)
                    font_size: '18sp'
                    halign: 'left'

            BoxLayout:
                id: best_quedada_box
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
'''


class MyCard(MDSwiperItem):
    blanco = StringProperty('')
    image_source = StringProperty('')
    vehicle_name = StringProperty('')
    vehicle_year = StringProperty('')
    vehicle_power = StringProperty('')


class MyQuedadaCard(MDCard):
    image_source = StringProperty('')
    quedada_name = StringProperty('')
    location = StringProperty('')
    date = StringProperty('')
    participants = StringProperty('')


class MainApp(MDApp):
    username = StringProperty()
    vehicles = ListProperty([])
    quedadas_organizadas = NumericProperty(0)
    quedadas_visitadas = NumericProperty(0)
    best_quedada = ListProperty([])

    def build(self):
        self.theme_cls.theme_style = "Dark"
        # Reemplaza 'user_id' con el ID del usuario que quieres recuperar
        user_id = 7
        self.username = self.get_username_from_db(user_id)
        self.vehicles = self.get_vehicles_from_db(user_id)
        self.quedadas_organizadas = self.get_quedadas_organizadas_from_db(user_id)
        self.quedadas_visitadas = self.get_quedadas_visitadas_from_db(user_id)
        self.best_quedada = self.get_best_quedada_from_db(user_id)
        return Builder.load_string(KV)

    def get_username_from_db(self, user_id):
        username = conexion.get_username(user_id)
        return f'@{username}'

    @staticmethod
    def get_vehicles_from_db(user_id):
        return conexion.get_user_vehicles(user_id)

    @staticmethod
    def get_quedadas_organizadas_from_db(user_id):
        return conexion.get_quedadas_organizadas(user_id)

    @staticmethod
    def get_quedadas_visitadas_from_db(user_id):
        return conexion.get_quedadas_visitadas(user_id)

    @staticmethod
    def get_best_quedada_from_db(user_id):
        return conexion.get_best_quedada(user_id)

    def on_start(self):
        swiper = self.root.ids.swiper
        print(f'Vehicles: {self.vehicles}')  # Debugging line
        if not self.vehicles:
            print('No vehicles found, adding default card.')  # Debugging line
            vehicle_card = MyCard(
                blanco='‎ ',
                image_source='vehiculosnuevo.jpeg',  # Usa una imagen predeterminada para los vehículos
                vehicle_name='Añadir vehículo',
                vehicle_year='',
                vehicle_power=''
            )
            swiper.add_widget(vehicle_card)
        else:
            for vehicle in self.vehicles:
                marca, modelo, anio = vehicle
                vehicle_card = MyCard(
                    blanco='‎ ',
                    image_source='cbr.png',  # Usa una imagen predeterminada para los vehículos
                    vehicle_name=f'{marca} {modelo}',
                    vehicle_year=f'Año: {anio}',
                    vehicle_power='CV: Desconocido'  # Puedes actualizar esto si tienes la información de la potencia
                )
                swiper.add_widget(vehicle_card)

        if self.best_quedada:
            quedada_card = MyQuedadaCard(image_source= 'vehiculosnuevo.jpeg',
                                         quedada_name=self.best_quedada[1],
                                         location=f"{self.best_quedada[5]}, {self.best_quedada[6]}",
                                         date=self.best_quedada[2].strftime("%d/%m/%Y"),
                                         participants=f"Participantes: {self.best_quedada[3]}")
            self.root.ids.best_quedada_box.add_widget(quedada_card)


if __name__ == '__main__':
    MainApp().run()
