from typing import Protocol
from textual.widget import Widget
from textual.app import App, ComposeResult


class DataWidget(Protocol):
    def load_data(self) -> None:
        ...


# This widget implements the protocol (duck typing)
class UserWidget(Widget, DataWidget):
    # if this was renamed then the type checker will complain:
    def load_data(self) -> None:
        self.notify("Users loaded")


# This widget does NOT implement the protocol - missing load_data method
class BrokenWidget(Widget):
    pass


class DataApp(App[None]):
    def compose(self) -> ComposeResult:
        yield UserWidget()
        # Uncomment this line to see mypy/type checker complain:
        # yield BrokenWidget()
    
    def on_mount(self) -> None:
        # This function expects a DataWidget protocol
        def refresh_data(widget: DataWidget) -> None:
            widget.load_data()
        
        user_widget = self.query_one(UserWidget)
        refresh_data(user_widget)  # Works - UserWidget follows protocol
        
        # # This would fail type checking:
        # broken = BrokenWidget()
        # refresh_data(broken)  # Type error - BrokenWidget missing load_data


if __name__ == "__main__":
    app = DataApp()
    app.run()