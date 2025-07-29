from textual.app import App, ComposeResult
from textual.widgets import Static, Footer


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    """

    BINDINGS = [
        ("b", "binding", "My Binding Foo"),
    ]

    def compose(self) -> ComposeResult:

        yield Static("Hello, Textual!", id="my_static")
        yield Footer()

    def action_binding(self) -> None:
        self.notify("You pressed the 'b' key!")

TextualApp().run()
