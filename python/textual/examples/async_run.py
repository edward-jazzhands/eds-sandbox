import asyncio

from textual.app import App

class MyApp(App):
    def __init__(self, main_async, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_async = main_async
        self.main_async_task = None

    def on_load(self):
        self.main_async_task = asyncio.create_task(self.main_async)


async def main_async(...):
    ...


app = MyApp(main_async(), ...)
app.run()