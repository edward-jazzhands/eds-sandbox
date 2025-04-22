# This demonstrates how to remove the focus highlight from buttons in Textual.

from textual.app import App
from textual.widgets import Button
from textual.containers import Container

class TextualApp(App):

    DEFAULT_CSS = """
    #my_container { width: 1fr; height: 1fr; align: center middle; }
    .my_button {&:focus {text-style: none;}}
    """
    
    def compose(self):

        with Container(id="my_container"):
            yield Button("Button1", classes="my_button")
            yield Button("Button2", classes="my_button")
            yield Button("Button3", classes="my_button")

TextualApp().run()