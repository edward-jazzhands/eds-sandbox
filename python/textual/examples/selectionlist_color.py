from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, SelectionList
from textual.containers import Container

class MyApp(App):

    DEFAULT_CSS = """
        /* styles.tcss */
    #mylist ToggleButton.-on {
        color: red; /* color you want for selected items */
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            SelectionList[str](
                *["Item 1", "Item 2", "Item 3"],
                id="mylist"
            ),
            id="container"
        )

if __name__ == "__main__":
    app = MyApp()
    app.run()