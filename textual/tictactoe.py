from __future__ import annotations
from enum import Enum
from copy import deepcopy
from asyncio import sleep
from itertools import product


# Textual imports
from rich.text import Text
from rich.spinner import Spinner
from textual import work, on
from textual.app import App
from textual.reactive import reactive
from textual.worker import Worker, WorkerState
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Footer, Button, Label, Static, Input
from textual.screen import ModalScreen
from textual.binding import Binding
from textual.validation import Number



class PlayerState(Enum):
    """The state of a cell in the game. \n
    Can be EMPTY, PLAYER1, or PLAYER2."""
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2


class SpinnerWidget(Static):
    def __init__(self, spinner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._spinner = Spinner(spinner)  

    def on_mount(self) -> None:
        self.update_render = self.set_interval(1 / 60, self.update_spinner)

    def update_spinner(self) -> None:
        self.update(self._spinner)
        

class Cell(Widget):

    state = reactive(PlayerState.EMPTY)
    """This is modified by `cell_pressed` method in the GameManager class
    whenever a move is chosen by either the player or the computer."""

    x = r"""
\_/ 
/ \ """
    o = r""" __ 
/  \
\__/"""

    #* Sent by: on_click in this class.
    #* Handled by: cell_pressed in the main App.
    class Pressed(Message):
        def __init__(self, cell: Cell):
            super().__init__()
            self.cell = cell

    def __init__(
            self,
            row: int,
            column: int,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
        ):
        """ | Arg     | Description 
            |---------|-------------
            | row     | - The row of the cell 
            | column  | - The column of the cell
            | name    | - The name of the widget
            | id      | - The ID of the widget in the DOM
            | classes | - The CSS classes for the widget """
            
        super().__init__(name=name, id=id, classes=classes)
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

    BINDINGS = [
        Binding("enter", "select", "Select"),
        Binding("left", "left", "Move left", priority=True),
        Binding("right", "right", "Move right", priority=True),
        Binding("up", "up", "Move up"),
        Binding("down", "down", "Move down"),
    ]

    def __init__(
            self,
            rows: int,
            columns: int,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
        ):
        """ | Arg     | Description 
            |---------|-------------
            | rows    | - The number of rows in the grid
            | columns | - The number of columns in the grid
            | name    | - The name of the widget
            | id      | - The ID of the widget in the DOM
            | classes | - The CSS classes for the widget """
        
        super().__init__(name=name, id=id, classes=classes)
        self.rows:int = rows
        self.columns:int = columns
        self.styles.grid_size_rows = self.rows
        self.styles.grid_size_columns = self.columns
        self.styles.width = rows * 10
        self.styles.height = columns * 6 + 1
        self.can_focus = True
        self.focus_grid = [[0 for _ in range(columns)] for _ in range(rows)]
        # self.focus_grid = reactive([[0 for _ in range(columns)] for _ in range(rows)])

    def compose(self):

        for row in range(self.rows):
            for col in range(self.columns):
                yield Cell(row=row, column=col, id=f"cell_{row}_{col}", classes="gridcell bordered centered")

    def on_mount(self):
        self.focus_cell(0, 0)

    #* Called by: restart in main App.
    def clear_grid(self):
        for cell in self.query_children(Cell):
            cell.state = PlayerState.EMPTY

    def clear_focus(self):
        for cell in self.query_children(Cell):
            cell.remove_class("focusing")
        self.focus_grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def focus_cell(self, row: int, col: int):
        self.focus_grid[row][col] = 1
        self.query_one(f"#cell_{row}_{col}").add_class("focusing")

    def unfocus_cell(self, row: int, col: int):
        self.focus_grid[row][col] = 0
        self.query_one(f"#cell_{row}_{col}").remove_class("focusing")

    def get_focused_cell(self) -> tuple[int, int]:
        for row_index, row in enumerate(self.focus_grid):
            if 1 in row:
                col_index = row.index(1)
                return row_index, col_index

    def action_left(self):
        row_index, col_index = self.get_focused_cell()
        self.unfocus_cell(row_index, col_index)
        self.focus_cell(
            row_index, (col_index-1 if col_index != 0 else self.columns-1)
        ) # subtract 1 unless first column

    def action_right(self):
        row_index, col_index = self.get_focused_cell()
        self.unfocus_cell(row_index, col_index)
        self.focus_cell(
            row_index, (col_index+1 if col_index != self.columns-1 else 0)
        ) # add 1 unless last column

    def action_up(self):
        row_index, col_index = self.get_focused_cell()
        self.unfocus_cell(row_index, col_index)
        self.focus_cell(
            (row_index-1 if row_index != 0 else self.rows-1), col_index
        ) # subtract 1 unless first row

    def action_down(self):
        row_index, col_index = self.get_focused_cell()
        self.unfocus_cell(row_index, col_index)
        self.focus_cell(
            (row_index+1 if row_index != self.rows-1 else 0), col_index
        ) # add 1 unless last row

    def action_select(self):
        row_index, col_index = self.get_focused_cell()
        self.query_one(f"#cell_{row_index}_{col_index}").on_click()

class GameManager(Widget):

    #*Sent by: start_game, cell_pressed, computer_turn_orch in this class.
    #* Handled by: change_turn in main App.
    class ChangeTurn(Message):
        def __init__(self, value: PlayerState):
            super().__init__()
            self.value = value

    #* Sent by: calculate_winner in this class.
    #* Handled by: game_over in main App.
    class GameOver(Message):
        def __init__(self, result: PlayerState):
            super().__init__()
            self.result = result

    #* Sent by: computer_turn_orch in this class.
    #* Handled by: AI_move in main App.
    class AIMove(Message):
        def __init__(self, row: int, col: int):
            super().__init__()
            self.row = row
            self.col = col

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display = False
        self.game_running = False
    
    #* Called by: `mount_grid` and `restart` in main App.
    def start_game(self, grid_size: int):

        self.game_running = True
        self.grid_size = grid_size
        self.int_board = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.move_counter = 0

        self.post_message(self.ChangeTurn(PlayerState.PLAYER1))
        self.notify("Game started", timeout=1.5)

    #* Called by: cell_pressed in main App, forwarded from on_click in Cell class.
    async def cell_pressed(self, event: Cell.Pressed):

        cell = event.cell
        
        if cell.state != PlayerState.EMPTY:
            self.notify("Cell already taken", timeout=1)
            return
        if not self.game_running:
            return

        self.log.info(f"Cell pressed: {cell.row}, {cell.column} \n")

        cell.state = PlayerState.PLAYER1
        self.int_board[cell.row][cell.column] = 1
        self.move_counter += 1
        game_result = self.calculate_winner(self.int_board)
        if game_result is not None:
            self.post_message(self.GameOver(game_result))
            return
    
        self.post_message(self.ChangeTurn(PlayerState.PLAYER2))     # Change turn to AI
        # NOTE: I let the main app call the computer_turn_orch method to ensure the
        # UI is updated before it starts thinking.

    #* Called by: change_turn in main App.
    async def computer_turn_orch(self):

        self.minimax_counter = 0
        self.pruning_counter = 0
        self.depth_limit_counter = 0

        board_copy = deepcopy(self.int_board)
        worker = self.computer_turn_worker(board_copy)
        ai_row, ai_col = await worker.wait()
        if ai_row is None:
            raise ValueError("AI made an invalid move.")

        self.log(
            f"Minimax counter: {self.minimax_counter}\n"
            f"Branches pruned: {self.pruning_counter}\n"
            f"Times depth limit reached: {self.depth_limit_counter}\n"
        )        

        self.int_board[ai_row][ai_col] = 2              # Apply AI move to integer board
        self.move_counter += 1
        self.post_message(self.AIMove(ai_row, ai_col))  # Updates the cell state in the Grid

        game_result = self.calculate_winner(self.int_board)
        if game_result is not None:
            self.post_message(self.GameOver(game_result))
            return
        
        self.post_message(self.ChangeTurn(PlayerState.PLAYER1))     # Change turn back to human

    @work(thread=True)
    async def computer_turn_worker(self, board: list[list[int]]) -> tuple[int, int]:

        await sleep(0.5)            # Artificial delay to simulate thinking time
        _, best_move = self.minimax(board, depth=0, is_maximizing=True)    # AI is maximizer
        return best_move

    #* Called by: cell_pressed in this class.
    def calculate_winner(self, board: list[list[int]]) -> PlayerState | None:
        """Returns a PlayerState if game is over, else returns None."""

        rows      = board
        columns   = list(zip(*board))
        main_diag = [[board[i][i] for i in range(self.grid_size)]]
        anti_diag = [[board[i][self.grid_size - i - 1] for i in range(self.grid_size)]]

        # Combine all possible lines into a single list
        lines = (rows + columns + main_diag + anti_diag)

        def check_line(line, player):
            return all(cell == player for cell in line)

        for player in (1, 2):
            if any(check_line(line, player) for line in lines):     # Check for winner
                return PlayerState.PLAYER1 if player == 1 else PlayerState.PLAYER2

        if all(cell != 0 for row in board for cell in row):         # Check for draw
            return PlayerState.EMPTY
        
        return None


    def minimax(
        self,
        board: list[list[int]],
        depth: int,
        is_maximizing: bool,
        alpha: int = float('-inf'),
        beta: int = float('inf')
    ) -> tuple[int, tuple[int, int]]:       # score, best_move coordinates
        """ | Arg           | Description 
            |---------------|---------------------
            | board         | - The current game board state
            | depth         | - Current depth in the game tree
            | is_maximizing | - True if AI's turn (maximizing), False if human's turn (minimizing)

            Returns:
                tuple[int, int, int]: (best_score, best_row, best_col)"""

        self.minimax_counter += 1

        result = self.calculate_winner(board)

        # Base cases: game over scenarios
        if result == PlayerState.PLAYER2:       # AI is maximizer
            return 10 - depth, None
        elif result == PlayerState.PLAYER1:     # Human is minimizer
            return -10 + depth, None
        elif result == PlayerState.EMPTY:       # Draw
            return 0, None
        
        if self.grid_size <= 3:
            max_depth = 9
        if self.grid_size == 4:             
            max_depth = self.move_counter if self.move_counter < 5 else 5   # Starts at 1, increases to 5.
        if self.grid_size == 5:                                             # Makes it play fast without thinking much.
            max_depth = self.move_counter if self.move_counter < 3 else 3   # for 5x5 its capped at 3.

        if depth == max_depth:
            self.depth_limit_counter += 1
            return 0, None
    
        best_move  = (None, None)
        best_score = float('-inf') if is_maximizing else float('inf')
        player     =             2 if is_maximizing else 1
        
        # Try all possible moves
        for row, col in product(range(self.grid_size), range(self.grid_size)):
            if board[row][col] == 0:        # only empty cells

                board[row][col] = player
                score, _, = self.minimax(board, depth + 1, not is_maximizing, alpha, beta)
                board[row][col] = 0         # Undo move

                if is_maximizing and score > best_score:
                        best_score = score
                        alpha = max(score, alpha)
                        best_move = (row, col)
                elif not is_maximizing and score < best_score:
                        best_score = score
                        beta = min(score, beta)
                        best_move = (row, col)

                if beta <= alpha:
                    self.pruning_counter += 1
                    break

        return best_score, best_move

    @on(Worker.StateChanged)
    def worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.state == WorkerState.SUCCESS:
            self.log(Text(f"Worker {event.worker.name} completed successfully", style="green"))


#* Called by: on_mount in main app.
class MyScreen(ModalScreen):

    def compose(self):

        with Container(classes="auto bordered"):
            yield Label("Enter a number between 2 and 5: \n")
            yield Input(id="input", type="integer", validators=[Number(2, 5)], validate_on=["submitted"])
            yield Label("\nNote: AI won't play strategically \nfor grid sizes larger than 3. But it \n"
                        "should still block you from winning.")

    @on(Input.Submitted)
    def close(self, event: Input.Submitted):

        if not event.validation_result.is_valid:
            return
        else:
            self.dismiss(int(event.value))
        

class TicTacToe(App):

    DEFAULT_CSS = """
        .bar {width: 1fr;}
        .footer {height: 5;}
        .auto {width: auto; height: auto;}
        .centered {align: center middle; content-align: center middle;}
        .onefr {width: 1fr; height: 1fr;}
        Cell:hover {background: $secondary-background;}
        .header {
            height: 0.2fr;
            content-align: center bottom;
            align: center bottom;
        }
        .grid {
            layout: grid;
            grid-gutter: 0;
            padding: 0;
            margin: 0;
        }
        .gridcell {
            width: 10;
            height: 5;
            margin: 1 0 0 0;
        }
        .bordered {
            background: $surface-lighten-1;
            border: tall $primary-background;
            padding: 0 2 0 2;
            &.focusing {background: $secondary-background; border: tall $primary-lighten-1;}
        }
    """

    BINDINGS = [
        Binding("left", "focus_previous", "Move left"),
        Binding("right", "focus_next", "Move right"),
    ]    

    def compose(self):

        self.game_manager = GameManager()
        yield self.game_manager

        with Horizontal(classes="bar header"):
            yield Label(id="turn_label", classes="auto centered")
            yield SpinnerWidget("line", id="spinner", classes="auto centered")
        with Container(id="content", classes="onefr centered"):
            yield Static()
        with Horizontal(classes="centered bar footer"):
            yield Button("Restart", id="restart", classes="centered")
            yield Button("Change Size", id="change_size", classes="centered")
        yield Footer()

    def on_mount(self):
        self.query_one("#spinner").visible = False
        self.push_screen(MyScreen(classes="centered"), self.mount_grid)

    async def mount_grid(self, grid_size: int):

        self.grid_size = grid_size
        self.game_manager.start_game(grid_size)
        self.grid = Grid(rows=grid_size, columns=grid_size, classes="grid onefr")
        self.query_one("#content").remove_children()
        await self.query_one("#content").mount(self.grid)
        self.grid.focus()

    @on(Button.Pressed, "#restart")
    def restart(self):
        self.grid.clear_grid()
        self.game_manager.start_game(self.grid_size)
        self.grid.can_focus = True
        self.grid.focus()
        self.grid.focus_cell(0, 0)        

    @on(Button.Pressed, "#change_size")
    def change_size(self):
        self.push_screen(MyScreen(classes="centered"), self.mount_grid)

    ###~ Child Events ~###

    #* Sent by: on_click in Cell class.
    @on(Cell.Pressed)                   
    async def cell_pressed(self, event: Cell.Pressed):
        await self.game_manager.cell_pressed(event)

    #* Sent by: computer_turn in GameManager class.
    @on(GameManager.AIMove)
    def AI_move(self, event: GameManager.AIMove):

        cell = self.grid.query_one(f"#cell_{event.row}_{event.col}")
        cell.state = PlayerState.PLAYER2

    #* Sent by: start_game, cell_pressed, computer_turn_orch in GameManager class.
    @on(GameManager.ChangeTurn)         
    @work
    async def change_turn(self, event: GameManager.ChangeTurn):

        self.log.debug(f"Turn label changing to {event.value.name}")
        if event.value == PlayerState.PLAYER1:
            self.query_one("#spinner").visible = False
            self.query_one("#turn_label").update("Your turn")
        else:
            self.query_one("#spinner").visible = True
            self.query_one("#turn_label").update("Computer is thinking... ")
            await self.game_manager.computer_turn_orch()

    #* Sent by: calculate_winner in GameManager class.
    @on(GameManager.GameOver)           
    def game_over(self, event: GameManager.GameOver):
        
        self.query_one("#spinner").visible = False
        self.notify("Game over", timeout=1.5)
        if event.result == PlayerState.EMPTY:
            self.query_one("#turn_label").update("It's a tie!")
        else:
            self.query_one("#turn_label").update(f"{event.result.name} wins!")
        self.game_manager.game_running = False
        self.grid.clear_focus()
        self.grid.can_focus = False
        self.query_one("#restart").focus()


if __name__ == "__main__":
    TicTacToe().run()