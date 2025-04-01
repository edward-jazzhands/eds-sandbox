from textual.app import App
from textual.widgets import Static
from textual.containers import Container

from PIL import Image
from rich_pixels import Pixels


class MyApp(App):

    def compose(self):

        with Image.open("my_image.jpg") as image:
            pixels = Pixels.from_image(image)        

        with Container():
            yield Static(pixels)

MyApp().run()