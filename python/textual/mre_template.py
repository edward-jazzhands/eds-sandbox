from textual.app import App
from textual.widgets import Static, Footer
from textual.containers import VerticalScroll

class MREApp(App):

    def compose(self):
        with VerticalScroll(id="messages"):
            for _ in range(100):
                yield Static("All work and no play makes Lorem Ipsum dolor sit amet.")

        yield Footer()
    
    async def on_mount(self):
        self.messages = self.query_one("#messages")

        self.last_static = Static("This is the last widget.")
        await self.messages.mount(self.last_static)

        # self.do_the_scrolly_thing()                 #! <-- This will not work!

        self.call_after_refresh(self.do_the_scrolly_thing) #* <-- This fixes it

    def do_the_scrolly_thing(self):
        self.messages.scroll_to_widget(self.last_static)

MREApp().run()