# This example demonstrates how to override the _log method of the App class
# to insert some custom logic like logging to a RichLog widget.
# You have to run this with the dev console enabled to see what this
# example is doing.


from typing import Any

from textual.app import App
from textual import on, LogGroup    # type: ignore [import]
from textual.widgets import Footer, Input, RichLog
from textual.containers import Container
from rich.text import Text

class RichLoggingLogger(App):

    CSS = """
    RichLog { border: solid blue; width: 80%; height: 60%}
    #center_content { border: solid red; align: right bottom; }
    #input1 { width: 25; }
    """

    def _log(self, group: LogGroup, verbosity, _textual_calling_frame,
        *objects: Any, **kwargs, ) -> None:
        
        if self._dom_ready and group == LogGroup.INFO:
            self.rich_log.write(Text(f"INFO: {objects[0]}"))

        super()._log(
            group, verbosity, _textual_calling_frame, *objects, **kwargs
        )
    
    def compose(self):

        with Container(id="center_content"):

            self.rich_log = RichLog()   
            yield self.rich_log
            yield Input(placeholder="Type here", id="input1")      

        yield Footer()

    @on(Input.Submitted, "#input1")
    def input_submitted(self, event: Input.Submitted) -> None:
        self.log(f"Input submitted: {event.value}")
        event.input.value = ""  # Clear the input field after submission

RichLoggingLogger().run()
