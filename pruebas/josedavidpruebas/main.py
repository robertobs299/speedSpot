from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
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
        on_release: app.show_add_vehicle_dialog()

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
                        text: 'Quedadas organizadas: ' + str(app.quedadas_organizadas)
                        halign: 'center'
                        theme_text_color: 'Secondary'
                        size_hint_y: None
                        height: dp(18)
                        font_size: '10sp'

                    MDLabel:
                        id: attended_label
                        text: 'Quedadas visitadas: ' + str(app.quedadas_visitadas)
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
                    font_size: '18sp'

            MDSwiper:
                id: swiper
                size_hint_y: None
                height: dp(225)

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

<AddVehicleDialog>:
    orientation: 'vertical'
    spacing: dp(5)
    padding: dp(5)

    Widget:
        size_hint_y: None
        height: dp(20)

    Widget:
        size_hint_y: None
        height: dp(20)


    MDLabel:
        text: 'Añadir Vehiculo:'
        font_style: 'H4'
        size_hint_y: None
        height: dp(24)
        font_size: '26sp'
        halign: 'left'

    MDTextField:
        id: marca
        hint_text: "Marca"

    MDTextField:
        id: modelo
        hint_text: "Modelo"

    MDTextField:
        id: anio
        hint_text: "Año"

    MDTextField:
        id: cv
        hint_text: "CV"
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
    user_id = NumericProperty(7)  # Define user_id en un solo lugar
    username = StringProperty()
    vehicles = ListProperty([])
    quedadas_organizadas = NumericProperty(0)
    quedadas_visitadas = NumericProperty(0)
    best_quedada = ListProperty([])
    lista_marcas = conexion.get_marca_options()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.username = self.get_username_from_db()
        self.vehicles = self.get_vehicles_from_db()
        self.quedadas_organizadas = self.get_quedadas_organizadas_from_db()
        self.quedadas_visitadas = self.get_quedadas_visitadas_from_db()
        self.best_quedada = self.get_best_quedada_from_db()

        return Builder.load_string(KV)

    def get_username_from_db(self):
        username = conexion.get_username(self.user_id)
        return f'@{username}'

    def get_vehicles_from_db(self):
        return conexion.get_user_vehicles(self.user_id)

    def get_quedadas_organizadas_from_db(self):
        return conexion.get_quedadas_organizadas(self.user_id)

    def get_quedadas_visitadas_from_db(self):
        return conexion.get_quedadas_visitadas(self.user_id)

    def get_best_quedada_from_db(self):
        return conexion.get_best_quedada(self.user_id)

    def on_start(self):
        self.swiper = self.root.ids.swiper
        self.swipervehiculos()

        if self.best_quedada:
            quedada_card = MyQuedadaCard(image_source='vehiculosnuevo.jpeg',
                                         quedada_name=self.best_quedada[1],
                                         location=f"{self.best_quedada[5]}, {self.best_quedada[6]}",
                                         date=self.best_quedada[2].strftime("%d/%m/%Y"),
                                         participants=f"Participantes: {self.best_quedada[3]}")
            self.root.ids.best_quedada_box.add_widget(quedada_card)

    def swipervehiculos(self, *args):
        self.vehicles = self.get_vehicles_from_db()

        # Limpiar el carrusel
        self.swiper.clear_widgets()

        print(f'Vehículos: {self.vehicles}')  # Línea de depuración
        for vehicle in self.vehicles:
            marca, modelo, anio, cv = vehicle
            vehicle_card = MyCard(
                blanco='‎ ',
                image_source='cbr.png',  # Usa una imagen predeterminada para los vehículos
                vehicle_name=f'{marca} {modelo}',
                vehicle_year=f'Año: {anio}',
                vehicle_power=f'CV: {cv}'  # Puedes actualizar esto si tienes la información de la potencia
            )
            self.swiper.add_widget(vehicle_card)
        # Añade la tarjeta de 'Añadir vehículo' después de mostrar todos los vehículos existentes
        vehicle_card = MyCard(
            blanco='‎ ',
            image_source='vehiculosnuevo.jpeg',  # Usa una imagen predeterminada para los vehículos
            vehicle_name='Añadir vehículo',
            vehicle_year='',
            vehicle_power=''
        )
        self.swiper.add_widget(vehicle_card)

    def show_add_vehicle_dialog(self):
        self.dialog = MDDialog(
            type="custom",
            size_hint=(0.8, 1),
            content_cls=AddVehicleDialog(),
            buttons=[
                MDRaisedButton(text="CANCELAR", on_release=self.close_dialog),
                MDRaisedButton(
                    text="AÑADIR",
                    on_release=lambda x: (self.add_vehicle_to_db(), self.swipervehiculos())
                )]
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

    def add_vehicle_to_db(self, *args):
        content = self.dialog.content_cls
        marca = content.ids.marca.text
        modelo = content.ids.modelo.text
        anio = content.ids.anio.text
        cv = content.ids.cv.text

        # Añadir lógica para insertar el vehículo en la base de datos
        conexion.add_vehicle(self.user_id, marca, modelo, anio, cv)

        self.close_dialog()


class AddVehicleDialog(MDBoxLayout):
    pass


if __name__ == '__main__':
    MainApp().run()
