from enum import Enum
from typing import Optional

from board import Board, DiscColor
from player import Player

class GameState(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    WON = "WON"
    DRAW = "DRAW"


class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.state = GameState.IN_PROGRESS
        self.winner: Optional["Player"] = None

    def make_move(self, player, column: int) -> bool:
        if self.state is not GameState.IN_PROGRESS:
            return False
        if player is not self.current_player:
            return False

        row = self.board.place_disc(column, player.color)
        if row == -1:
            return False

        if self.board.check_win(row, column, player.color):
            self.state = GameState.WON
            self.winner = player
        elif self.board.is_full():
            self.state = GameState.DRAW
        else:
            self.current_player = self.player2 if self.current_player is self.player1 else self.player1

        return True

    def get_current_player(self) -> Player:
        return self.current_player

    def get_game_state(self) -> GameState:
        return self.state

    def get_winner(self) -> Optional[Player]:
        return self.winner

    def get_board(self) -> Board:
        return self.board


def main() -> None:
    red_player = Player("Player 1", DiscColor.RED)
    yellow_player = Player("Player 2", DiscColor.YELLOW)
    game = Game(red_player, yellow_player)

    while game.get_game_state() is GameState.IN_PROGRESS:
        player = game.get_current_player()
        try:
            column = int(input(f"{player.name} ({player.color.value}), choose a column (1-7): ")) - 1
        except ValueError:
            print("Please enter a number from 1 to 7.")
            continue

        if not game.make_move(player, column):
            print("Invalid move. Choose a non-full column from 1 to 7.")

    if game.get_game_state() is GameState.WON:
        print(f"{game.get_winner().name} wins!")
    else:
        print("The game is a draw.")


if __name__ == "__main__":
    main()

