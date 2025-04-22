import os
from textual.app import App
from textual.widgets import Static, Footer
from textual.containers import Container


class TextualApp(App):

    env_has_true_color:bool = os.environ["COLORTERM"] == "truecolor"

    def compose(self):

        self._refresh_truecolor_filter

        with Container(id="my_container"):
            yield Static("Hello, Textual!")

        yield Footer()


TextualApp().run()