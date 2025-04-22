from textual.app import App
from textual.widgets import Static, Footer
from textual.containers import Container

class TextualApp(App):

    DEFAULT_CSS = """
    #my_container { align: center middle; }
    #my_static { background: blue; width: 40; height: 15; }
    """
    
    def compose(self):

        self.my_static = Static("Hello, Textual! great day eh", id="my_static")
        self.my_static.loading = True
        with Container(id="my_container"):
            yield self.my_static
        yield Footer()

    def on_ready(self):
        self.set_timer(2, lambda: setattr(self.my_static, "loading", False))

TextualApp().run()