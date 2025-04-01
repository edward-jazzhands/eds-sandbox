from textual.app import App, ComposeResult
from textual.widgets import TextArea


class InlineApp(App):
    CSS = """
    TextArea {
        height: auto;
        max-height: 50vh;
    }
    """

    def compose(self) -> ComposeResult:
        yield TextArea(language="python")


if __name__ == "__main__":
    InlineApp().run(inline=True, mouse=False)