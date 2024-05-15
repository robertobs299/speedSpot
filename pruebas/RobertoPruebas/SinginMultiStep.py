import hashlib

from kivy.animation import Animation
from kivymd.app import  MDApp
from kivy.lang import Builder
import re

from pruebas.RobertoPruebas import conexion

KV = """
MDFloatLayout:
    MDCard:
        size_hint: 1, 1
        pos_hint: {"center_x": .5, "center_y": .5}
        Carousel:
            id: slide
            MDFloatLayout:
                MDTextField:
                    id: nombre
                    hint_text: "Nombre"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    size_hint_x: .8
                MDTextField:
                    id: apellidos
                    hint_text: "Apellidos"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    size_hint_x: .8
                MDTextField:
                    id: username
                    hint_text: "Nombre de Usuario"
                    pos_hint: {"center_x": .5, "center_y": .3}
                    size_hint_x: .8
                MDLabel:
                    id: error_username
                    text: "El nombre de usuario ya existe"
                    pos_hint: {"center_x": .5, "center_y": .25}
                    halign: "center"
                    theme_text_color: "Error"
                    opacity: 0
                MDRaisedButton:
                    id: next1
                    text: "Siguiente"
                    pos_hint: {"center_x": .5, "center_y": .2}
                    size_hint_x: .8
                    on_release: app.next1()
            
            MDFloatLayout:
                MDTextField:
                    id: email
                    hint_text: "Email"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    size_hint_x: .8
                MDLabel:
                    id: error_email
                    text: "El correo electrónico no es válido"
                    pos_hint: {"center_x": .5, "center_y": .45}
                    halign: "center"
                    theme_text_color: "Error"
                    opacity: 0
                MDTextField:
                    id: telefono
                    hint_text: "Numero de Telefono"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    size_hint_x: .8
                MDLabel:
                    id: error_telefono
                    text: "El número de teléfono no es válido"
                    pos_hint: {"center_x": .5, "center_y": .35}
                    halign: "center"
                    theme_text_color: "Error"
                    opacity: 0
                MDTextField:
                    id: cp
                    hint_text: "Codigo Postal"
                    pos_hint: {"center_x": .5, "center_y": .3}
                    size_hint_x: .8 
                MDLabel:
                    id: error_cp
                    text: "El código postal no es válido"
                    pos_hint: {"center_x": .5, "center_y": .25}
                    halign: "center"         
                    theme_text_color: "Error" 
                    opacity: 0        
                MDRaisedButton:
                    text: "Anterior"
                    pos_hint: {"center_x": .3, "center_y": .2}
                    size_hint_x: .39
                    on_release: app.previous1()
                MDRaisedButton:
                    id: next2
                    text: "Siguiente"
                    pos_hint: {"center_x": .7, "center_y": .2}
                    size_hint_x: .39
                    on_release: app.next2()
            
            MDFloatLayout:
                MDTextField:
                    id: password
                    hint_text: "Contraseña"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    size_hint_x: .8
                    password: True
                MDLabel:
                    id: error_password
                    text: "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una minúscula, un número y un carácter especial"
                    pos_hint: {"center_x": .5, "center_y": .45}
                    halign: "center"
                    theme_text_color: "Error"
                    opacity: 0
                MDTextField:
                    id: confirm_password
                    hint_text: "Confirmar Contraseña"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    size_hint_x: .8
                    password: True
                MDLabel:
                    id: error_confirm_password
                    text: "Las contraseñas no coinciden"
                    pos_hint: {"center_x": .5, "center_y": .35}
                    halign: "center"
                    theme_text_color: "Error"
                    opacity: 0    
                MDRaisedButton:
                    text: "Anterior"
                    pos_hint: {"center_x": .3, "center_y": .2}
                    size_hint_x: .39
                    on_press: app.previous2()
                MDRaisedButton:
                    text: "Registrar"
                    pos_hint: {"center_x": .7, "center_y": .2}
                    size_hint_x: .39
                    on_release: app.comprobarContraseñas()   
    MDLabel:
        text: "Registro de Usuario"
        bold: True
        pos_hint: {"center_x": .8, "center_y": .8}    
        font_style: "H4" 
    MDFloatingActionButton:
        icon: "numeric-1-circle"
        pos_hint: {"center_x": .14, "center_y": .65}
        size_hint: .1, .1
        md_bg_color: app.theme_cls.primary_color
    MDProgressBar:
        id: progress1
        size_hint_x: .3
        size_hint_y: .015
        pos_hint: {"center_x": .315, "center_y": .65}
    
    MDIconButton:
        id: icon2_progreso
        icon: "numeric-2-circle"
        pos_hint: {"center_x": .5, "center_y": .65}
        user_font_size: "50sp"
        theme_text_color: "Custom"
    MDProgressBar:
        id: progress2
        size_hint_x: .3
        size_hint_y: .015
        pos_hint: {"center_x": .68, "center_y": .65}
        
    MDIconButton:
        id: icon3_progreso
        icon: "numeric-3-circle"
        pos_hint: {"center_x": .86, "center_y": .65}
        user_font_size: "50sp"
        theme_text_color: "Custom" 
        
"""

#Comprobaciones para el regsitro del usuario

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
    result = cursor.fetchone()
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
        "INSERT INTO User (email, nombre, apellidos, cp, telefono) VALUES (%s, %s, %s, %s, %s)",
        (email, name, surname, idCp, phone))

    iduser = cursor.lastrowid

    # Insertar los datos de inicio de sesión en la tabla Login
    cursor.execute("INSERT INTO Login (id_user, username, password) VALUES (%s, %s, %s)",
                   (iduser, username, encrypted_password))

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


class LoginMultiStep(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        return Builder.load_string(KV)

    def next1(self):

        if not self.root.ids.nombre.text or not self.root.ids.apellidos.text or not self.root.ids.username.text:
            # Si alguno de los campos está vacío, agitar el botón y salir del método
            anim = Animation(x=self.root.ids.nombre.x + 10, duration=0.1) + Animation(x=self.root.ids.nombre.x - 10, duration=0.1)
            anim.repeat = 3
            anim.start(self.root.ids.next1)
            return
        if exist_user(self.root.ids.username.text):
            self.root.ids.error_username.opacity = 100
            return
        else:
            self.root.ids.error_username.opacity = 0


        self.root.ids.slide.load_next(mode="next")
        self.root.ids.icon1_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.ids.progress1)
        self.root.ids.icon1_progreso.icon = "check-circle"

    def next2(self):

        if not self.root.ids.email.text or not self.root.ids.telefono.text or not self.root.ids.cp.text:
            # Si alguno de los campos está vacío, agitar el botón y salir del método
            anim = Animation(x=self.root.ids.nombre.x + 10, duration=0.1) + Animation(x=self.root.ids.nombre.x - 10,duration=0.1)
            anim.repeat = 3
            anim.start(self.root.ids.next2)
            return
        if not validate_email(self.root.ids.email.text):
            self.root.ids.error_email.opacity = 100
            return
        else:
            self.root.ids.error_email.opacity = 0
        if not is_valid_phone_number(self.root.ids.telefono.text):
            self.root.ids.error_telefono.opacity = 100
            return
        else:
            self.root.ids.error_telefono.opacity = 0
        if not is_valid_cp(self.root.ids.cp.text):
            self.root.ids.error_cp.opacity = 100
            return
        else:
            self.root.ids.error_cp.opacity = 0

        self.root.ids.slide.load_next(mode="next")
        self.root.ids.icon2_progreso.text_color = self.theme_cls.primary_color
        anim = Animation(value=100, duration=1)
        anim.start(self.root.ids.progress2)
        self.root.ids.icon2_progreso.icon = "check-circle"
    def previous1(self):
        self.root.ids.slide.load_previous()
        self.root.ids.icon1_progreso.text_color = 0,0,0,1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.ids.progress1)
        self.root.ids.icon1_progreso.icon = "numeric-1-circle"
    def previous2(self):
        self.root.ids.slide.load_previous()
        self.root.ids.icon2_progreso.text_color = 0,0,0,1
        anim = Animation(value=0, duration=1)
        anim.start(self.root.ids.progress2)
        self.root.ids.icon2_progreso.icon = "numeric-2-circle"

    def comprobarContraseñas(self):
        if is_valid_password(self.root.ids.password.text):
            self.root.ids.error_password.opacity = 0
        else:
            self.root.ids.error_password.opacity = 100
            return

        if self.root.ids.password.text != self.root.ids.confirm_password.text:
            self.root.ids.error_confirm_password.opacity = 100
            return
        else:
            self.root.ids.error_confirm_password.opacity = 0

        registrar(self.root.ids.email.text, self.root.ids.password.text, self.root.ids.username.text,
                  self.root.ids.nombre.text, self.root.ids.apellidos.text, self.root.ids.cp.text, self.root.ids.telefono.text)

if __name__ == "__main__":
    LoginMultiStep().run()


