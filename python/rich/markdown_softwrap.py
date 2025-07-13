# This file demonstrates a simple common issue - The text will have the 
# issue explained in the markdown, unless soft_wrap is enabled.
# You can set soft_wrap=False to see the issue being described.

from rich.console import Console
from rich.markdown import Markdown

example = """Here is some example markdown.

Here's a 2nd paragraph.

Changing the width of the terminal _change the vertical spacing of the
paragraphs!_

If I use `xxd` to view the raw hex output, or use `sed` to replace spaces with
periods, you can see each line ends with lots of spaces which wrap if the
terminal width changes."""

console = Console(force_terminal=True, markup=True, highlight=False, soft_wrap=True)
console.print(Markdown(example))