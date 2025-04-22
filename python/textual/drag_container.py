# This script is the first prototype of a floating "window" for textual
# which can be dragged around the screen using the mouse.

from __future__ import annotations
from textual.app import App
from textual import on
from textual.events import MouseDown, MouseUp, MouseMove
from textual.widgets import Footer, Static
from textual.containers import Container
from textual.geometry import Offset
from textual.reactive import Reactive
# from textual.binding import Binding


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

    def on_mouse_up(self, event: MouseDown) -> None:
        self.mouse_status = False   

    def on_mouse_down(self, event: MouseDown) -> None:
        self.mouse_status = True

    def on_leave(self) -> None:
        self.mouse_status = False


    def move_up(self) -> None:
        self.offset = Offset(self.offset.x, self.offset.y - 1)

    def move_down(self) -> None:
        self.offset = Offset(self.offset.x, self.offset.y + 1)

    def move_left(self) -> None:
        self.offset = Offset(self.offset.x - 1, self.offset.y)

    def move_right(self) -> None:
        self.offset = Offset(self.offset.x + 1, self.offset.y)


    # def _slide_closed(self):      

    #     if self.slide_direction == "left":
    #         self.animate(
    #             "offset", Offset(-(self.size.width+self.bo), 0),
    #             duration=self.duration, easing=self.easing_function
    #         )
    #     elif self.slide_direction == "right":
    #         self.animate(
    #             "offset", Offset(self.size.width+self.bo, 0),
    #             duration=self.duration, easing=self.easing_function
    #         )
    #     elif self.slide_direction == "up":
    #         self.animate(
    #             "offset", Offset(0, -(self.size.height+self.bo)),
    #             duration=self.duration, easing=self.easing_function
    #         )            
    #     elif self.slide_direction == "down":
    #         self.animate(
    #             "offset", Offset(0, self.size.height+self.bo),
    #             duration=self.duration, easing=self.easing_function
    #         ) 


class TextualApp(App):

    mouse_status: Reactive[bool] = Reactive[bool](False)

    DEFAULT_CSS = """
    # Screen { align: center middle; }
    DragContainer {
        border: panel $primary; width: 25; height: 10;
        background: $panel; align: center middle;
        &.focus {
            background: $accent;
        }
    }
    #placeholder { width: 1fr; height: 1fr; content-align: center middle;}
    #center_placeholder { border: solid blue; content-align: center middle; width: auto;}
    #center_content { align: center middle; }
    """
    
    def compose(self):

        self.drag_container = DragContainer(id="drag_container")
        self.drag_container.data_bind(TextualApp.mouse_status)

        yield self.drag_container
        with Container(id="center_content"):
            yield Static("Center placeholder", id="center_placeholder")
        yield Footer()

    @on(MouseMove)
    def my_mouse_moving(self, event: MouseMove) -> None:

        if event.delta_x < 0:
            my_leftright = "left"
        elif event.delta_x > 0:
            my_leftright = "right"
        else:
            my_leftright = ""

        if event.delta_y < 0:
            my_updown = "up"
        elif event.delta_y > 0:
            my_updown = "down"
        else:
            my_updown = ""

        direction = f"{my_leftright} {my_updown}"


        self.log(
            f"direction: {direction} \n"
            f"{event.screen_offset} \n"
        )

        if self.drag_container.mouse_status:
            if my_leftright == "left":
                self.drag_container.move_left()
            elif my_leftright == "right":
                self.drag_container.move_right()
            if my_updown == "up":
                self.drag_container.move_up()
            elif my_updown == "down":
                self.drag_container.move_down()   
    

TextualApp().run()