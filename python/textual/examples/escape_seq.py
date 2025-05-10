from textual.app import App
from textual.widgets import Footer, Static
from textual.markup import escape

import re


class TextualApp(App):

    DEFAULT_CSS = """
    /* any needed CSS  here */
    """

    def compose(self):
        yield Static(escape("[0]Hello World!", _escape=re.compile(r"(\\*)(\[[a-z0-9#/@][^[]*?])").sub))
        yield Footer()

    # code that causes a bug here

TextualApp().run()