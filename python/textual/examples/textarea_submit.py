# This shows how to add a Submitted action to a TextArea widget which
# replicates the Submitted messge in the Input widget, and which can
# be triggered by pressing a key (Enter key in this case).

from __future__ import annotations
from textual import on
from textual.message import Message
from textual.binding import Binding
from textual.widgets import TextArea
from textual.widget import Widget

class MyTextArea(TextArea):

    class Submitted(Message):
        def __init__(self, textarea: MyTextArea, text: str):
            self.textarea = textarea    # the MyTextArea widget that sent the message
            self.text = text
            self.value = text  # extra alias for text
    
    BINDINGS = [
        Binding("enter", "submit", "Submit", show=True),
    ]
    
    def action_submit(self):
        self.post_message(self.Submitted(self, self.text))


# USAGE IN PARENT:
class MyParentFoo(Widget):

    def compose(self):
        yield MyTextArea()
    
    @on(MyTextArea.Submitted)
    def my_textarea_submitted(self, event: MyTextArea.Submitted):
        self.log.info(f"TextArea submitted with text: {event.text}")
        # handle submit here