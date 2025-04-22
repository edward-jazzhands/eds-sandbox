from textual.app import App
from textual import on
from textual.widgets import Static, Footer, Button
from textual.containers import Container

from textual_slidecontainer import SlideContainer

class TextualApp(App):

    DEFAULT_CSS = """
    #my_container {
        width: 1fr; height: 1fr; border: solid red;
        align: center middle; content-align: center middle;
    }
    #my_static { border: solid blue; width: 1fr;}
    SlideContainer {
        width: 25; height: 1fr;
        background: $panel; align: center middle;
    }
    """
    def compose(self):

        # The container will start closed / hidden:
        with SlideContainer(slide_direction="left", start_open=False):
            yield Static("This is content in the slide container", id="my_static")
        with Container(id="my_container"):
            yield Button("Show/Hide slide container", id="toggle_slide")
        yield Footer()

    @on(Button.Pressed, "#toggle_slide")
    def toggle_slide(self) -> None:
        self.query_one(SlideContainer).toggle()

    # @on(SlideContainer.FinishedLoading)     # Event handler using @on
    # def slide_loaded(self):
    #     self.log("Slide container finished loading")

     # Alternative Textual method (use this or the one above)
    def on_slide_container_finished_loading(self, event: SlideContainer.FinishedLoading) -> None: 
        self.notify(str(event))

TextualApp().run()