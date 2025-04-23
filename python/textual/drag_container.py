# This script is the first prototype of a floating "window" for textual
# which can be dragged around the screen using the mouse.

from textual.app import App
from textual.events import MouseUp, MouseDown, MouseMove
from textual.widgets import Footer, Static
from textual.containers import Container
from textual.geometry import Offset
from textual.reactive import Reactive


class DragContainer(Container):

    BORDER_TITLE = "Drag Me"
    mouse_status: Reactive[bool] = Reactive[bool](False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_layers = self.app.screen.layers
        if "drag_container" not in current_layers:
            layers = [layer for layer in current_layers if not layer.startswith("_")]
            new_layers = tuple(layers) + ("drag_container",)
            self.app.screen.styles.layers = new_layers  # type: ignore  |  Pylance complains but this is fine.

        self.styles.layer = "drag_container"
        self.can_focus = True

    def compose(self):
        yield Static("Placeholder", id="placeholder")

    def on_mouse_up(self, event: MouseUp) -> None:
        self.mouse_status = False   

    def on_mouse_down(self, event: MouseDown) -> None:
        self.mouse_status = True

    def on_leave(self) -> None:
        self.mouse_status = False
        
    def on_mouse_move(self, event: MouseMove) -> None:

        if self.mouse_status:
            self.offset = Offset(self.offset.x + event.delta_x, self.offset.y)
            self.offset = Offset(self.offset.x, self.offset.y + event.delta_y)

class TextualApp(App):

    DEFAULT_CSS = """
    DragContainer {
        border: panel $primary; width: 25; height: 10;
        background: $panel; align: center middle;
    }
    #placeholder { width: 1fr; height: 1fr; content-align: center middle;}
    #center_placeholder { border: solid blue; content-align: center middle; width: auto;}
    #center_content { align: center middle; }
    """
    
    def compose(self):

        yield DragContainer()
        yield DragContainer()        
        with Container(id="center_content"):
            yield Static("Center placeholder", id="center_placeholder")
        yield Footer() 


TextualApp().run()