from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from main.Clases.Quedada import Quedada

Builder.load_file('my.kv')

class MyCard(BoxLayout):
    pass

class MyScrollView(ScrollView):
    pass

class MainApp(MDApp):
    def build(self):
        scroll_view = MyScrollView()
        quedadas = Quedada.get_last_five()
        for quedada in quedadas:  # Reemplaza esto con tu propia lista de elementos
            card = MyCard()
            card.ids.title.text = quedada.nombre
            card.ids.description.text = quedada.descripcion
            scroll_view.ids.box_layout.add_widget(card)
        return scroll_view



MainApp().run()