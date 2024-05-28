from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class ConfigScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class SpeedSpotApp(App):
    def build(self):
        return Builder.load_file("C:/Users/luism/PycharmProjects/speedSpot/pruebas/LuismiPruebas/prueba.kv")

    def open_config_screen(self):
        self.root.current = 'config'

    def go_back_to_main_screen(self):
        self.root.current = 'main'

if __name__ == '__main__':
    SpeedSpotApp().run()
