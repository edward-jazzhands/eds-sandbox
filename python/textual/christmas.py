from collections import deque
from typing import Self

from pyfiglet import figlet_format
from rich.color import Color
from rich.segment import Segment
from rich.style import Style
from textual.app import App, ComposeResult
from textual.containers import Center
from textual.geometry import Region
from textual.reactive import reactive
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Header, Button


class ChristmasWidget(Widget):
    DEFAULT_CSS = """
    ChristmasWidget {
        width: auto;
        height: auto;
        padding: 0;
    }
    """

    colors: deque[Style] = deque()
    text: reactive[list[str]] = reactive(list, init=False, layout=True)

    def on_mount(self) -> None:
        for color in ("#165B33", "#146B3A", "#F8B229", "#EA4630", "#BB2528"):
            self.colors.append(Style(color=Color.parse(color)))
        self.clock = self.set_interval(0.2, self.refresh)

    def render_lines(self, crop: Region) -> list[Strip]:
        self.colors.rotate()
        return super().render_lines(crop)

    def render_line(self, y: int) -> Strip:
        try:
            return Strip([Segment(self.text[y], style=self.colors[y % 5])])
        except IndexError:
            return Strip.blank(self.size.width)

    def with_text(self, text: str) -> Self:
        self.text = figlet_format(text, "banner", width=self.app.size.width).split("\n")
        return self
    
    def update_text(self, text: str) -> None:
        self.text = figlet_format(text, "banner", width=self.app.size.width).split("\n")


    def get_content_height(self, *_) -> int:
        if self.text:
            return len(self.text)
        return 0

    def get_content_width(self, *_) -> int:
        if self.text:
            return len(max(self.text, key=len))
        return 0


class ChristmasApp(App):
    TITLE = "Merry Christmas"

    CSS = """
    ChristmasApp {
        background: $panel-darken-2;
    }
    Center {
        height: 100%;
        align: center middle;
    }
    ChristmasWidget {background: $panel; border: solid red;}
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Center():
            yield ChristmasWidget().with_text("Merry Christmas!")
            yield Button("Update", id="update")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ChristmasWidget).update_text("Cool")



if __name__ == "__main__":
    ChristmasApp().run()