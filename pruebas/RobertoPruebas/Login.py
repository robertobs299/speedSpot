import hashlib
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from main.Clases.User import User


def encrypt_password(password):
    # Convertir la contraseña a bytes
    password_bytes = password.encode('utf-8')
    # Calcular el hash SHA256 de la contraseña
    password_hash = hashlib.sha256(password_bytes).hexdigest()
    return password_hash

class Login(Screen):
    def build(self):
        App.get_running_app().theme_cls.theme_style = "Dark"
        App.get_running_app().theme_cls.primary_palette = "Amber"
        Builder.load_file('Login.kv')

        return self

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

            # Comprobar si el usuario y la contraseña son correctos Usando la clase User
            user = User(None, None, None, None, None, None)
            user = user.validate_user(username, encrypt_password(password))
            if user:
                print("Inicio de sesión correcto")
                self.manager.current = 'main'
            else:
                self.root.ids.error_username.opacity = 100

#
# if __name__ == '__main__':
#     Login().run()