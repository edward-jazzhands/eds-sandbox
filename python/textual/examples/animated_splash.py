from collections import deque

from textual.app import App, ComposeResult
from textual.containers import Center
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Footer
from textual.geometry import Region
from textual.color import Gradient, Color

from rich.segment import Segment
from rich.style import Style

# you can replace this with regular pyfiglet, it works the same.
from textual_pyfiglet.pyfiglet import Figlet

from rich import traceback
traceback.install()

###############################
# ~ Modify these five lines ~ #
###############################

splash_text = "Chezmoi Mousse"   # It will auto wrap the text based on the terminal width when launching.
font = "ansi_shadow"
gradient_color_1 = "hotpink"
gradient_color_2 = "blue"
quality = 30        # Must be >= number of lines in the splash text

##############################


class AnimatedSplash(Widget):

    def __init__(self, splash: list[str], gradient: Gradient) -> None:
        super().__init__()

        self.splash = splash
        self.line_colors = deque([Style(color=color.rich_color) for color in gradient.colors])

        self.set_interval(interval=0.08, callback=self.refresh, repeat=0)

    def render_lines(self, crop: Region) -> list[Strip]:
        self.line_colors.rotate()
        return super().render_lines(crop)

    def render_line(self, y: int) -> Strip:
        return Strip([Segment(self.splash[y], style=self.line_colors[y])])


class GreeterScreen(App):
    CSS = """
    Center {height: 100%; width: 100%; align: center middle}
    """

    def compose(self) -> ComposeResult:

        splash = self.make_splash(splash_text, font)
        gradient = self.make_gradient(gradient_color_1, gradient_color_2, quality)

        splash_width = len(max(splash, key=len))
        splash_height = len(splash)

        self.log(f"Splash width: {splash_width} | Term width: {self.size.width}")
        self.log(f"Splash height: {splash_height} | Term height: {self.size.height}")

        animated_splash = AnimatedSplash(splash, gradient)
        animated_splash.styles.width = splash_width
        animated_splash.styles.height = splash_height

        with Center(id="center"):
            yield animated_splash
        yield Footer()

    def make_splash(self, text: str, font: str) -> list[str]:

        figlet_obj = Figlet(font=font, justify="left", width=self.size.width-10)
        figlet = figlet_obj.renderText(text)

        return figlet.splitlines()

    def make_gradient(self, color1: str, color2: str, quality: int) -> Gradient:
        "Use color names, ie. 'red', 'blue'"

        parsed_color1 = Color.parse(color1)
        parsed_color2 = Color.parse(color2)

        stop1 = (0.0, parsed_color1)
        stop2 = (0.5, parsed_color2)
        stop3 = (1.0, parsed_color1)
        return Gradient(stop1, stop2, stop3, quality=quality)
        
if __name__ == "__main__":
    GreeterScreen().run()