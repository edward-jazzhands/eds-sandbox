from textual.app import App
from textual.widgets import Footer, RichLog, Log
from textual.containers import Container
from rich.text import Text
import random


class MyRichLog(RichLog):

    ALLOW_SELECT = True

    @property
    def allow_select(self) -> bool:
        return True


class TextualApp(App):

    DEFAULT_CSS = """
    #my_container { width: 1fr; height: 1fr; border: solid red;
    align: center middle; content-align: center middle; }
    RichLog { border: solid blue; width: 50%; height: 1fr}

    """

    def compose(self):

        with Container(id="my_container"):
            yield MyRichLog(markup=True, highlight=True)
        yield Footer()

    def on_ready(self):

        self.set_interval(1, self.post_log_message)

    def post_log_message(self):

        colors = ["red", "green", "blue", "yellow", "cyan", "magenta"]
        color = random.choice(colors)

        self.query_one(MyRichLog).write(f"Hello, [bold {color}]world!")


TextualApp().run()
