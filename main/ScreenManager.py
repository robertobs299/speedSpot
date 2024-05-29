import re

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.bubble import Bubble
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivymd.uix.pickers import MDTimePicker, MDDatePicker
from main.Clases.Quedada import Quedada
import hashlib
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
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
    historial_list = []
    dark_theme = True
    def build(self):
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
            # source="moto.jpg",  # Reemplazar con quedada.imagen_url si se tiene la URL de la imagen
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

        self.root.get_screen('main').ids.card_list.add_widget(card)
        self.root.get_screen('main').ids.card_list.height += card.height + dp(15)  # Update height of BoxLayout

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
        historial_container = self.root.get_screen('main').ids.historial_list
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


######### CREAR QUEDADA ################################################################################################
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
        self.root.get_screen('main').ids.slide.load_next(mode="next")
        self.root.get_screen('main').ids.icon1_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.get_screen('main').ids.progress1)
        self.root.get_screen('main').ids.icon1_progreso.icon = "check-circle"

    def next2(self):
        if not self.root.get_screen('main').ids.cp.text or not self.root.get_screen('main').ids.direccion.text or not self.root.get_screen('main').ids.numero.text:
            # Si alguno de los campos está vacío, agitar el botón y salir del método
            anim = Animation(x=self.root.get_screen('main').ids.nombre.x + 10, duration=0.1) + Animation(x=self.root.get_screen('main').ids.nombre.x - 10,
                                                                                      duration=0.1)
            anim.repeat = 3
            anim.start(self.root.get_screen('main').ids.next2)
            return

        self.root.get_screen('main').ids.slide.load_next(mode="next")
        self.root.get_screen('main').ids.icon2_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.get_screen('main').ids.progress2)
        self.root.get_screen('main').ids.icon2_progreso.icon = "check-circle"

    def previous1(self):
        self.root.get_screen('main').ids.slide.load_previous()
        self.root.get_screen('main').ids.icon1_progreso.text_color = 1,1,1,1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.get_screen('main').ids.progress1)
        self.root.get_screen('main').ids.icon1_progreso.icon = "numeric-1-circle"

    def previous2(self):
        self.root.get_screen('main').ids.slide.load_previous()
        self.root.get_screen('main').ids.icon2_progreso.text_color = 1,1,1, 1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.get_screen('main').ids.progress2)
        self.root.get_screen('main').ids.icon2_progreso.icon = "numeric-2-circle"

    def crear_quedada(self):
        id_cp = obtener_id_cp(self.root.get_screen('main').ids.cp.text)

        id_direccion = insertar_direccion(self.root.get_screen('main').ids.tipo_via.text, self.root.get_screen('main').ids.direccion.text, id_cp,
                                          self.root.get_screen('main').ids.numero.text)

        id_corrdenadas = insertarCoordenadas(self.root.get_screen('main').ids.map_view.lat, self.root.get_screen('main').ids.map_view.lon)

        actualizar_coordenadas_direccion(id_direccion, id_corrdenadas)

        quedada = Quedada(None, self.root.get_screen('main').ids.nombre.text, self.root.get_screen('main').ids.descripcion.text, 1, self.fecha, self.hora,
                          id_direccion, self.root.ids.max_personas.text, 0, 1)

        quedada.insertar_quedada()

####### LOGIN ##########################################################################################################

    def login(self):
        self.root.get_screen('login').ids.error_password.opacity = 0
        self.root.get_screen('login').ids.error_username.opacity = 0
        if self.root.get_screen('login').ids.username.text == "" or self.root.get_screen('login').ids.password.text == "":
            anim = Animation(x=self.root.get_screen('login').ids.btn_login.x + 10, duration=0.1) + Animation(x=self.root.get_screen('login').ids.btn_login.x - 10,
                duration=0.1)
            anim.repeat = 3
            anim.start(self.root.get_screen('login').ids.btn_login)
            return
        else:
            username = self.root.get_screen('login').ids.username.text
            password = self.root.get_screen('login').ids.password.text

            # Comprobar si el usuario y la contraseña son correctos Usando la clase User
            user = User(None, None, None, None, None, None)
            user = user.validate_user(username, encrypt_password(password))
            if user:
                print("Inicio de sesión correcto")
                #Obtener datos del usuario
                self.root.current = 'main'
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
        self.root.get_screen('singin').ids.icon1_progreso.text_color = 1,1,1,1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.get_screen('singin').ids.progress1)
        # poner el icon1_progreso en blanco
        self.root.get_screen('singin').ids.icon1_progreso.icon = "numeric-1-circle"

    def previous2_singin(self):
        self.root.get_screen('singin').ids.slide.load_previous()
        self.root.get_screen('singin').ids.icon2_progreso.text_color = 1,1,1,1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.get_screen('singin').ids.progress2)
        self.root.get_screen('singin').ids.icon2_progreso.icon = "numeric-2-circle"

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

        registrar(self.root.get_screen('singin').ids.email.text, self.root.get_screen('singin').ids.password.text, self.root.get_screen('singin').ids.username.text,
                  self.root.get_screen('singin').ids.nombre.text, self.root.get_screen('singin').ids.apellidos.text, self.root.get_screen('singin').ids.cp.text, self.root.get_screen('singin').ids.telefono.text)
        self.root.current = 'main'




if __name__ == '__main__':
    MyApp().run()

