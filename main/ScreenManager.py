import re
import tempfile
import urllib
import urllib.request
import paramiko
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.bubble import Bubble
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.metrics import dp
from kivymd.uix.pickers import MDTimePicker, MDDatePicker
from main.Clases.Quedada import Quedada, Quedada2
import hashlib
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image, Loader, AsyncImage
from main.Clases import conexion
from main.Clases.User import User


###### REGISTRO #######################################################################################################
def validate_email(email):
    pattern = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    match = pattern.fullmatch(email)
    return bool(match)
def is_valid_password(password):
    # Define la expresión regular para validar la contraseña
    password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@$!%*?&]{8,}$')
    return bool(password_regex.match(password))
def is_valid_cp(cp):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT cp FROM Postal_code WHERE cp like %s", (cp,))
    result = cursor.fetchall()  # Utiliza fetchall() en lugar de fetchone()
    conn.close()
    if not result:
        return False
    return True
def is_valid_phone_number(phone_number):
    # Define la expresión regular para validar números de teléfono
    phone_number_pattern = re.compile(r'^\+?[1-9][0-9]{7,14}$')
    return bool(phone_number_pattern.match(phone_number))

def exist_user(username):
    conn = conexion.connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT id_user FROM Login WHERE username = %s", (username,))
    result = cursor.fetchone()
    conn.close()
    if not result:
        return False
    return True

# Registrar al usuario en base de daatos:

def registrar(email, password, username,name, surname, postalcode, phone,):

    encrypted_password = hashlib.sha256(password.encode()).hexdigest()

    # Conexión a la base de datos
    conn = conexion.connect_to_database()
    cursor = conn.cursor()

    # Buscar el ID del código postal
    cursor.execute("SELECT id_cp FROM Postal_code WHERE cp LIKE %s", (str(postalcode),))
    result = cursor.fetchall()  # Utiliza fetchall() en lugar de fetchone()

    if result:
        idCp = result[0][0]  # Obtener el ID del código postal
    else:
        # Si no se encuentra el código postal, puedes manejar el error aquí
        print("El código postal no existe en la base de datos")
        conn.close()
        print(result)

    # Calcular el hash de la contraseña
    encrypted_password = hashlib.sha256(password.encode()).hexdigest()

    # Insertar el usuario en la tabla User
    cursor.execute(
        "INSERT INTO User (email, nombre, apellidos, cp, telefono) VALUES (%s, %s, %s, %s, %s)",
        (email, name, surname, idCp, phone))

    iduser = cursor.lastrowid

    # Insertar los datos de inicio de sesión en la tabla Login
    cursor.execute("INSERT INTO Login (id_user, username, password) VALUES (%s, %s, %s)",
                   (iduser, username, encrypted_password))

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()
    return iduser

###### CREAR QUEDADA ###################################################################################################
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

def load_image_from_url(url):
    with urllib.request.urlopen(url) as response:
        img_data = response.read()
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    # Write the image data to the temporary file
    temp_file.write(img_data)
    # Close the file
    temp_file.close()
    # Return the path to the temporary file
    return temp_file.name


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


def encrypt_password(password):
    # Convertir la contraseña a bytes
    password_bytes = password.encode('utf-8')
    # Calcular el hash SHA256 de la contraseña
    password_hash = hashlib.sha256(password_bytes).hexdigest()
    return password_hash






class MyApp(MDApp):
    user = None
    dark_theme = True
    current_id_quedada = 0
    confirm_dialog = None
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        sm = ScreenManager()
        sm.add_widget(Builder.load_file('Login.kv'))
        sm.add_widget(Builder.load_file('main.kv'))
        sm.add_widget(Builder.load_file('Singin.kv'))
        sm.current = 'login'
        return sm

    def change_screen(self, screen_name):
        # Cambia a la pantalla especificada
        self.root.current = screen_name


###### VER QUEDADAS ####################################################################################################
    def toggle_theme(self):
        if self.dark_theme:
            self.theme_cls.theme_style = "Light"  # Cambia al tema claro
            self.theme_cls.primary_palette = "Amber"

        else:
            self.theme_cls.theme_style = "Dark"  # Cambia al tema oscuro
            self.theme_cls.primary_palette = "Amber"

        self.dark_theme = not self.dark_theme  # Cambia el estado del tema
    def on_start(self):
        # Limpiar la lista de quedadas existentes
        self.root.get_screen('main').ids.card_list.clear_widgets()

        # Obtener las últimas cinco quedadas
        quedadas = Quedada.get_last_five()

        # Agregar cada quedada a la pantalla
        for quedada in quedadas:
            self.add_card(quedada)

    def mostrar_historial(self):
        # Limpiar la lista de quedadas existentes
        self.root.get_screen('main').ids.historial_list.clear_widgets()

        # Obtener las últimas cinco quedadas
        historial = Quedada.get_quedadas_user_asist(self.user.id)

        # Agregar cada quedada a la pantalla
        for quedada in historial:
            self.add_card_historial(quedada)


#Metodo que crea las tarjetas de las quedadas y las añade al layout
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
        if quedada.imagen is not None:
            url = load_image_from_url(quedada.imagen)
            image = Image(
                source=url,  # Load image from URL
                size_hint_y=None,
                allow_stretch=True,
                height=dp(250),
            )
            # Add the card to a layout or return it
        else:
            print("No hay imagen en la bbdd disponible para esta quedada")
            image = Image(
                source='moto.jpg',
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
            text='Ver Quedada',
            md_bg_color=self.theme_cls.primary_color,
            size_hint_x=0.15,
            on_release=self.on_view_quedadas_button_press

        )

        description_layout.add_widget(description_label)
        description_layout.add_widget(sign_up_button)

        box_layout.add_widget(image)
        box_layout.add_widget(title_label)
        box_layout.add_widget(description_layout)

        card.add_widget(box_layout)
        card.data = {
            "id": quedada.id_quedada,
            "image": "default_image.jpg",
            "title": quedada.nombre,
            "participants": f'Nº de participantes: {quedada.numero_personas}',
            "description": quedada.descripcion,
        }

        self.root.get_screen('main').ids.card_list.add_widget(card)
        self.root.get_screen('main').ids.card_list.height += card.height + dp(15)  # Update height of BoxLayout

    def add_card_historial(self, quedada):
        card_user = MDCard(
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
        if quedada.imagen is not None:
            url = load_image_from_url(quedada.imagen)
            image = Image(
                source=url,  # Load image from URL
                size_hint_y=None,
                allow_stretch=True,
                height=dp(250),
            )
            # Add the card to a layout or return it
        else:
            print("No hay imagen en la bbdd disponible para esta quedada")
            image = Image(
                source='moto.jpg',
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
            text='Ver Quedada',
            md_bg_color=self.theme_cls.primary_color,
            size_hint_x=0.15,
            on_release=self.on_view_quedadas_button_press

        )

        description_layout.add_widget(description_label)
        description_layout.add_widget(sign_up_button)

        box_layout.add_widget(image)
        box_layout.add_widget(title_label)
        box_layout.add_widget(description_layout)

        card_user.add_widget(box_layout)
        card_user.data = {
            "id": quedada.id_quedada,
            "image": "default_image.jpg",
            "title": quedada.nombre,
            "participants": f'Nº de participantes: {quedada.numero_personas}',
            "description": quedada.descripcion,
        }

        self.root.get_screen('main').ids.historial_list.add_widget(card_user)
        self.root.get_screen('main').ids.historial_list.height += card_user.height + dp(15)  # Update height of BoxLayout

    def reinicio_info_quedada(self):
        # Restablecer todos los campos de entrada

        self.root.get_screen('ver_quedada').ids.nombre.text = "Nombre:"
        self.root.get_screen('ver_quedada').ids.descripcion.text = "Descripción:"
        self.root.get_screen('ver_quedada').ids.user_organiza.text = "Organizador:"
        self.root.get_screen('ver_quedada').ids.fecha.text = "Fecha:"
        self.root.get_screen('ver_quedada').ids.hora.text = "Hora:"
        self.root.get_screen('ver_quedada').ids.direccion.text = "Dirección:"
        self.root.get_screen('ver_quedada').ids.max_personas.text = "Max. personas:"
        self.root.get_screen('ver_quedada').ids.numero_personas.text = "Número de personas:"
        self.change_screen('main')
        self.clear_carousel()


    def ver_id_quedada(self,instance):
        parent_card = instance.parent.parent.parent
        card_data = parent_card.data
        self.current_id_quedada = card_data['id']
        print (f"{self.current_id_quedada}")
        sm = ScreenManager()
        sm.add_widget(Builder.load_file('infoQuedadas.kv'))
        sm.current = 'ver_quedada'
    # def toggle_sign_up(self, instance):
    #     parent_card = instance.parent.parent.parent
    #     card_data = parent_card.data
    #
    #     if instance.text == 'Inscribirse':
    #         instance.text = 'Desapuntarse'
    #         instance.md_bg_color = (1, 0, 0, 1)  # Rojo
    #         Quedada.unirse(self.user.id, card_data['id'])
    #         self.historial_list.insert(0, card_data)
    #     else:
    #         instance.text = 'Inscribirse'
    #         instance.md_bg_color = self.theme_cls.primary_color  # Ámbar
    #         Quedada.desapuntarse(self.user.id, card_data['id'])
    #         self.historial_list.remove(card_data)
    #
    #     self.update_historial()

#Metodo que actualiza el historial de quedadas a las que el usuario se ha apuntado
    # def update_historial(self):
    #     historial_container = self.root.get_screen('main').ids.historial_list
    #     historial_container.clear_widgets()
    #
    #     for event in self.historial_list:
    #         card = MDCard(
    #             size_hint=(None, None),
    #             size=(dp(400), dp(460)),
    #             pos_hint={"center_x": 0.5},
    #             elevation=10,
    #             radius=[15],
    #         )
    #
    #         box_layout = MDBoxLayout(
    #             orientation='vertical',
    #             padding=dp(10),
    #             spacing=dp(10),
    #         )
    #
    #         image = Image(
    #             source=event['image'],
    #             size_hint_y=None,
    #             allow_stretch=True,
    #             height=dp(250),
    #         )
    #
    #         title_label = MDLabel(
    #             text=event['title'],
    #             halign='center',
    #             size_hint_y=None,
    #             height=dp(30),
    #         )
    #
    #         participants_label = MDLabel(
    #             text=event['participants'],
    #             size_hint_y=None,
    #             height=dp(30),
    #         )
    #
    #         description_layout = MDBoxLayout(
    #             orientation='horizontal',
    #             size_hint_y=None,
    #             height=dp(60),
    #         )
    #
    #         description_label = MDLabel(
    #             text=event['description'],
    #             size_hint_x=0.85,
    #         )
    #
    #         description_layout.add_widget(description_label)
    #
    #         box_layout.add_widget(image)
    #         box_layout.add_widget(title_label)
    #         box_layout.add_widget(participants_label)
    #         box_layout.add_widget(description_layout)
    #
    #         card.add_widget(box_layout)
    #         historial_container.add_widget(card)
    #         historial_container.height += card.height + dp(15)  # Update height of BoxLayout


######### CREAR QUEDADA ################################################################################################
    fecha = ""
    hora = ""
    ruta_imagen = None
    def reset_and_go_to_first_screen(self):
        # Restablecer todos los campos de entrada
        self.root.get_screen('main').ids.nombre.text = ""
        self.root.get_screen('main').ids.descripcion.text = ""
        self.root.get_screen('main').ids.tipo_via.text = ""
        self.root.get_screen('main').ids.direccion.text = ""
        self.root.get_screen('main').ids.numero.text = ""
        self.root.get_screen('main').ids.cp.text = ""
        self.root.get_screen('main').ids.max_personas.text = ""
        # Cambiar a la primera pantalla del registro de quedadas
        self.root.get_screen('main').ids.slide.load_slide(self.root.get_screen('main').ids.slide.slides[0])
        self.previous2()
        self.previous1()


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


    def check_theme(self):
        if self.theme_cls.theme_style == "Dark":
            return 1
        else:
            return 0

    def show_missing_fields_dialog(self, missing_fields):
        close_button = MDFlatButton(text='Cerrar',
                                    on_release=lambda x: dialog.dismiss())  # Botón para cerrar el diálogo
        dialog = MDDialog(title="Campos faltantes:", auto_dismiss=False, buttons=[close_button])
        dialog.text = missing_fields  # Añadir el texto directamente al diálogo
        dialog.open()


    def next1(self):
        missing_fields = ""
        if not self.root.get_screen('main').ids.nombre.text:
            missing_fields += "Nombre, "
        if not self.root.get_screen('main').ids.descripcion.text:
            missing_fields += "Descripción, "
        if not self.root.get_screen('main').ids.max_personas.text:
            missing_fields+= "Máximo de personas, "
        if self.fecha == "":
            missing_fields += "Fecha, "
        if self.hora == "":
            missing_fields += "Hora, "
        if missing_fields:
            self.show_missing_fields_dialog(missing_fields)
            return
        self.root.get_screen('main').ids.slide.load_next(mode="next")
        self.root.get_screen('main').ids.icon1_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.get_screen('main').ids.progress1)
        self.root.get_screen('main').ids.icon1_progreso.icon = "check-circle"

    def next2(self):
        missing_fields = ""
        if not self.root.get_screen('main').ids.tipo_via.text:
            missing_fields += "Tipo de vía,"
        if not self.root.get_screen('main').ids.direccion.text:
            missing_fields += "Dirección, "
        if not self.root.get_screen('main').ids.numero.text:
            missing_fields += "Número, "
        if not self.root.get_screen('main').ids.cp.text:
            missing_fields +="Código postal, "
        if missing_fields:
            self.show_missing_fields_dialog(missing_fields)
            return

        self.root.get_screen('main').ids.slide.load_next(mode="next")
        self.root.get_screen('main').ids.icon2_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.get_screen('main').ids.progress2)
        self.root.get_screen('main').ids.icon2_progreso.icon = "check-circle"

    def previous1(self):
        self.root.get_screen('main').ids.slide.load_previous()
        color = self.check_theme()
        self.root.get_screen('main').ids.icon1_progreso.text_color = color,color,color,1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.get_screen('main').ids.progress1)
        self.root.get_screen('main').ids.icon1_progreso.icon = "numeric-1-circle"

    def previous2(self):
        self.root.get_screen('main').ids.slide.load_previous()
        color = self.check_theme()
        self.root.get_screen('main').ids.icon2_progreso.text_color = color,color,color,1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.get_screen('main').ids.progress2)
        self.root.get_screen('main').ids.icon2_progreso.icon = "numeric-2-circle"

    def crear_quedada(self):
        id_cp = obtener_id_cp(self.root.get_screen('main').ids.cp.text)

        id_direccion = insertar_direccion(self.root.get_screen('main').ids.tipo_via.text,
                                          self.root.get_screen('main').ids.direccion.text, id_cp,
                                          self.root.get_screen('main').ids.numero.text)

        id_corrdenadas = insertarCoordenadas(self.root.get_screen('main').ids.map_view.lat,
                                             self.root.get_screen('main').ids.map_view.lon)

        actualizar_coordenadas_direccion(id_direccion, id_corrdenadas)

        quedada = Quedada(None, self.root.get_screen('main').ids.nombre.text,
                          self.root.get_screen('main').ids.descripcion.text, self.user.id, self.fecha, self.hora,
                          id_direccion, self.root.get_screen('main').ids.max_personas.text, 0, 1, self.ruta_imagen)

        idQuedada = quedada.insertar_quedada()
        self.reset_and_go_to_first_screen()
        if self.ruta_imagen != None:
            Quedada.updateFotoQuedada(idQuedada, self.ruta_imagen)

        # Actualizar la pantalla de quedadas
        self.on_start()

    def file_manager_open(self):
        self.file_manager.show('/')

    def select_path(self, path):
        self.exit_manager()
        # ver en que pantalla esta y si esta en main llamar a select_path_crear_quedada y si esta en info_quedada llamar a select_path_info_quedada
        if self.root.current == 'main':
            self.select_path_crear_quedada(path)
        if self.root.current == 'ver_quedada':
            self.select_path_info_quedada(path)

    def select_path_crear_quedada(self, path):
        self.exit_manager()
        self.upload_image_to_server_and_save_to_db(path)

    def exit_manager(self, *args):
        self.file_manager.close()

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
        self.ruta_imagen = ruta_imagen


####### LOGIN ##########################################################################################################

    def login(self):
        self.root.get_screen('login').ids.error_password.opacity = 0
        self.root.get_screen('login').ids.error_username.opacity = 0
        if self.root.get_screen('login').ids.username.text == "" or self.root.get_screen(
                'login').ids.password.text == "":
            anim = Animation(x=self.root.get_screen('login').ids.btn_login.x + 10, duration=0.1) + Animation(
                x=self.root.get_screen('login').ids.btn_login.x - 10,
                duration=0.1)
            anim.repeat = 3
            anim.start(self.root.get_screen('login').ids.btn_login)
            return
        else:
            username = self.root.get_screen('login').ids.username.text
            password = self.root.get_screen('login').ids.password.text

            # Comprobar si el usuario y la contraseña son correctos Usando la clase User
            temp_user = User(None, None, None, None, None, None)
            validated_user = temp_user.validate_user(username, encrypt_password(password))
            if validated_user:
                print("Inicio de sesión correcto")
                self.user = validated_user  # Guarda el usuario validado en self.user
                self.root.current = 'main'
                self.mostrar_historial()
            else:
                self.root.get_screen('login').ids.error_username.opacity = 100

####### REGISTRO #######################################################################################################

    def next1_singin(self):

        if not self.root.get_screen('singin').ids.nombre.text or not self.root.get_screen('singin').ids.apellidos.text or not self.root.get_screen('singin').ids.username.text:
            # Si alguno de los campos está vacío, agitar el botón y salir del método
            anim = Animation(x=self.root.get_screen('singin').ids.nombre.x + 10, duration=0.1) + Animation(x=self.root.get_screen('singin').ids.nombre.x - 10, duration=0.1)
            anim.repeat = 3
            anim.start(self.root.get_screen('singin').ids.next1)
            return
        if exist_user(self.root.get_screen('singin').ids.username.text):
            self.root.get_screen('singin').ids.error_username.opacity = 100
            return
        else:
            self.root.get_screen('singin').ids.error_username.opacity = 0


        self.root.get_screen('singin').ids.slide.load_next(mode="next")
        self.root.get_screen('singin').ids.icon1_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.get_screen('singin').ids.progress1)
        self.root.get_screen('singin').ids.icon1_progreso.icon = "check-circle"

    def next2_singin(self):

        if not self.root.get_screen('singin').ids.email.text or not self.root.get_screen('singin').ids.telefono.text or not self.root.get_screen('singin').ids.cp.text:
            # Si alguno de los campos está vacío, agitar el botón y salir del método
            anim = Animation(x=self.root.get_screen('singin').ids.nombre.x + 10, duration=0.1) + Animation(x=self.root.get_screen('singin').ids.nombre.x - 10,duration=0.1)
            anim.repeat = 3
            anim.start(self.root.get_screen('singin').ids.next2)
            return
        if not validate_email(self.root.get_screen('singin').ids.email.text):
            self.root.get_screen('singin').ids.error_email.opacity = 100
            return
        else:
            self.root.get_screen('singin').ids.error_email.opacity = 0
        if not is_valid_phone_number(self.root.get_screen('singin').ids.telefono.text):
            self.root.get_screen('singin').ids.error_telefono.opacity = 100
            return
        else:
            self.root.get_screen('singin').ids.error_telefono.opacity = 0
        if not is_valid_cp(self.root.get_screen('singin').ids.cp.text):
            self.root.get_screen('singin').ids.error_cp.opacity = 100
            return
        else:
            self.root.get_screen('singin').ids.error_cp.opacity = 0
        self.root.get_screen('singin').ids.slide.load_next(mode="next")
        self.root.get_screen('singin').ids.icon2_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.get_screen('singin').ids.progress2)
        self.root.get_screen('singin').ids.icon2_progreso.icon = "check-circle"

    def previous1_singin(self):
        self.root.get_screen('singin').ids.slide.load_previous()
        color = self.check_theme()
        self.root.get_screen('singin').ids.icon1_progreso.text_color = color,color,color,1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.get_screen('singin').ids.progress1)
        # poner el icon1_progreso en blanco
        self.root.get_screen('singin').ids.icon1_progreso.icon = "information"

    def previous2_singin(self):
        self.root.get_screen('singin').ids.slide.load_previous()
        color = self.check_theme()
        self.root.get_screen('singin').ids.icon2_progreso.text_color = color,color,color,1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.get_screen('singin').ids.progress2)
        self.root.get_screen('singin').ids.icon2_progreso.icon = "map-marker"

    def comprobarContraseñas(self):
        if is_valid_password(self.root.get_screen('singin').ids.password.text):
            self.root.get_screen('singin').ids.error_password.opacity = 0
        else:
            self.root.get_screen('singin').ids.error_password.opacity = 100
            return

        if self.root.get_screen('singin').ids.password.text != self.root.get_screen('singin').ids.confirm_password.text:
            self.root.get_screen('singin').ids.error_confirm_password.opacity = 100
            return
        else:
            self.root.get_screen('singin').ids.error_confirm_password.opacity = 0

        id_user = registrar(self.root.get_screen('singin').ids.email.text, self.root.get_screen('singin').ids.password.text, self.root.get_screen('singin').ids.username.text,
                  self.root.get_screen('singin').ids.nombre.text, self.root.get_screen('singin').ids.apellidos.text, self.root.get_screen('singin').ids.cp.text, self.root.get_screen('singin').ids.telefono.text)

        self.user= User(None, None, None, None, None, id_user).get_user()

        self.root.current = 'main'


############# VER DETALLES QUEDADA #####################################################################################
    def obtener_coordenadas(self):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT 
                    c.latitud, c.longitud
                FROM
                    Coordenadas c
                        JOIN
                    Direccion d ON c.id_coordenadas = d.coordenadas
                        JOIN
                    Quedada q ON d.id_direccion = q.direccion
                WHERE
                    q.id_quedada = %s
            """,
            (self.current_id_quedada,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result  # Retorna una tupla (latitud, longitud) o None si no se encontraron coordenadas

#Metodo que se ejecuta al iniciar la aplicacion para colocar los datos de la quedada
    def on_view_quedadas_button_press(self,instance):
        parent_card = instance.parent.parent.parent
        card_data = parent_card.data
        self.current_id_quedada = card_data['id']
        if self.user is None:
            print("Por favor, inicia sesión para ver las quedadas.")
            return
        # Comprueba si la pantalla 'ver_quedada' ya existe
        if 'ver_quedada' not in self.root.screen_names:
            # Si no existe, añádela
            self.root.add_widget(Builder.load_file('infoQuedadas.kv'))

        infoQuedada = Quedada2.get_by_id(self.current_id_quedada)

        coords = self.obtener_coordenadas()
        if coords is not None:
            lat, lon = coords
            lat = float(lat)
            lon = float(lon)
            # Accede al mapa
            map_view = self.root.get_screen('ver_quedada').ids.map_view

            # Centra el mapa en las coordenadas obtenidas
            map_view.center_on(lat, lon)

            # Si quieres añadir un marcador en las coordenadas puedes usar la función change_marker
            marker_text = "Your Marker Text"  # Cambia esto por el texto que quieras mostrar en el marcador
            self.current_marker = change_marker(map_view, lat, lon, marker_text)

        self.display_quedada(infoQuedada)

        # Carga las fotos para la quedada
        self.load_photos_for_quedada(self.current_id_quedada)

        # Verifica el estado de inscripción del usuario
        self.check_user_signup_status(self.user.id, self.current_id_quedada)

        # Cambia a la pantalla 'ver_quedada'
        self.root.current = 'ver_quedada'

        # Programa el cambio de diapositiva
        Clock.schedule_interval(self.change_slide, 3)  # Cambia de diapositiva cada 3 segundos

#Metodo que muestra la informacion de la quedada en la pantalla
    def display_quedada(self, quedada):

        # Actualiza los widgets con la información de la quedada
        self.root.get_screen('ver_quedada').ids.nombre.text += quedada.nombre
        self.root.get_screen('ver_quedada').ids.descripcion.text += quedada.descripcion
        self.root.get_screen('ver_quedada').ids.user_organiza.text += f"{quedada.organizador_nombre} {quedada.organizador_apellidos}"
        self.root.get_screen('ver_quedada').ids.fecha.text += str(quedada.fecha)
        self.root.get_screen('ver_quedada').ids.hora.text += str(quedada.hora)
        self.root.get_screen('ver_quedada').ids.direccion.text += f"{quedada.tipo_via} {quedada.direccion}, {quedada.cp}"
        self.root.get_screen('ver_quedada').ids.max_personas.text += str(quedada.max_personas)
        self.root.get_screen('ver_quedada').ids.numero_personas.text += str(quedada.numero_personas)

#Actualiza la galeria de fotos para que se vayan mostrando
    def change_slide(self, dt):
        carrousel = self.root.get_screen('ver_quedada').ids.carousel
        if carrousel.index == len(carrousel.slides) - 1:
            carrousel.index = 0
        else:
            carrousel.load_next()
#Metodo que permite almacenar la ruta del archivo
    def select_path_info_quedada(self, path):
        self.exit_manager()
        self.add_image_to_carousel(path)
        self.upload_image_to_server_and_save_to_db_info(path)
    def clear_carousel(self):
        # Obtener el carrusel
        carousel = self.root.get_screen('ver_quedada').ids.carousel

        # Limpiar el carrusel
        carousel.clear_widgets()
#Metodo que añade una imagen al carrusel y la sube al servidor
    def add_image_to_carousel(self, image_path):
        # Crear una nueva imagen
        new_image = AsyncImage(source=image_path)

        # Añadir la nueva imagen al carrusel
        self.root.get_screen('ver_quedada').ids.carousel.add_widget(new_image)

        # Actualizar el carrusel para mostrar la nueva imagen
        self.root.get_screen('ver_quedada').ids.carousel.index = len(
            self.root.get_screen('ver_quedada').ids.carousel.slides) - 1
#Metodo que sube la imagen al servidor y la guarda en la base de datos
    def upload_image_to_server_and_save_to_db_info(self, path):
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
                       (self.current_id_quedada, self.user.id, ruta_imagen))
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
            self.root.get_screen('ver_quedada').ids.carousel.add_widget(default_image)
        else:
            for foto in fotos:
                enlace_foto = foto[0]
                image = AsyncImage(source=enlace_foto)
                self.root.get_screen('ver_quedada').ids.carousel.add_widget(image)
#Metodo que permite inscribirse o desapuntarse de una quedada
    def toggle_sign_up(self, instance):
        if instance.text == 'Inscribirse':
            print("Intentando inscribirse...")
            if not self.check_if_user_is_registered(self.user.id, self.current_id_quedada):
                instance.text = 'Desapuntarse'
                instance.md_bg_color = (1, 0, 0, 1)  # Rojo
                resultado = Quedada2.unirse(self.user.id,self.current_id_quedada)  # Suponiendo que 6 es el user_id del usuario actual
                print(f"Resultado de inscribirse: {resultado}")
                # Incrementar el número de personas en la quedada
                num_personas = int(self.root.get_screen('ver_quedada').ids.numero_personas.text.split(": ")[1])
                self.root.get_screen('ver_quedada').ids.numero_personas.text = "Número de personas: " + str(
                    num_personas + 1)
            else:
                print("El usuario ya está inscrito.")
        else:
            self.show_confirm_dialog(instance)
            # Decrementar el número de personas en la quedada

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
                        on_release=lambda x: self.unsign_user(instance),
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
        resultado = Quedada2.desapuntarse(self.user.id, self.current_id_quedada)  # Suponiendo que 6 es el user_id del usuario actual
        print(f"Resultado de desapuntarse: {resultado}")
        # Decrementar el número de personas en la quedada
        num_personas = int(self.root.get_screen('ver_quedada').ids.numero_personas.text.split(": ")[1])
        self.root.get_screen('ver_quedada').ids.numero_personas.text = "Número de personas: " + str(num_personas - 1)
        self.close_dialog(None)

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
            signup_button = self.root.get_screen('ver_quedada').ids.signup_button
            signup_button.text = 'Desapuntarse'
            signup_button.md_bg_color = (1, 0, 0, 1)  # Rojo
if __name__ == '__main__':
    MyApp().run()