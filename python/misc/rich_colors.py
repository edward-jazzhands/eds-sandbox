import time
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.box import MINIMAL
from rich.panel import Panel
import random

# Available terminal colors in Rich
colors = [
    "red",
    "green",
    "blue",
    "magenta",
    "cyan",
    "yellow",
    "bright_red",
    "bright_green",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_yellow",
]


def color_cycling_animation():
    console = Console()

    # Our message to animate
    message = "This text is changing colors every 2 seconds!"

    # Creating a styled panel with the content
    with Live(refresh_per_second=4, console=console) as live:
        while True:
            # Choose a random color
            color = random.choice(colors)

            # Create styled text
            styled_text = Text(message, style=f"bold {color}")

            # Create a panel containing our styled text
            panel = Panel(
                styled_text,
                title="[bold white]Color Animation Demo[/bold white]",
                border_style=color,
                padding=(1, 2),
            )

            # Update the live display with our panel
            live.update(panel)

            # Wait for 2 seconds before changing color
            time.sleep(2)


def rainbow_wave_animation():
    """Creates a rainbow wave effect across multiple lines of text"""
    # Define rainbow colors
    console = Console()

    # List of multiple lines
    messages = [
        "This is the first line of the rainbow wave animation!",
        "Here's the second line flowing with colors.",
        "The third line joins the colorful party.",
        "Fourth line showing the rainbow effect.",
        "And finally, the fifth line completes the animation!",
    ]

    with Live(refresh_per_second=15, console=console) as live:
        position = 0
        while True:
            # Create a combined text object for all lines
            combined_text = Text()

            # Process each line
            for i, message in enumerate(messages):
                text = Text(message)

                # Apply colors in a wave pattern for each character
                for j in range(len(message)):
                    # Calculate color position in the rainbow
                    # Same index positions across all lines get the same color
                    color_index = (j + position) % len(colors)
                    text.stylize(colors[color_index], j, j + 1)

                # Add the line to our combined text
                combined_text.append(text)

                # Add a newline if this isn't the last line
                if i < len(messages) - 1:
                    combined_text.append("\n")

            # Create a panel with our rainbow text
            panel = Panel(
                combined_text,
                title="[bold white]Rainbow Wave Animation[/bold white]",
                border_style="bright_white",
                padding=(1, 2),
            )

            # Update the display
            live.update(panel)

            # Move the wave position and sleep briefly
            position += 1
            time.sleep(0.1)


def rainbow_line_animation():
    """Creates a rainbow effect where each line has its own color that shifts over time"""
    console = Console()

    # Multi-line text - each line will have its own color
    message = [
        "This is line 1 of the text with its own color.",
        "Line 2 will have a different color.",
        "Line 3 gets another color in the sequence.",
        "Line 4 continues the pattern.",
        "Line 5 completes our rainbow effect.",
        "Line 6 starts the cycle again.",
    ]

    with Live(refresh_per_second=4, console=console) as live:
        position = 0
        while True:
            # Create a text object to hold all lines
            text = Text()

            # Apply a different color to each line
            for i, line in enumerate(message):
                # Calculate color position in the rainbow
                color_index = (i + position) % len(colors)

                # Add the line with its color
                if i > 0:
                    text.append("\n")  # Add newline except for first line
                text.append(line, style=f"bold {colors[color_index]}")

            # Create a panel with our rainbow text
            panel = Panel(
                text,
                box=MINIMAL,
                expand=False,
            )

            # Update the display
            live.update(panel)

            # Shift the colors and sleep
            position += 1
            time.sleep(0.5)


def mega_rainbow_wave_animation():
    """Creates a mega rainbow wave that flows both horizontally and vertically"""
    console = Console()

    # Multi-line text for our mega rainbow
    message = [
        "This is part of an amazing diagonal rainbow wave!",
        "Each character's color is calculated based on its",
        "position in both the X and Y dimensions, creating",
        "a smooth diagonal wave effect across the entire",
        "text block. The colors flow through in a beautiful",
        "coordinated pattern that's hypnotizing to watch.",
    ]

    # max_line_length = max(len(line) for line in message)

    with Live(refresh_per_second=10, console=console) as live:
        wave_position = 0
        while True:
            # Create a text object to hold all lines
            text = Text()

            # Apply colors to each character based on its position
            for line_idx, line in enumerate(message):
                if line_idx > 0:
                    text.append("\n")  # Add newline except for first line

                for char_idx, char in enumerate(line):
                    # Calculate the diagonal position (x + y)
                    # This creates a diagonal wave effect
                    diagonal_pos = (char_idx + line_idx + wave_position) % len(colors)

                    # Add the character with its calculated color
                    text.append(char, style=f"{colors[diagonal_pos]}")

            # Create a panel with our mega rainbow wave text
            panel = Panel(
                text,
                box=MINIMAL,
                expand=False,
            )

            # Update the display
            live.update(panel)

            # Move the wave position and sleep briefly
            wave_position += 1
            time.sleep(0.1)


if __name__ == "__main__":
    print("Running color cycling animation (press Ctrl+C to stop)...")

    # Uncomment one of these to run the desired animation:
    # color_cycling_animation()    # Changes the entire text color every 2 seconds
    rainbow_wave_animation()  # Creates a flowing rainbow effect across text
    # rainbow_line_animation()  # Creates a rainbow effect where each line has its own color
    # mega_rainbow_wave_animation()  # Creates a diagonal wave flowing across all text
