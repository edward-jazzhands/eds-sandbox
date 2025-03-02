
from textual.app import App
from textual import work
from textual.widget import Widget
from textual.widgets import Header, Footer, Label
import asyncio

class MyWidget(Widget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loading = True

    def compose(self):
        yield Label("Your Textual App Here")

    def on_mount(self):
        self.call_after_refresh(self.init)

    @work
    async def init(self):
        await asyncio.sleep(3)
        self.loading = False

class MyApp(App):

    DEFAULT_CSS = """MyWidget {
    width: 1fr; height: 1fr; content-align: center middle; align: center middle;
    } Label { background: $surface; padding: 2;}"""

    def compose(self):
        yield Header()
        yield MyWidget()
        yield Footer()

MyApp().run()