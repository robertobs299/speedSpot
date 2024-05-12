import hashlib
import re
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout

from pruebas.RobertoPruebas import conexion


def validate_email(email):
    pattern = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    match = pattern.fullmatch(email)
    return bool(match)
def is_valid_password(password):
    # Define la expresión regular para validar la contraseña
    password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@$!%*?&]{8,}$')
    return bool(password_regex.match(password))
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
        show_popup("Usuario no encontrado")

def show_popup(text):
    popup = Popup(title='Mensaje', content=Label(text=text), size_hint=(None, None),
                          size=(400, 200))
    popup.open()
class registroScreen(BoxLayout):


    def get_postal_codes(self):
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT cp FROM postal_code")
        result = cursor.fetchall()
        conn.close()

        # Extrae las cadenas de la tupla resultante
        postal_codes = [row[0] for row in result]

        print(postal_codes)
        return postal_codes

    def registrar(self,email, password, confirm_password, username,name, surname, postalcode, phone, sexo,):
        errores = ""
        if email == '' or password == '' or username == '' or name == '' or surname == '' or postalcode == '' or phone == '' or sexo == '':
            errores += "Todos los campos son obligatorios\n"
        if not validate_email(email):
            errores += "El correo electrónico no es válido\n"
        if not is_valid_password(password):
            errores += "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una minúscula, un número y un carácter especial\n"
        if confirm_password != password:
            errores += "Las contraseñas no coinciden\n"
        if not is_valid_phone_number(phone):
            errores += "El número de teléfono no es válido\n"
        if exit_user(username):
            errores += "El nombre de usuario ya existe\n"
        # la idea es recoger los errores y mostrarlos en un popup
        if sexo == "Hombre":
            sexo = "H"
        elif sexo == "Mujer":
            sexo = "M"
        else:
            sexo = "O"

        if errores != "":
            show_popup(errores)
        else:
            encrypted_password = hashlib.sha256(password.encode()).hexdigest()

            # Conexión a la base de datos
            conn = conexion.connect_to_database()
            cursor = conn.cursor()

            # Buscar el ID del código postal
            cursor.execute("SELECT id_cp FROM postal_code WHERE cp LIKE %s", (str(postalcode),))
            result = cursor.fetchone()  # Obtener el resultado de la consulta

            if result:
                idCp = result[0]  # Obtener el ID del código postal
            else:
                # Si no se encuentra el código postal, puedes manejar el error aquí
                print("El código postal no existe en la base de datos")
                conn.close()
                print(result)

            # Calcular el hash de la contraseña
            encrypted_password = hashlib.sha256(password.encode()).hexdigest()

            # Insertar el usuario en la tabla User
            cursor.execute(
                "INSERT INTO User (email, nombre, apellidos, cp, telefono, sexo) VALUES (%s, %s, %s, %s, %s, %s)",
                (email, name, surname, idCp, phone, sexo))

            iduser = cursor.lastrowid

            # Insertar los datos de inicio de sesión en la tabla Login
            cursor.execute("INSERT INTO Login (id_user, username, password) VALUES (%s, %s, %s)",
                           (iduser, username, encrypted_password))

            # Confirmar los cambios y cerrar la conexión
            conn.commit()
            conn.close()
            show_popup("Registrado con exito")

class loginScreen(BoxLayout):
    def login(self, username, password):
        encrypted_password = hashlib.sha256(password).hexdigest()

        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id_user, password FROM Login WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            id_user, password_hash = result
            if password_hash == encrypted_password:
                show_popup("Inicio de sesión correcto")
            else:
                show_popup("Contraseña incorrecta")
        else:
            show_popup("Usuario no encontrado")

class mainScreen(BoxLayout):
    pass

class Registro(MDApp):
    def login(self, username, password):

        password_bytes = password.encode('utf-8')
        encrypted_password = hashlib.sha256(password_bytes).hexdigest()

        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id_user, password FROM Login WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            id_user, password_hash = result
            if password_hash == encrypted_password:
                print("Inicio de sesión correcto")
            else:
                print("Contraseña incorrecta")
        else:
            print("Usuario no encontrado")

Registro().run()


#Ejemplo pasar a ptra pantalla
#----------------------------------------------------------------------------
# name: 'principalScreen'
#         BoxLayout:
#             orientation: 'vertical'
#             Label:
#                 text: 'Principal Screen'
#             Button:
#                 text: 'Go to second screen'
#                 on_press: root.manager.current = 'secondScreen'
#         <secondScreen>:
#             name: 'secondScreen'
#             BoxLayout:
#                 orientation: 'vertical'
#                 Label:
#                     text: 'Second Screen'
#                 Button:
#                     text: 'Go to principal screen'
#                     on_press: root.manager.current = 'principalScreen'
