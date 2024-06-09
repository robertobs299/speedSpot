import paramiko
from kivy.uix.image import AsyncImage
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.bubble import Bubble
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.image import Image
from kivy.metrics import dp
from main.Clases import conexion
from main.Clases.Quedada import Quedada2

#Clase que permite hacer click en el mapa
class ClickableMapView(MapView):
    current_marker = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.scroll_enabled = False
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            touch_lat, touch_lon = self.get_latlon_at(*touch.pos)
            if self.current_marker:
                self.remove_widget(self.current_marker)
            self.current_marker = self.cambiar_marcador(touch_lat, touch_lon, "You clicked here")
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.parent.scroll_enabled = True
        return super().on_touch_up(touch)
#Metodo que permite cambiar el marcador del mapa
    def cambiar_marcador(self, lat, lon, text):
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
    current_quedada_id = None  # Atributo para guardar el ID de la quedada actual
    confirm_dialog = None  # Atributo para el diálogo de confirmación

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        Clock.schedule_interval(self.change_slide, 5)
        return Builder.load_file('InfoQuedadas.kv')

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

#Metodo que se ejecuta al iniciar la aplicacion para colocar los datos de la quedada
    def on_start(self):
        # Obtén la primera quedada de la base de datos
        primera_quedada = Quedada2.get_last_five()[0]  # Suponiendo que el método devuelve una lista
        self.current_quedada_id = primera_quedada.id_quedada  # Guardar el ID de la quedada actual
        self.display_quedada(primera_quedada)
        self.load_photos_for_quedada(primera_quedada.id_quedada)  # Cargar fotos para la quedada
        self.check_user_signup_status(6, primera_quedada.id_quedada)  # Verificar el estado de inscripción del usuario al inicio

#Metodo que muestra la informacion de la quedada en la pantalla
    def display_quedada(self, quedada):
        # Actualiza los widgets con la información de la quedada
        self.root.ids.nombre.text += quedada.nombre
        self.root.ids.descripcion.text += quedada.descripcion
        self.root.ids.user_organiza.text += f"{quedada.organizador_nombre} {quedada.organizador_apellidos}"
        self.root.ids.fecha.text += str(quedada.fecha)
        self.root.ids.hora.text += str(quedada.hora)
        self.root.ids.direccion.text += f"{quedada.tipo_via} {quedada.direccion}, {quedada.cp}"
        self.root.ids.max_personas.text += str(quedada.max_personas)
        self.root.ids.numero_personas.text += str(quedada.numero_personas)

#Actualiza la galeria de fotos para que se vayan mostrando
    def change_slide(self, dt):
        if len(self.root.ids.carousel.slides) > 1:
            self.root.ids.carousel.load_next()
#Metodo que permite abrir el gestor de archivos
    def file_manager_open(self):
        self.file_manager.show('/')
#Metodo que permite almacenar la ruta del archivo
    def select_path(self, path):
        self.exit_manager()
        self.add_image_to_carousel_and_db(path)
#Metodo que cierra el gestor de archivos
    def exit_manager(self, *args):
        self.file_manager.close()
#Metodo que añade una imagen al carrusel y la sube al servidor
    def add_image_to_carousel_and_db(self, path):
        image = AsyncImage(source=path)
        self.root.ids.carousel.add_widget(image)
        self.upload_image_to_server_and_save_to_db(path)
#Metodo que sube la imagen al servidor y la guarda en la base de datos
    def upload_image_to_server_and_save_to_db(self, path):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname='165.227.130.67', port=22, username='root', password='Ballesta123?Rata')

        ruta_imagen_local = path.replace('\\', '/')
        ruta_imagen_remota = '/var/www/html/' + ruta_imagen_local.split('/')[-1]
        with ssh_client.open_sftp() as sftp:
            sftp.put(ruta_imagen_local, ruta_imagen_remota)
        ssh_client.close()

        ruta_imagen = 'http://165.227.130.67/' + ruta_imagen_local.split('/')[-1]
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Fotos_quedada (quedada_id, user_id, enlace_foto) VALUES (%s, %s, %s)",
                       (self.current_quedada_id, 6, ruta_imagen))
        conn.commit()
        cursor.close()
        conn.close()
#Metodo que carga las fotos de la quedada
    def load_photos_for_quedada(self, quedada_id):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT enlace_foto FROM Fotos_quedada WHERE quedada_id = %s", (quedada_id,))
        fotos = cursor.fetchall()
        cursor.close()
        conn.close()

        if not fotos:
            default_image = AsyncImage(source='default.jpeg')
            self.root.ids.carousel.add_widget(default_image)
        else:
            for foto in fotos:
                enlace_foto = foto[0]
                image = AsyncImage(source=enlace_foto)
                self.root.ids.carousel.add_widget(image)
#Metodo que permite inscribirse o desapuntarse de una quedada
    def toggle_sign_up(self, instance):
        if instance.text == 'Inscribirse':
            print("Intentando inscribirse...")
            if not self.check_if_user_is_registered(6, self.current_quedada_id):
                instance.text = 'Desapuntarse'
                instance.md_bg_color = (1, 0, 0, 1)  # Rojo
                resultado = Quedada2.unirse(6, self.current_quedada_id)  # Suponiendo que 6 es el user_id del usuario actual
                print(f"Resultado de inscribirse: {resultado}")
            else:
                print("El usuario ya está inscrito.")
        else:
            self.show_confirm_dialog(instance)
#Metodo que muestra un dialogo de confirmacion para desapuntarte de la quedada
    def show_confirm_dialog(self, instance):
        if not self.confirm_dialog:
            self.confirm_dialog = MDDialog(
                text="¿Estás seguro que quieres desapuntarte?",
                buttons=[
                    MDFlatButton(
                        text="CANCELAR",
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="CONFIRMAR",
                        on_release=lambda x: self.unsign_user(instance)
                    ),
                ],
            )
        self.confirm_dialog.open()
#Metodo que cierra el dialogo de confirmacion
    def close_dialog(self, *args):
        self.confirm_dialog.dismiss()
#Meto que desapunta al usuario de la quedada
    def unsign_user(self, instance):
        self.confirm_dialog.dismiss()
        print("Intentando desapuntarse...")
        instance.text = 'Inscribirse'
        instance.md_bg_color = self.theme_cls.primary_color  # Ámbar
        resultado = Quedada2.desapuntarse(6, self.current_quedada_id)  # Suponiendo que 6 es el user_id del usuario actual
        print(f"Resultado de desapuntarse: {resultado}")
#Metodo que comprueba si el usuario esta inscrito en la quedada
    def check_if_user_is_registered(self, user_id, quedada_id):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Asiste WHERE user_id = %s AND quedada_id = %s", (user_id, quedada_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] > 0
#Metodo que comprueba el estado de inscripcion del usuario
    def check_user_signup_status(self, user_id, quedada_id):
        if self.check_if_user_is_registered(user_id, quedada_id):
            signup_button = self.root.ids.signup_button
            signup_button.text = 'Desapuntarse'
            signup_button.md_bg_color = (1, 0, 0, 1)  # Rojo

if __name__ == '__main__':
    MainApp().run()
