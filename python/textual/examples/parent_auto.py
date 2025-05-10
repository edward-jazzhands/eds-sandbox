from textual.app import App
from textual.widgets import Static, Footer, Button
from textual.containers import Container


class TextualApp(App):

    DEFAULT_CSS = """
    Screen { align: center middle; }
    #my_container { align: center middle; border: solid red; }
    #sub_container {
        align: center middle; border: solid green;
        width: auto; height: auto;
    }
    #my_static { border: solid blue; width: auto;}
    """

    def compose(self):

        with Container(id="my_container"):
            with Container(id="sub_container"):
                yield Static("Hello, Textual! More width!", id="my_static")
                yield Button("press me")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:

        static = self.query_one("#my_static", Static)
        static.styles.width = 50
        static.styles.height = 20


TextualApp().run()
