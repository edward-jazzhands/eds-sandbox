# This script demonstrates what order that events are fired in Textual.

from textual.app import App
from textual.widgets import Static, Footer

import textual.events as events
events.Mount
events.AppBlur
events.AppFocus
events.Compose
events.Idle
events.Load
events.Ready
events.Resize
events.DescendantBlur
events.DescendantFocus

class TextualApp(App):

    def __init__(self):         # This is the very first thing to run.
        super().__init__()
        self.my_state = "foo"
        self._counter = 0
        self.log("This log statement won't work. The logger isn't set up yet")

    def counter(self) -> int:
        self._counter += 1
        return self._counter        

    def on_load(self, event: events.Load):
        self.log(f"{self.counter()}) Load event: {event._sender.__class__.__name__}. "      #1
                f"State: {self.my_state}")

    def compose(self):
        self.log(f"{self.counter()}) Composing started on main App class.")                 #2

        yield Static("Hello, Textual!")
        yield Footer()

    def on_resize(self, event: events.Resize):
        self.log(f"{self.counter()}) Resize event: {event._sender.__class__.__name__}")     #3 and 5 

    def on_mount(self, event: events.Mount):
        self.log(f"{self.counter()}) Mount event: {event._sender.__class__.__name__}")      #4

    def on_ready(self, event: events.Ready):
        self.log(f"{self.counter()}) Ready event: {event._sender.__class__.__name__}")      #6

TextualApp().run()