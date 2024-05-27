from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from pruebas.RobertoPruebas.main import MainApp
from pruebas.RobertoPruebas.Login import Login

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        main_screen = MainApp().build()  # Crea una instancia de MainApp y llama a su método build
        login_screen = Login().build()  # Crea una instancia de Login y llama a su método build

        sm.add_widget(main_screen)
        sm.add_widget(login_screen)

        main_screen.name = 'main'
        login_screen.name = 'login'

        sm.current = 'login'  # Establece la pantalla de inicio de sesión como la pantalla actual
        return sm

if __name__ == '__main__':
    MyApp().run()