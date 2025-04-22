from textual.app import App
from textual.widgets import Static, Footer
from textual.binding import Binding

class TextualApp(App):

    BINDINGS = [
        Binding("ctrl+s", "binding1", description="My Binding 1"),
    ]
    
    def compose(self):

        yield Static("Hello, Textual!")
        yield Footer()

    def action_binding1(self):
        self.notify("Binding 1 triggered!")

TextualApp().run()