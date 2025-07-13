from textual.app import App
from textual.widgets import Static, Footer


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    """

    BINDINGS = [
        ("b", "binding", "My Binding Foo"),
    ]

    def compose(self):

        yield Static("Hello, Textual!", id="my_static")
        yield Footer()

    def action_binding(self):
        self.notify("You pressed the 'b' key!")

TextualApp().run()
