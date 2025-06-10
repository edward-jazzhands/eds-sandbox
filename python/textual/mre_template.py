from textual.app import App
from textual.widgets import Footer

class TextualApp(App[None]):

    CSS = """
    /* any needed CSS  here */
    """

    def compose(self):
        # any needed widgets here
        yield Footer()

    # code that causes a bug here

TextualApp().run()