# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import TYPE_CHECKING
from collections import deque

if TYPE_CHECKING:
    pass

# from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Static
from textual.reactive import reactive
from textual.strip import Strip
from rich.segment import Segment
from rich.style import Style


class ScrollingLine(Static):

    DEFAULT_CSS = """
    ScrollingLine { width: 50 ; height: 1; }
    """

    sequence: reactive[deque[Segment]] = reactive(deque([]), layout=True)

    def __init__(self):
        super().__init__()
        self.pattern = [
            Segment("+", style=Style(color="green")),
            Segment(" ", style=Style()),
            Segment(" ", style=Style()),
            Segment("+", style=Style(color="blue")),
            Segment(" ", style=Style()),
            Segment(" ", style=Style()),
            Segment("+", style=Style(color="red")),
            Segment(" ", style=Style()),
            Segment(" ", style=Style()),            
        ]
        self.direction_int = 1

    def on_mount(self):

        self.set_interval(fps, self.asciiscroll)

        if self.styles.width and self.styles.width.cells:
            amount = (self.styles.width.cells // len(self.pattern)) + 1
            self.sequence.extend(self.pattern * amount)
        else:
            raise Exception("Yo momma")

    def asciiscroll(self):

        self.sequence.rotate(self.direction_int)  # 1 = forwards, -1 = reverse
        self.mutate_reactive(ScrollingLine.sequence)  

    def render_line(self, y: int) -> Strip:
        return Strip(self.sequence)
