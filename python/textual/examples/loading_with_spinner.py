

from rich.spinner import Spinner
from textual import work
from textual.app import App
from textual.containers import Container
from textual.widgets import Header, Footer, Label, Static
import asyncio

class SpinnerWidget(Static):
    def __init__(self, spinner, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._spinner = Spinner(spinner, text)  

    def on_mount(self) -> None:
        self.update_render = self.set_interval(1 / 60, self.update_spinner)

    def update_spinner(self) -> None:
        self.update(self._spinner)


class MainContent(Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compose(self):
        yield SpinnerWidget("bouncingBall", "Loading...", classes="spinner")

        # A few common options:
        # arc, arrow, bouncingBall, boxBounce, dots, dots2 to dots12, line
        # python -m rich.spinner to see all options

    def on_mount(self):
        self.call_after_refresh(self.init)

    @work
    async def init(self):
        await asyncio.sleep(3)
        self.finalize()

    def finalize(self):
        self.remove_children()
        self.mount(Label("Hello world."))

class MyApp(App):

    DEFAULT_CSS = """
    .content {
        width: 1fr; height: 1fr; content-align: center middle; align: center middle;
    }
    .spinner {width: 1fr; height: 1fr; content-align: center middle;}
    """

    def compose(self):
        yield Header()
        yield MainContent(classes="content")
        yield Footer()

MyApp().run()