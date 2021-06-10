class KubaGame:
    def __init__(self , player1_tuple , player2_tuple):
        self._current_turn = None
        self._winner = None
        self._player1 = Player(player1_tuple)
        self._player2 = Player(player2_tuple)
        self._marbles_count = Marbles()
        self._game_board = Board()
        self._player_list = [self._player1 , self._player2]

    def get_current_turn(self):
        return self._current_turn

    def get_winner(self):
        return self._winner

    def get_captured(self , playername):
        for player in self._player_list:
            if player.get_name() == playername:
                return player.get_red_captures()

    def get_marble(self , coordinates):
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        marble = self._game_board.get_current_game_board()[row_coordinate][column_coordinate]
        return marble

    def get_marble_count(self):
        return self._marbles_count.total_marbles()

    def make_move(self , playername , coordinates , direction):
        self._game_board.set_columns()
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        current_board = self._game_board.get_current_game_board()
        columns = self._game_board.get_columns()
        current_player = None
        other_player = None

        for player in self._player_list:
            if playername == player.get_name():
                current_player = player
            other_player = player
        if self._current_turn is None:
            self._current_turn = current_player.get_name()

        player_color = current_player.get_color()

        if "X" not in current_board[row_coordinate]:
            if direction == "L":
                if current_board[row_coordinate][0] == player_color:
                    return False
            elif direction == "R":
                if current_board[row_coordinate][6] == player_color:
                    return False
        elif "X" not in columns[column_coordinate]:
            if direction == "F":
                if columns[column_coordinate][0] == player_color:
                    return False
            elif direction == "B":
                if columns[column_coordinate][6] == player_color:
                    return False

        if self._current_turn == current_player.get_name():
            if 0 <= row_coordinate <= 6:
                if 0 <= column_coordinate <= 6:
                    if current_player.get_color() == current_board[row_coordinate][column_coordinate]:
                        if self._winner is None:
                            return self.is_valid_move(current_player , row_coordinate ,
                                                      column_coordinate , direction, other_player)
                        return False
                    return False
                return False
            return False
        return False

    def set_current_turn(self, playername):
        self._current_turn = playername

    def is_valid_move(self , current_player , row_coordinate , column_coordinate , direction, other_player):
        is_valid = False
        current_board = self._game_board.get_current_game_board()

        if direction == "L":
            if column_coordinate - 1 > 0:
                if column_coordinate + 1 > 6 or current_board[row_coordinate][column_coordinate + 1] == "X":
                    is_valid = True

        elif direction == "R":
            if column_coordinate + 1 < 7:
                if column_coordinate - 1 < 0 or current_board[row_coordinate][column_coordinate - 1] == "X":
                    is_valid = True

        elif direction == "F":
            if row_coordinate - 1 > 0:
                if row_coordinate + 1 > 6 or current_board[row_coordinate + 1][column_coordinate] == "X":
                    is_valid = True

        elif direction == "B":
            if row_coordinate + 1 < 7:
                if row_coordinate - 1 < 0 or current_board[row_coordinate - 1][column_coordinate] == "X":
                    is_valid = True

        if is_valid:
            self._game_board.move_marble(current_player , row_coordinate , column_coordinate , direction)
            self.evaluate_win(current_player)
            self.set_current_turn(other_player.get_name())

        return is_valid

    def evaluate_win(self , player):
        red_marbles = player.get_red_captures()
        opposite_marbles = player.get_opposite_captures()

        if red_marbles >= 7 or opposite_marbles == 8:
            self._winner = player.get_name()


class Player:
    def __init__(self , player_tuple):
        self._player_name = player_tuple[0]
        self._player_color = player_tuple[1]
        self._player_red_captures = 0
        self._player_opposite_captures = 0

    def get_color(self):
        return self._player_color

    def get_name(self):
        return self._player_name

    def get_red_captures(self):
        return self._player_red_captures

    def get_opposite_captures(self):
        return self._player_opposite_captures

    def add_capture(self , color):
        if color == "B" or "W":
            self._player_opposite_captures += 1
        elif color == "R":
            self._player_red_captures += 1


class Board:
    def __init__(self):
        self._current_game_board = [['W' , 'W' , 'X' , 'X' , 'X' , 'B' , 'B'] ,
                                    ['W' , 'W' , 'X' , 'R' , 'X' , 'B' , 'B'] ,
                                    ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                    ['X' , 'R' , 'R' , 'R' , 'R' , 'R' , 'X'] ,
                                    ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                    ['B' , 'B' , 'X' , 'R' , 'X' , 'W' , 'W'] ,
                                    ['B' , 'B' , 'X' , 'X' , 'X' , 'W' , 'W']
                                    ]
        self._columns = []
        self._previous_game_board = self._current_game_board
        self._rows_linked_list = []
        self._marbles = Marbles()

    def set_columns(self):
        self._columns = []
        for row in range(7):
            column = []
            for index in range(7):
                column.append(self._current_game_board[row][index])
            self._columns.append(column)

    def get_columns(self):
        return self._columns

    def get_current_game_board(self):
        return self._current_game_board

    def get_previous_game_board(self):
        return self._previous_game_board

    def move_marble(self , player , row_coordinate , column_coordinate , direction):
        self._previous_game_board = self._current_game_board
        color = player.get_color()
        opposite_color = None
        captured = None

        if color == "W":
            opposite_color = "B"
        elif color == "B":
            opposite_color = "W"

        if direction == "L":
            start_column = column_coordinate
            next_column = column_coordinate - 1
            count = start_column

            while column_coordinate != 0 and self._current_game_board[row_coordinate][column_coordinate] != "X":
                count -= 1
                column_coordinate -= 1

            if column_coordinate == 0:
                captured = self._current_game_board[row_coordinate][0]
                self._current_game_board[row_coordinate][count:start_column] = self._current_game_board \
                    [row_coordinate][count + 1:]
                del self._current_game_board[row_coordinate][0]

            elif self._current_game_board[row_coordinate][column_coordinate] == "X":
                if start_column == 6:
                    self._current_game_board[row_coordinate][count:start_column] = self._current_game_board \
                        [row_coordinate][count+1:]
                else:
                    self._current_game_board[row_coordinate][count:start_column] = self._current_game_board \
                        [row_coordinate][count+1:start_column+1]
            self._current_game_board[row_coordinate][start_column] = "X"

        elif direction == "R":
            start_column = column_coordinate
            next_column = column_coordinate + 1
            count = start_column

            while column_coordinate != 6 and self._current_game_board[row_coordinate][column_coordinate] != "X":
                count += 1
                column_coordinate += 1

            if column_coordinate == 6:
                captured = self._current_game_board[row_coordinate][6]
                self._current_game_board[row_coordinate][next_column:] = self._current_game_board \
                    [row_coordinate][start_column:count]
                del self._current_game_board[row_coordinate][6]

            elif self._current_game_board[row_coordinate][column_coordinate] == "X":
                self._current_game_board[row_coordinate][next_column:count + 1] = self._current_game_board \
                    [row_coordinate][start_column:count]
            self._current_game_board[row_coordinate][start_column] = "X"

        elif direction == "F":
            start_row = row_coordinate
            next_row = row_coordinate - 1
            count = start_row

            while row_coordinate != 0 and self._columns[column_coordinate][row_coordinate] != "X":
                count -= 1
                row_coordinate -= 1

            if row_coordinate == 0:
                captured = self._columns[column_coordinate][0]
                self._columns[column_coordinate][next_row:] = self._columns \
                    [column_coordinate][start_row:count + 1]
                del self._columns[column_coordinate][0]

            elif self._current_game_board[row_coordinate][column_coordinate] == "X":
                if start_row == 6:
                    self._columns[column_coordinate][count:start_row] = self._columns \
                        [column_coordinate][count:]
                else:
                    self._columns[column_coordinate][count:start_row] = self._current_game_board \
                        [column_coordinate][count:start_row + 1]
            self._columns[column_coordinate][start_row] = "X"

        elif direction == "B":
            start_row = row_coordinate
            next_row = row_coordinate + 1
            count = start_row

            while row_coordinate != 6 and self._columns[column_coordinate][row_coordinate] != "X":
                count += 1
                row_coordinate += 1

            if row_coordinate == 6:
                captured = self._columns[column_coordinate][6]
                self._columns[column_coordinate][next_row:] = self._columns \
                    [column_coordinate][start_row:count]
                del self._columns[column_coordinate][6]

            elif self._columns[column_coordinate][row_coordinate] == "X":
                self._columns[column_coordinate][next_row:count + 1] = self._columns \
                    [column_coordinate][start_row:count]

            self._columns[column_coordinate][start_row] = "X"

        if captured is not None and captured != "X":
            if captured == "R":
                self._marbles.remove_marble("R")
            elif captured == opposite_color:
                self._marbles.remove_marble(opposite_color)
            player.add_capture(captured)


class Marbles:
    def __init__(self):
        self._white_marbles = 8
        self._black_marbles = 8
        self._red_marbles = 13

    def total_marbles(self):
        marble_count = (self._white_marbles , self._black_marbles , self._red_marbles)
        return marble_count

    def remove_marble(self , color):
        if color == "R":
            self._red_marbles -= 1
        elif color == "B":
            self._black_marbles -= 1
        elif color == "W":
            self._white_marbles -= 1


def main():
    game = KubaGame(('PlayerA' , 'W') , ('PlayerB' , 'B'))
    print(game.get_marble_count())  # returns (8,8,13)
    print(game.get_captured('PlayerA'))  # returns 0
    print(game.get_winner())  # returns None
    print(game.make_move('PlayerA' , (6 , 5) , 'F'))
    print(game.get_current_turn())  # returns 'PlayerB' because PlayerA has just played.
    print(game.make_move('PlayerA' , (6 , 5) , 'L'))  # Cannot make this move
    print(game.get_marble((5 , 5)))  # returns 'W'
    print(game.make_move('PlayerB' , (0 , 5) , 'B'))
    print(game.make_move('PlayerA' , (5 , 5) , 'F'))
    print(game.make_move('PlayerB' , (1 , 5) , 'B'))
    print(game.make_move('PlayerA' , (4 , 5) , 'F'))
    print(game.make_move('PlayerB' , (0 , 6) , 'B'))
    print(game.make_move('PlayerA' , (3 , 5) , 'F'))
    print(game.make_move('PlayerB' , (1 , 6) , 'B'))
    print(game.make_move('PlayerA' , (2 , 5) , 'F'))
    print(game.make_move('PlayerB' , (2 , 6) , 'B'))
    print(game.make_move('PlayerA' , (1 , 5) , 'F'))
    print(game.make_move('PlayerB' , (3 , 6) , 'B'))
    print(game.get_captured("PlayerA"))


if __name__ == "__main__":
    main()



# ---------------------------------------- Tests ------------------------------------- #
# # FROM CANVAS:
# game = KubaGame(('PlayerA' , 'W') , ('PlayerB' , 'B'))
# print(game.get_marble_count())  # returns (8,8,13)
# print(game.get_captured('PlayerA'))  # returns 0
# print(game.get_winner())  # returns None
# print(game.make_move('PlayerA' , (6 , 5) , 'F'))
# print(game.get_current_turn())  # returns 'PlayerB' because PlayerA has just played.
# print(game.make_move('PlayerA' , (6 , 5) , 'L'))  # Cannot make this move
# print(game.get_marble((5 , 5)))  # returns 'W'


# CAROLINE'S TESTS:
# game = KubaGame(("Randy" , "W") , ("John" , "B"))
# print(game.get_marble((0 , 2)))
