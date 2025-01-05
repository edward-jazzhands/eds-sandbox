# Tic-Tac-Toe built with Textual
# This is a standalone script. You can copy and paste this file into
# any environment that has Textual installed and run it directly.
# No dependencies are required other than Textual.


from __future__ import annotations
from enum import Enum

# Textual imports
from textual.app import App, on
from textual.reactive import reactive
from textual.widget import Widget
from textual.message import Message
from textual.dom import DOMNode
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.validation import Number
from textual.widgets import Footer, Button, Label, Input

class PlayerState(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

class MyScreen(ModalScreen):

    def compose(self):
        with Container(classes="auto bordered"):
            yield Label("Enter a number\nbetween 2 and 5:")
            yield Input(id="input", type="integer", validators=[Number(2, 5)], validate_on=["submitted"])

    @on(Input.Submitted)
    def close(self, event: Input.Submitted):
        if not event.validation_result.is_valid:
            return
        else:
            self.dismiss(int(event.value))

class Cell(Widget):
    
    state = reactive(PlayerState.EMPTY)
    x = r"""
\_/ 
/ \ """
    o = r""" __ 
/  \
\__/"""

    class Pressed(Message):
        def __init__(self, cell: Cell):
            super().__init__()
            self.cell = cell

    def __init__(self, row: int, column: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = row
        self.column = column

    def render(self):
        if self.state == PlayerState.PLAYER1:
            return self.x
        elif self.state == PlayerState.PLAYER2:
            return self.o
        else:
            return ""

    def on_click(self):
        self.post_message(self.Pressed(self))


class Grid(Widget):

    def __init__(self, rows: int, columns: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows:int = rows
        self.columns:int = columns
        self.styles.grid_size_rows = self.rows
        self.styles.grid_size_columns = self.columns
        self.styles.width = rows * 10
        self.styles.height = columns * 6 + 1

    def compose(self):
        for row in range(self.rows):
            for column in range(self.columns):
                yield Cell(row=row, column=column, classes="gridcell bordered centered")

    def clear_grid(self):
        for cell in self.query_children(Cell):
            cell.state = PlayerState.EMPTY

class GameManager(DOMNode):

    class ChangeTurn(Message):
        def __init__(self, value: PlayerState):
            super().__init__()
            self.value = value

    class GameOver(Message):
        def __init__(self, result: PlayerState):
            super().__init__()
            self.result = result

    turn_token: PlayerState | None = reactive(PlayerState.EMPTY)
    
    def __init__(self, rows:int, columns:int, id:str=None):
        super().__init__(id=id)
        self.rows = rows
        self.columns = columns
        self.start_game()

    def watch_turn_token(self, value: PlayerState):
        self.app.post_message(self.ChangeTurn(value))

    def game_over(self, result: PlayerState):

        self.int_board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.turn_token = PlayerState.EMPTY
        self.app.post_message(self.GameOver(result))

    def start_game(self):
        self.turn_token = PlayerState.PLAYER1
        self.int_board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.app.notify("Game started", timeout=1)

    def cell_pressed(self, event: Cell.Pressed):

        cell = event.cell
        if self.turn_token == PlayerState.EMPTY:
            self.app.notify("Game hasn't started yet", timeout=1)
            return
        if cell.state != PlayerState.EMPTY:
            self.app.notify("Cell already taken", timeout=1)
            return

        if self.turn_token == PlayerState.PLAYER1:
            cell.state = PlayerState.PLAYER1
            self.turn_token = PlayerState.PLAYER2
            self.int_board[cell.row][cell.column] = 1
            self.calculate_winner()

        elif self.turn_token == PlayerState.PLAYER2:
            cell.state = PlayerState.PLAYER2
            self.turn_token = PlayerState.PLAYER1
            self.int_board[cell.row][cell.column] = 2
            self.calculate_winner()
        
    def calculate_winner(self):

        def check_line(line, player):
            return all(cell == player for cell in line)
        
        rows      = self.int_board
        columns   = list(zip(*self.int_board))
        main_diag = [[self.int_board[i][i] for i in range(self.rows)]]
        anti_diag = [[self.int_board[i][self.rows - i - 1] for i in range(self.rows)]] 
        
        lines = (rows + columns + main_diag + anti_diag)    # Get all possible winning lines

        for player in (1, 2):
            if any(check_line(line, player) for line in lines):
                self.game_over(PlayerState.PLAYER1 if player == 1 else PlayerState.PLAYER2)
                return
                
        if all(cell != 0 for row in self.int_board for cell in row):
            self.game_over(PlayerState.EMPTY)
        

class MyAppTemplate(App):

    DEFAULT_CSS = """

        .auto {
            width: auto;
            height: auto;
        }

        .onefr {
            width: 1fr;
            height: 1fr;
        }

        .centered {
            align: center middle;
            content-align: center middle;
        }

        .bordered {
            background: $surface-lighten-1;
            border: tall $primary-background;
            padding: 0 2 0 2;
        }

        .grid {
            layout: grid;
            grid-gutter: 0;
            padding: 0;
            margin: 0;
        }

        .footer {
            width: 1fr;
            height: 5;
        }

        .gridcell {
            width: 10;
            height: 5;
            margin: 1 0 0 0;
        }

        Cell:hover {
            background: $secondary-background;
        }
    """

    def compose(self):

        with Container(id="content", classes="onefr centered"):
            yield Label(id="turn_label", classes="auto centered")
        with Horizontal(classes="centered footer"):
            yield Button("Restart", id="restart", classes="auto centered")
            yield Button("Change Size", id="change_size", classes="auto centered")
        yield Footer()

    def on_mount(self):
        self.push_screen(MyScreen(classes="centered"), self.mount_grid)

    async def mount_grid(self, grid_size: int):

        self.game_manager = GameManager(rows=grid_size, columns=grid_size)
        self.grid = Grid(rows=grid_size, columns=grid_size, classes="grid onefr centered")
        self.query_one("#content").mount(self.grid)

    @on(Cell.Pressed)
    def cell_pressed(self, event: Cell.Pressed):
        self.game_manager.cell_pressed(event)

    @on(GameManager.ChangeTurn)
    def change_turn(self, event: GameManager.ChangeTurn):
        self.query_one("#turn_label").update(f"{event.value.name}'s turn")

    @on(GameManager.GameOver)
    def game_over(self, event: GameManager.GameOver):
        self.notify("Game over", timeout=1)
        if event.result == PlayerState.EMPTY:
            self.query_one("#turn_label").update("It's a tie!")
        else:
            self.query_one("#turn_label").update(f"{event.result.name} wins!")

    @on(Button.Pressed, "#restart")
    def restart(self):
        self.grid.clear_grid()
        self.game_manager.start_game()

    @on(Button.Pressed, "#change_size")
    def change_size(self):
        self.grid.remove()
        self.push_screen(MyScreen(classes="centered"), self.mount_grid)


if __name__ == "__main__":
    MyAppTemplate().run()