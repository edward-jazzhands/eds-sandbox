from textual.app import App, ComposeResult
from textual.widgets import Header, Button


class SandboxApp(App):
    # TITLE = "FR3-d1"

    # def __init__(self):
    #     super().__init__()
        

    def compose(self) -> ComposeResult:
        self.title = "my new title"
        yield Header()
        yield Button("Change the title")

    # def on_button_pressed(self) -> None:
        

if __name__ == "__main__":
    SandboxApp().run()