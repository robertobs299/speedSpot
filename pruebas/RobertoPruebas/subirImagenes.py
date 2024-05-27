import paramiko
from kivy.lang import Builder
from kivymd.app import MDApp
from plyer import filechooser
from pruebas.RobertoPruebas import conexion

from kivy.core.image import Image as CoreImage
from io import BytesIO
import urllib.request

def load_image_from_url(url):
    with urllib.request.urlopen(url) as response:
        img_data = response.read()
    img = CoreImage(BytesIO(img_data), ext='png')
    return img.texture

KV = '''
MDFloatLayout:
    Image:
        id: image
        source: ""
        size_hint: None, None
        size: "300dp", "300dp"
        pos_hint: {"center_x": .5, "center_y": .7}
    MDRaisedButton:
        text: "Subir imagen"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.file_chooser()
 '''
# Establecer la conexión SSH


# Ruta local de la imagen a subir
# ruta_imagen_local = '/home/roberto.bermudez@ad.minderest.com/Descargas/2024-05-27_10-02_1.png'
#
# # Ruta remota donde se guardará la imagen en el servidor
# ruta_imagen_remota = '/var/www/html/2024-05-27_10-02_1.png'
#
# # Subir la imagen al servidor
# with ssh_client.open_sftp() as sftp:
#     sftp.put(ruta_imagen_local, ruta_imagen_remota)

# Cerrar la conexión SSH


def replace_backslashes(path):
    return path.replace("\\", "/")

class FileChooser(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        return Builder.load_string(KV)

    def file_chooser(self):

        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname='165.227.130.67', port=22, username='root', password='Ballesta123?Rata')

            ruta_imagen_local = replace_backslashes(selection[0])
            ruta_imagen_remota = '/var/www/html/' + ruta_imagen_local.split('/')[-1]
            with ssh_client.open_sftp() as sftp:
                sftp.put(ruta_imagen_local, ruta_imagen_remota)
            ssh_client.close()

            ruta_imagen = 'http://165.227.130.67/' + ruta_imagen_local.split('/')[-1]
            conn = conexion.connect_to_database()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Fotos_quedada (quedada_id, user_id, enlace_foto) VALUES (%s,%s,%s)", (10, 1, ruta_imagen,))
            conn.commit()
            cursor.close()

            ruta_ver_imagen = 'http://165.227.130.67/2024-05-27_10-02_1.png'
            self.root.ids.image.texture = load_image_from_url(ruta_ver_imagen)

# http://165.227.130.67/2024-05-27_10-02_1.png

if __name__ == '__main__':
    FileChooser().run()