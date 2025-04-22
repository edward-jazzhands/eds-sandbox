# This example demonstrates how to create a button with markup text using Textual.

from textual.app import App
from textual.widgets import Footer, Button
from textual.containers import Container
from textual.content import Content

class TextualApp(App):

    DEFAULT_CSS = """
    #my_container { width: 1fr; height: 1fr; border: solid red;
    align: center middle; content-align: center middle; }
    .buttons {&:focus { text-style: bold; } }
    """
    
    def compose(self):

        with Container(id="my_container"):
            button = Button(
                Content.from_markup("[yellow]This[/yellow] is my [red]button"),
                classes="buttons"
            )
            yield button
        yield Footer()


TextualApp().run()