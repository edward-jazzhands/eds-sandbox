# This file demonstrates how to create a Textual application
# with a transparent background

from textual.app import App
from textual.widgets import Static, Footer, Button, Switch
from textual.containers import Container


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    #my_static { border: solid blue; width: auto;}
    #main_container { 
        width: 50%; height: 50%;
        border: solid red;
        align: center middle;
    }
    """

    def compose(self):

        with Container(id="main_container"):
            yield Static("Hello, Textual!", id="my_static")
            yield Button("Button1")
            yield Switch()

        yield Footer()


TextualApp(ansi_color=True).run()  # <- this is it. Thats all.
