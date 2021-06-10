# Author: Caroline Davis
# Date: 06/08/2021
# Description: This program generates a game of Kuba for 2 players. The program has multiple classes to handle
#   various aspects of the game, including the Players, the Board, and the game itself.


class KubaGame:
    """Class that creates a KubaGame object"""
    def __init__(self , player1_tuple , player2_tuple):
        """Function that initializes the data members in KubaGame"""
        self._current_turn = None
        self._winner = None
        self._player1 = Player(player1_tuple)
        self._player2 = Player(player2_tuple)
        self._player_list = [self._player1 , self._player2]
        self._game_board = Board()
        self._white_marbles = 8
        self._black_marbles = 8
        self._red_marbles = 13

    def get_current_turn(self):
        """Function that returns the playername whose turn it is"""
        return self._current_turn

    def get_winner(self):
        """Function that returns the playername who is the winner"""
        return self._winner

    def get_captured(self , playername):
        """Function that returns the amount of red marbles captured by
            a specified player"""
        for player in self._player_list:
            if player.get_name() == playername:
                return player.get_red_captures()

    def get_marble(self , coordinates):
        """Function that returns the marble at given coordinates on the board"""
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        marble = self._game_board.get_current_game_board()[row_coordinate][column_coordinate]
        return marble

    def get_marble_count(self):
        """Function that returns the total marbles count"""
        return self._white_marbles, self._black_marbles, self._red_marbles

    def make_move(self , playername , coordinates , direction):
        """Function that a user can call to move a specified marble, in the directions: "L", "R",
            "F" or "B"."""
        if playername == self._player1.get_name():
            current_player = self._player1
        else:
            current_player = self._player2

        if self._current_turn is None:
            self.initialize_game(current_player)

        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        current_board = self._game_board.get_current_game_board()
        player_color = current_player.get_color()
        columns = self._game_board.get_columns()

        if "X" in current_board[row_coordinate]:
            if "X" in columns[column_coordinate]:
                if direction == "L":
                    if current_board[row_coordinate][0] == player_color:
                        return False
                elif direction == "R":
                    if current_board[row_coordinate][6] == player_color:
                        return False
                elif direction == "F":
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
                                                      column_coordinate , direction)
                        return False
                    return False
                return False
            return False
        return False

    def initialize_game(self, current_player):
        """Function that initializes the KubaGame Board's columns and the current turn"""
        self._game_board.set_columns()
        self._current_turn = current_player.get_name()

    def set_current_turn(self):
        """Function to be used to set the current turn"""
        if self._current_turn == self._player1.get_name():
            self._current_turn = self._player2.get_name()
        else:
            self._current_turn = self._player1.get_name()

    def is_valid_move(self , current_player , row_coordinate , column_coordinate , direction):
        """Function to provide validation that the user-requested marble move is valid"""
        is_valid = False
        current_board = self._game_board.get_current_game_board()
        columns = self._game_board.get_columns()

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
                if row_coordinate + 1 > 6 or columns[column_coordinate][row_coordinate + 1] == "X":
                    is_valid = True

        elif direction == "B":
            if row_coordinate + 1 < 7:
                if row_coordinate - 1 < 0 or columns[column_coordinate][row_coordinate - 1] == "X":
                    is_valid = True

        if is_valid:
            captured = self._game_board.move_marble(current_player , row_coordinate ,
                                                    column_coordinate , direction)
            self.evaluate_win(current_player)
            self.set_current_turn()
            self._game_board.reset_columns()
            if captured != "X" and captured is not None:
                if captured == "R":
                    self.remove_marble("R")
                elif captured == "B":
                    self.remove_marble("B")
                elif captured == "W":
                    self.remove_marble("W")
                current_player.add_capture(captured)
        return is_valid

    def remove_marble(self , color):
        """Function that removes a marble from the count, based on color"""
        if color == "R":
            self._red_marbles -= 1
        elif color == "B":
            self._black_marbles -= 1
        elif color == "W":
            self._white_marbles -= 1

    def evaluate_win(self , player):
        """Function called to evaluate the win status of the game"""
        red_marbles = player.get_red_captures()
        opposite_marbles = player.get_opposite_captures()

        if red_marbles >= 7 or opposite_marbles == 8:
            self._winner = player.get_name()


class Player:
    """Class that creates a Player object"""
    def __init__(self , player_tuple):
        """Function that initializes the Player class data members"""
        self._player_name = player_tuple[0]
        self._player_color = player_tuple[1]
        self._player_red_captures = 0
        self._player_opposite_captures = 0

    def get_color(self):
        """Function that returns a Player object's chosen color"""
        return self._player_color

    def get_name(self):
        """Function that returns a Player object's chosen name"""
        return self._player_name

    def get_red_captures(self):
        """Function that returns a Player object's red marble captures"""
        return self._player_red_captures

    def get_opposite_captures(self):
        """Function that returns a Player object's opposition marble captures"""
        return self._player_opposite_captures

    def add_capture(self , color):
        """Function that adds a capture to a Player object, based on color"""
        if color == "B":
            self._player_opposite_captures += 1
        elif color == "W":
            self._player_opposite_captures += 1
        else:
            self._player_red_captures += 1


class Board:
    """Class that creates a Board Object"""
    def __init__(self):
        """Function that initializes the Board object's data members"""
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

    def set_columns(self):
        """Function that is called to set the initial columns on the board"""
        self._columns = []
        for row in range(7):
            column = []
            for index in range(7):
                column.append(self._current_game_board[row][index])
            self._columns.append(column)

    def reset_columns(self):
        """Function that is called after each marble move to reset the columns"""
        for row in range(7):
            for column in range(7):
                self._current_game_board[row][column] = self._columns[column][row]

    def get_columns(self):
        """Function that returns the columns board"""
        return self._columns

    def get_current_game_board(self):
        """Function that returns the current game board"""
        return self._current_game_board

    def get_previous_game_board(self):
        """Function that returns the previous game board"""
        return self._previous_game_board

    def move_marble(self , player , row_coordinate , column_coordinate , direction):
        """Function that moves the specified marble on the board"""
        self._previous_game_board = self._current_game_board
        captured = None

        if direction == "L":
            start_column = column_coordinate
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
            next_row = row_coordinate + 1
            count = start_row

            while row_coordinate != 0 and self._columns[column_coordinate][row_coordinate] != "X":
                count -= 1
                row_coordinate -= 1

            if row_coordinate == 0:
                captured = self._columns[column_coordinate][0]
                self._columns[column_coordinate][count:start_row] = self._columns \
                    [column_coordinate][count:next_row]
                del self._columns[column_coordinate][0]

            elif self._current_game_board[row_coordinate][column_coordinate] == "X":
                if start_row == 6:
                    self._columns[column_coordinate][count:start_row] = self._columns \
                        [column_coordinate][count+1:]
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

        return captured
