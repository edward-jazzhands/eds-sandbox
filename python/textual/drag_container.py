# This script is the first prototype of a floating "window" for textual
# which can be dragged around the screen using the mouse.

from textual.app import App
import textual.events as events
from textual.widgets import Footer, Static
from textual.containers import Container
from textual.geometry import Offset
from textual.reactive import Reactive


class DragContainer(Container):

    BORDER_TITLE = "Drag Me"
    mouse_status: Reactive[bool] = Reactive[bool](False)

    _current_layer = 0  # Class variable to track the next available layer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layer_index = DragContainer._current_layer
        DragContainer._current_layer += 1

    def on_compose(self) -> None:

        current_layers = self.screen.layers
        if f"drag_container{self.layer_index}" not in current_layers:
            layers = [layer for layer in current_layers if not layer.startswith("_")]
            layers.extend([f"drag_container{self.layer_index}"])
            self.log(f"new layers: {layers}")
            self.screen.styles.layers = tuple(layers)       # type: ignore
        self.styles.layer = f"drag_container{self.layer_index}"


    def on_mouse_move(self, event: events.MouseMove) -> None:

        self.log(f"delta_x: {event.delta_x} | delta_y: {event.delta_y}")

        # self.app.mouse_captured refers to the widget that is currently capturing mouse events.
        # Thus, we can check if that variable is equal to this widget. Easy, no flags needed.
        if self.app.mouse_captured == self:
            self.offset = Offset(self.offset.x + event.delta_x, self.offset.y)
            self.offset = Offset(self.offset.x, self.offset.y + event.delta_y) 

    async def on_mouse_down(self, event: events.MouseDown) -> None:

        self.capture_mouse()
        self.bring_forward()

    async def on_mouse_up(self, event: events.MouseUp) -> None:

        self.capture_mouse(False)

    def bring_forward(self):

        # Get all layers that are not this widget's layer:
        layers = tuple(x for x in self.screen.styles.layers if x != self.layer)
        # Append this widget's layer to the end of the tuple:
        self.screen.styles.layers = layers + tuple([self.styles.layer])     # type: ignore

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

        with DragContainer(id="drag_container1"):
            yield Static("X", id="placeholder")
        with DragContainer(id="drag_container2"):
            yield Static("X", id="placeholder")
        with Container(id="center_content"):
            yield Static("Center placeholder", id="center_placeholder")
        yield Footer() 


TextualApp().run()