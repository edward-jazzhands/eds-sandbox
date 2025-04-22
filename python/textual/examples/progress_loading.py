from textual.app import App, ComposeResult
from textual import work
from textual.widget import Widget
from textual.widgets import Button, ProgressBar
from textual.containers import VerticalGroup

import asyncio

class CustomLoadingWidget(VerticalGroup):
  def compose(self) -> ComposeResult:
    yield Button('Do the thing!')
  

  async def on_button_pressed(self):
    self.loading_progress()

  @work()
  async def loading_progress(self):
    self.loading = True

    for i in range(4):
      await asyncio.sleep(0.75)
      self._cover_widget.advance(1)   #type: ignore
    
    self.loading = False

  def get_loading_widget(self) -> Widget:
    return ProgressBar(total=4)    


class Main(App):
  def compose(self) -> ComposeResult:
    yield CustomLoadingWidget()


if __name__ == '__main__':
  Main().run()