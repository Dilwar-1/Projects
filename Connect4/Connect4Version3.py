from enum import Enum
from typing import TypeAlias, Optional, List 
import sys
from dataclasses import dataclass
import time
import random

# Defining token types X and O
@dataclass(eq=True, frozen=True)
class X:
    def __str__(self):
        return "X"

@dataclass(eq=True, frozen=True)
class O:
    def __str__(self):
        return "O"

# Define Token type as the union of X and O --- Let Token [X,O]
Token: TypeAlias = X | O

# Defining the possible states of the cell --- Let Cell = Token U None
Cell: TypeAlias = Token | None

# Defining a column
Column: TypeAlias = tuple[Cell, Cell, Cell, Cell, Cell, Cell]

# Defining the grid
Grid: TypeAlias = tuple[Column, Column, Column, Column, Column, Column, Column]

#Now, we will define the player types we have planned.
@dataclass(eq=True, frozen=True)
class Player:
    pass

@dataclass(eq=True, frozen=True)
class CPU:
    pass

# Define PlayerType as the union of Player and CPU --- Let PlayerType = {Player} U {CPU}
PlayerType: TypeAlias = Player | CPU

# Define PlayerDetails as a tuple of PlayerType, String, and Token
PlayerDetails: TypeAlias = tuple[PlayerType, str, Token]

# Define MultiPlayers as a tuple of two PlayerDetails
MultiPlayers: TypeAlias = tuple[PlayerDetails, PlayerDetails]

def check_empty_cell(c:Column) -> bool:
    for i in range(0, len(c)):
        if c[i] == None:
            return True
    return False

def place_token_in_column(c: Column, t: Token) -> Optional[Column]:
     # Can I place the token in the column (is there any empty cells?)
    if not check_empty_cell(c):
        return None
    # Where can I place the token in the column (what is the coordinate?)
    for i in range(len(c)-1, -1, -1):
        if c[i] is None:
            new_column = list(c)
            new_column[i] = t
            return tuple(new_column)
    return None

def parse_token(s: str) -> Optional[Token]:
    match s.lower():
        case "x":
            return X()
        case "o":
            return O()
        case _:
            return None

def init_grid() -> Grid:
    empty_cell: Cell = None
    empty_column: Column = (empty_cell, empty_cell, empty_cell, empty_cell, empty_cell, empty_cell)
    empty_grid: Grid = (empty_column, empty_column, empty_column, empty_column, empty_column, empty_column, empty_column)
    return empty_grid

def draw_grid(grd: Grid) -> None:
    for row in range(6):
        print("|", end="")
        for col in range(7):
            cell = grd[col][row]
            print(f" {str(cell) if cell else ' '} |", end="")
        print()
    print("-" * 29)

def check_for_winner(grd: Grid, token: Token) -> bool:
    def check_for_four(start_col, start_row, delta_col, delta_row):
        for i in range(4):
            col = start_col + i * delta_col
            row = start_row + i * delta_row
            if not (0 <= col < 7 and 0 <= row < 6 and grd[col][row] == token):
                return False
        return True

    for col in range(7):
        for row in range(6):
            if (check_for_four(col, row, 1, 0) or
                check_for_four(col, row, 0, 1) or
                check_for_four(col, row, 1, 1) or
                check_for_four(col, row, 1, -1)):
                return True
    return False

def check_for_draw(grd: Grid) -> bool:
    return all(cell is not None for col in grd for cell in col)

def prompt_for_input(parse_func, message, err_msg):
    def inner():
        while True:
            match parse_func(input(message)):
                case None:
                    print(err_msg, file=sys.stderr)
                case x:
                    return x
    return inner

def prompt_for_column() -> int:
    while True:
        try:
            column = int(input("Please choose a column (1-7): ")) - 1
            if 0 <= column < 7:
                return column
            else:
                print("ERROR: Invalid column. Please select a valid column (1-7).", file=sys.stderr)
        except ValueError:
            print("ERROR: Invalid input. Please enter a number (Accepted Numbers: 1-7).", file=sys.stderr)

def create_player(player_type: PlayerType, name: str, tkn: Token) -> PlayerDetails:
    return (player_type, name, tkn)

def create_players(p1: PlayerDetails, p2: PlayerDetails) -> MultiPlayers:
    return (p1, p2)

def Init_player(player_type: PlayerType, prompt_message: str, tkn: Token) -> PlayerDetails:
    p_name = input(prompt_message)
    return create_player(player_type, p_name, tkn)

def get_token(existing_token: Optional[Token]) -> Token:
    return O() if isinstance(existing_token, X) else X()

def init_two_players() -> MultiPlayers:
    p1 = Init_player(Player(), "Player 1, Please input your name: ", get_token(None))
    p2 = Init_player(Player(), "Player 2, Please input your name: ", get_token(p1[2]))
    return create_players(p1, p2)

def init_player_and_cpu() -> MultiPlayers:
    p1 = Init_player(Player(), "Please input your name: ", get_token(None))
    p2 = create_player(CPU(), "CPU", get_token(p1[2]))
    return create_players(p1, p2)

def make_move(player: PlayerDetails, grid: Grid) -> Grid:
    while True:
        col = prompt_for_column()
        new_column = place_token_in_column(grid[col], player[2])
        if new_column is None:
            print("ERROR: Column is full. Try again.")
        else:
            new_grid = list(grid)
            new_grid[col] = new_column
            return tuple(new_grid)

def cpu_token_placement(player: PlayerDetails, grid: Grid) -> Grid:
    while True:
        col = random.randint(0, 6)
        new_column = place_token_in_column(grid[col], player[2])
        if new_column is not None:
            new_grid = list(grid)
            new_grid[col] = new_column
            return tuple(new_grid)

def change_player_order(players: MultiPlayers) -> MultiPlayers:
    return (players[1], players[0])

def gameplay_loop(players: MultiPlayers, grid: Grid) -> None:
    while True:
        draw_grid(grid)
        print(f"{players[0][1]}'s turn.")
        if isinstance(players[0][0], CPU):
            time.sleep(2)
            grid = cpu_token_placement(players[0], grid)
        else:
            grid = make_move(players[0], grid)
        if check_for_winner(grid, players[0][2]):
            draw_grid(grid)
            print(f"{players[0][1]} wins!")
            return
        if check_for_draw(grid):
            draw_grid(grid)
            print("It's a draw!")
            return
        players = change_player_order(players)

def multiplayer_game():
    players = init_two_players()
    grid = init_grid()
    gameplay_loop(players, grid)

def singleplayer_game():
    players = init_player_and_cpu()
    grid = init_grid()
    gameplay_loop(players, grid)

class MenuOption(Enum):
    SinglePlayer = 1
    MultiPlayer = 2
    Exit = 3

    @staticmethod
    def parse(s: str) -> Optional['MenuOption']:
        match s.strip().lower():
            case "1" | "singleplayer": return MenuOption.SinglePlayer
            case "2" | "multiplayer": return MenuOption.MultiPlayer
            case "3" | "exit" | "q": return MenuOption.Exit
            case _: return None

def prompt_for_input(parse_func, message, err_msg):
    def inner():
        while True:
            match parse_func(input(message)):
                case None:
                    print(err_msg, file=sys.stderr)
                case x:
                    return x
    return inner

prompt_for_menu_option = prompt_for_input(MenuOption.parse, 
                                          "Please choose an option:\n1 : Single Player - Play against a CPU\n2 : MultiPlayer - Play against another player\n3 : Exit\n", 
                                          "ERROR: Invalid menu option. Please select a valid option ranging from 1-3.")

def exit_program() -> int:
    print("Exiting Program: Dilwar - Connect4\nThanks for Playing!", file=sys.stdout)
    return 0

def main(argv: List[str]) -> int:
    while True:
        menu_choice = prompt_for_menu_option()
        match menu_choice:
            case MenuOption.SinglePlayer:
                singleplayer_game()
            case MenuOption.MultiPlayer:
                multiplayer_game()
            case MenuOption.Exit:
                return exit_program()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
