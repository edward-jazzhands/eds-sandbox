from textual.app import App
from textual import on
from textual.worker import Worker
from textual.widgets import Static, Footer, Button
from textual.containers import Container

class TextualApp(App):

    DEFAULT_CSS = """
    #my_static { border: solid blue; width: auto;}
    """
    
    def compose(self):

        with Container(id="my_container"):
            yield Static("Hello, Textual!", id="my_static")
            yield Button("press me")

        yield Footer()


TextualApp().run()