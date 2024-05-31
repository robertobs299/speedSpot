from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.swiper import MDSwiperItem
import conexion

# Load the KV file
Builder.load_file('main.kv')

class MyCard(MDSwiperItem):
    blanco = StringProperty('')
    image_source = StringProperty('')
    vehicle_name = StringProperty('')
    vehicle_year = StringProperty('')
    vehicle_power = StringProperty('')


class MainApp(MDApp):
    username = StringProperty()
    vehicles = ListProperty([])
    quedadas_organizadas = NumericProperty(0)
    quedadas_visitadas = NumericProperty(0)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        # Reemplaza 'user_id' con el ID del usuario que quieres recuperar
        user_id = 6
        self.username = self.get_username_from_db(user_id)
        self.vehicles = self.get_vehicles_from_db(user_id)
        self.quedadas_organizadas = self.get_quedadas_organizadas_from_db(user_id)
        self.quedadas_visitadas = self.get_quedadas_visitadas_from_db(user_id)
        return Builder.load_file('layout.kv')

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

    def on_start(self):
        swiper = self.root.ids.swiper
        if not self.vehicles:
            vehicle_card = MyCard(
                blanco='‎ ',
                image_source='vehiculosnuevo.jpeg',  # Usa una imagen predeterminada para los vehículos
                vehicle_year='Añadadir vehículo',
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


if __name__ == '__main__':
    MainApp().run()
