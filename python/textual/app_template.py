from textual.app import App
from textual.widgets import Static, Footer, Button
from textual.containers import Container

class TextualApp(App):

    DEFAULT_CSS = """
    Screen { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    """
    
    def compose(self):

        with Container(id="my_container"):
            yield Static("Hello, Textual!", id="my_static")
            yield Button("press me")

        yield Footer()

    def on_button_pressed(self):
        self.log(self.screen._compositor.render_update(full=True))


TextualApp().run()