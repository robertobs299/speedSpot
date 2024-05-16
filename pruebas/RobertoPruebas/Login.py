import hashlib
import secrets

from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pruebas.RobertoPruebas import conexion
import kivymd
print(kivymd.__version__)



KV = """
MDFloatLayout:
    MDLabel:
        text: 'Iniciar Sesión'
        halign: 'center'
        pos_hint: {'center_x':0.5, 'center_y':0.7}
        font_name: 'Roboto-Bold'
        font_size: "40sp"
    MDFloatLayout:
        size_hint: .85, .08
        pos_hint: {"center_x": .5, "center_y": .38}
        canvas:
            Color:
                rgb: (238/255, 238/255, 238/255, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [25]
        TextInput:
            id: username
            hint_text: "Nombre de Usuario"
            size_hint: 1, None
            pos_hint: {"center_x": .5, "center_y": .5}
            height: self.minimum_height
            multiline: False
            cursor_color: 96/255, 74/255, 215/255, 1
            cursor_width: "2sp"
            foreground_color: 96/255, 74/255, 215/255, 1
            background_color: 0, 0, 0, 0
            padding: 15
            font_name: "Roboto-Bold"
            font_size: "16sp"
        MDLabel:
            id: error_username
            text: "Usuario no encontrado"
            pos_hint: {"center_x": .45, "center_y": .5}
            halign: "center"
            theme_text_color: "Error"
            opacity: 0    
    MDFloatLayout:
        size_hint: .85, .08
        pos_hint: {"center_x": .5, "center_y": .28}
        canvas:
            Color:
                rgb: (238/255, 238/255, 238/255, 1)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [25]
        TextInput:
            id: password
            hint_text: "Contraseña"
            password: True
            size_hint: 1, None
            pos_hint: {"center_x": .5, "center_y": .5}
            height: self.minimum_height
            multiline: False
            cursor_color: 96/255, 74/255, 215/255, 1
            cursor_width: "2sp"
            foreground_color: 96/255, 74/255, 215/255, 1
            background_color: 0, 0, 0, 0
            padding: 15
            font_name: "Roboto-Bold"
            font_size: "16sp"
        MDLabel:
            id: error_password
            text: "Contraseña incorrecta"
            pos_hint: {"center_x": .45, "center_y": .5}
            halign: "center"
            theme_text_color: "Error"
            opacity: 0    
    MDTextButton:
        text: '¿Has olvidado tu contraseña?'
        theme_text_color: "Custom"
        text_color: 96/255, 74/255, 215/255, 1
        pos_hint: {"center_x": .5, "center_y": .21}
        on_release: app.forgot_password()
    Button:
        id: btn_login
        text: "LOGIN"
        font_name: "Roboto-Bold"
        font_size: "20sp"
        size_hint: .5, .08
        pos_hint: {"center_x": .5, "center_y": .12}
        background_color: 0, 0, 0, 0
        canvas.before:
            Color:
                rgb: app.theme_cls.primary_color
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [23]
        on_release: app.login()
"""

def encrypt_password(password):
    # Convertir la contraseña a bytes
    password_bytes = password.encode('utf-8')

    # Calcular el hash SHA256 de la contraseña
    password_hash = hashlib.sha256(password_bytes).hexdigest()

    return password_hash

def generate_temp_password():
    return secrets.token_hex(10)

def forgot_password(user_email):
    # Generar el token de restablecimiento de contraseña
    temp_password = generate_temp_password()

    # Almacenar el token de restablecimiento de contraseña en la base de datos
    # Aquí necesitarás escribir el código para almacenar el token en la base de datos

    # Enviar el correo electrónico de restablecimiento de contraseña
    send_temp_password_email(user_email, temp_password)


def send_temp_password_email(user_email, temp_password):
    # Configurar el servidor SMTP
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login('speedspot10@gmail.com', 'Ballesta123')

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = 'speedspot10@gmail.com'
    msg['To'] = user_email
    msg['Subject'] = 'Password Reset Request'
    body = f'Your temporary password is: {temp_password}\nPlease change your password the next time you log in.'
    msg.attach(MIMEText(body, 'plain'))

    # Enviar el correo electrónico
    smtp_server.send_message(msg)
    smtp_server.quit()
class Login(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        return Builder.load_string(KV)

    def login(self):
        self.root.ids.error_password.opacity = 0
        self.root.ids.error_username.opacity = 0
        if self.root.ids.username.text == "" or self.root.ids.password.text == "":
            anim = Animation(x=self.root.ids.btn_login.x + 10, duration=0.1) + Animation(x=self.root.ids.btn_login.x - 10,
                                                                                      duration=0.1)
            anim.repeat = 3
            anim.start(self.root.ids.btn_login)
            return
        else:
            username = self.root.ids.username.text
            password = self.root.ids.password.text
            conn = conexion.connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT username, password FROM Login WHERE username = %s", (username,))

            result = cursor.fetchone()
            conn.close()
            password = encrypt_password(password)
            if result:
                username, password_hash = result
                if password_hash == password:
                    print("Inicio de sesión correcto")
                else:
                    self.root.ids.error_password.opacity = 100
            else:
                self.root.ids.error_username.opacity = 100

    def forgot_password(self):
        # Obtener el correo electrónico del usuario
        conn = conexion.connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM User JOIN Login on User.id_user = Login.id_user = Login.id_user WHERE Login.username = %s", (self.root.ids.username.text,))
        if (result := cursor.fetchone()):
            user_email = result[0]
        else:
            print("Usuario no encontrado")
            return

        # Enviar el correo electrónico de restablecimiento de contraseña
        forgot_password(user_email)
if __name__ == '__main__':
    Login().run()