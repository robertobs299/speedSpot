from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image

KV = """
MDFloatLayout:
    Image:
        source: 'C:/Users/Roberto/PycharmProjects/speedSpot/imagenes/img.png'
        allow_stretch: True
        keep_ratio: False
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
    MDTextButton:
        text: '¿Has olvidado tu contraseña?'
        theme_text_color: "Custom"
        text_color: 96/255, 74/255, 215/255, 1
        pos_hint: {"center_x": .5, "center_y": .21}
    Button:
        text: "LOGIN"
        font_name: "Roboto-Bold"
        font_size: "20sp"
        size_hint: .5, .08
        pos_hint: {"center_x": .5, "center_y": .12}
        background_color: 0, 0, 0, 0
        canvas.before:
            Color:
                rgb: 246/255, 135/255, 177/255, 1
            RoundedRectangle:
                size: self.size
                pos: self-pos
                radius: [23]
                    
        
        

"""


class Login(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    Login().run()
