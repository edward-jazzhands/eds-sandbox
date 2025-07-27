"""
Conway's Game of Life implementation using Rich for terminal visualization.
Author: Paul Robello
Email: probello@gmail.com
"""

import random
from enum import Enum
from time import sleep
from typing import List

import typer
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich import print as rprint


app = typer.Typer()

class NeighborhoodRules(str, Enum):
    """
    Enum class representing the neighborhood rules for the Game of Life simulation.
    """
    MOORE = "moore"
    VAN_NEUMANN = "van_neumann"

class GameOfLife:
    """
    Represents the Game of Life simulation.
    """

    def __init__(self, width: int, height: int, rules: NeighborhoodRules = NeighborhoodRules.MOORE) -> None:
        """
        Initialize the Game of Life grid.
        Args:
            width (int): Width of the grid.
            height (int): Height of the grid.
        """
        self.width: int = width
        self.height: int = height
        self.rules: NeighborhoodRules = rules
        self.grid: List[List[int]] = [[random.choice([0, 1]) for _ in range(width)] for _ in range(height)]
        self.generation: int = 0

    def get_neighbors_van_neumann(self, x: int, y: int) -> int:
        """
        Count the number of live neighbors for a given cell according to the
        "Van Neumann Neighborhood" rules.
        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.
        Returns:
            int: Number of live neighbors.
        """
        count: int = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = (x + dx) % self.width, (y + dy) % self.height
            count += self.grid[ny][nx]
        return count

    def get_neighbors_moore(self, x: int, y: int) -> int:
        """
        Count the number of live neighbors for a given cell according to the
        "Moore Neighborhood" rules.
        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.
        Returns:
            int: Number of live neighbors.
        """
        count: int = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % self.width, (y + dy) % self.height
                count += self.grid[ny][nx]
        return count

    def get_neighbors(self, x: int, y: int) -> int:
        """
        Count the number of live neighbors for a given cell according to the
        "Neighborhood" rules.
        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.
        Returns:
            int: Number of live neighbors.
        """
        if self.rules == NeighborhoodRules.VAN_NEUMANN:
            return self.get_neighbors_van_neumann(x, y)
        return self.get_neighbors_moore(x, y)

    def next_generation(self) -> None:
        """
        Compute the next generation of the Game of Life.
        """
        new_grid: List[List[int]] = [[0 for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                neighbors: int = self.get_neighbors(x, y)
                if self.grid[y][x] == 1:
                    if 2 <= neighbors <= 3:
                        # print(f"live cell {x}, {y} = {neighbors}")
                        new_grid[y][x] = 1
                elif neighbors == 3:
                    # print(f"new cell {x}, {y} = {neighbors}")
                    new_grid[y][x] = 1
        self.grid = new_grid
        self.generation += 1

    def print_board_ascii(self) -> None:
        """
        Print the current state of the Game of Life grid.
        """
        for row in self.grid:
            for cell in row:
                print('●' if cell else ' ', end='')
            print()

    def print_neighbors(self) -> None:
        """
        Print the number of live neighbors for each cell in the Game of Life grid.
        """
        for y in range(self.height):
            for x in range(self.width):
                neighbors: int = self.get_neighbors(x, y)
                print(f"{neighbors} ", end='')
            print()

    def print_neighbors_rich(self) -> None:
        """
        Print the number of live neighbors for each cell in the Game of Life grid using Rich.
        Colors: red=will die, green=will generate, white=will continue
        """
        for y in range(self.height):
            row = []
            for x in range(self.width):
                neighbors: int = self.get_neighbors(x, y)
                cell_state = self.grid[y][x]
                if cell_state == 1 and (neighbors < 2 or neighbors > 3):
                    color = "red"
                elif cell_state == 0 and neighbors == 3:
                    color = "green"
                else:
                    color = "white"
                row.append(f"[{color}]{neighbors}[/{color}]")
            rprint(" ".join(row))

    def run(self, generations: int = 100) -> None:
        """
        Run the Game of Life simulation for a specified number of generations.
        Args:
            generations (int): Number of generations to simulate. Defaults to 100.
        """
        console: Console = Console()


        with Live(console=console, refresh_per_second=10, transient=False) as live:
            for _ in range(generations):
                title = Text(f"Conway's Game of Life: {self.width}x{self.height} - Rules: {self.rules.name} - Generation: {self.generation} / {generations}",
                             style="bold magenta")
                table: Table = Table(title=title, show_header=False, show_lines=True)
                for row in self.grid:
                    table.add_row(*['●' if cell else ' ' for cell in row])
                self.next_generation()
                live.update(table)
                sleep(0.1)



@app.command()
def main(
    width: int = typer.Option(32, "--width", "-w", help="Width of the grid"),
    height: int = typer.Option(32, "--height", "-h", help="Height of the grid"),
    generations: int = typer.Option(200, "--generations", "-g", help="Number of generations to simulate"),
    rules: NeighborhoodRules = typer.Option(NeighborhoodRules.MOORE, "--rules", "-r", help="Neighborhood rules to use")
):
    """
    Run Conway's Game of Life simulation with specified parameters.
    """
    game: GameOfLife = GameOfLife(width=width, height=height, rules=rules)
    game.run(generations=generations)


if __name__ == "__main__":
    typer.run(main)
else:
    # When imported as a module, make sure GameOfLife is available
    __all__ = ['GameOfLife']