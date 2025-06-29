# A very simple demonstration of colorirzed logging in Textual.

from textual.app import App
from rich.text import Text

class TextualApp(App[None]):

    def on_ready(self):

        self.log(Text.from_markup(
            "[bold][italic]Logger launched in on_ready method.[/italic] \n"
            "[green]Good Log message[/green] \n"
            "[blink red]Attention: something happened:"
        ))


TextualApp().run()