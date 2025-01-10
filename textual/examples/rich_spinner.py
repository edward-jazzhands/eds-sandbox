# This example shows how to use the rich library to display a spinner in Textual.
# The spinner object changes its rendering internally, but Textual needs to be manually updated
# to reflect that change. This is done by using `set_interval` to call the `update_spinner` method.

from rich.spinner import Spinner

from textual.app import App
from textual.widgets import Static

class SpinnerWidget(Static):
    def __init__(self, spinner, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._spinner = Spinner(spinner, text)  

    def on_mount(self) -> None:
        self.update_render = self.set_interval(1 / 60, self.update_spinner)

    def update_spinner(self) -> None:
        self.update(self._spinner)

class MyApp(App):

    DEFAULT_CSS = ".spinner {width: 1fr; height: 1fr; content-align: center middle;}"

    def compose(self):
        yield SpinnerWidget("line", "Loading...", classes="spinner")

    # A few common options:
    # arc, arrow, bouncingBall, boxBounce, dots, dots2 to dots12, line
    # python -m rich.spinner to see all options

MyApp().run()