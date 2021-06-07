# Author: Caroline Davis
# Date: 05/28/2021
# Description: ...


class KubaGame:
    def __init__(self , player1_tuple , player2_tuple):
        self._current_turn = None
        self._winner = None
        self._game_board = Board()
        self._player1 = Player(player1_tuple)
        self._player2 = Player(player2_tuple)
        self._marbles = Marbles()
        self._player_list = [self._player1 , self._player2]

    def get_current_turn(self):
        return self._current_turn

    def make_move(self , playername , coordinates , direction):
        player_requesting = None
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        current_board = self._game_board.get_current_game_board()

        for player in self._player_list:
            if playername == player.get_name():
                player_requesting = player
        player_requesting_name = player_requesting.get_name()

        if self._current_turn is None:
            self._current_turn = player_requesting_name
        elif self._current_turn != playername:
            return False

        current_player = player_requesting

        if 0 <= row_coordinate <= 6:
            if 0 <= column_coordinate <= 6:
                if current_player.get_color() == current_board[row_coordinate][column_coordinate]:
                    if self._winner is None:
                        return self.is_valid_move(current_player, coordinates , direction)
                    return False
                return False
            return False
        return False

    def is_valid_move(self , player , coordinates , direction):
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        current_board = self._game_board.get_current_game_board()

        if direction == "L":
            if column_coordinate - 1 < 0:
                return False
            elif column_coordinate + 1 > 6 or current_board[row_coordinate][column_coordinate + 1] == "X":
                return self._game_board.move_marble(player, coordinates , direction)
            return False

        elif direction == "R":
            if column_coordinate + 1 > 6:
                return False
            elif column_coordinate - 1 >= -1 or current_board[row_coordinate][column_coordinate - 1] == "X":
                return self._game_board.move_marble(player, coordinates , direction)
            return False

        elif direction == "F":
            if row_coordinate - 1 < 0:
                return False
            elif row_coordinate + 1 > 6 or current_board[row_coordinate + 1][column_coordinate] == "X":
                return self._game_board.move_marble(player, coordinates , direction)
            return False

        elif direction == "B":
            if row_coordinate + 1 > 6:
                return False
            elif row_coordinate - 1 < 0 or current_board[row_coordinate - 1][column_coordinate] == "X":
                return self._game_board.move_marble(player, coordinates , direction)
            return False

    def get_winner(self):
        return self._winner

    def get_captured(self , playername):
        for player in self._player_list:
            if player.get_name() == playername:
                return player.get_captures()
        return 0

    def get_marble(self , coordinates):
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        current_board = self._game_board.get_current_game_board()
        return current_board[row_coordinate][column_coordinate]

    def get_marble_count(self):
        return self._marbles.total_marbles()


class Player:
    def __init__(self , player_tuple):
        self._player_name = player_tuple[0]
        self._player_color = player_tuple[1]
        self._player_captures = 0

    def get_color(self):
        return self._player_color

    def get_name(self):
        return self._player_name

    def get_captures(self):
        return self._player_captures

    def add_capture(self):
        self._player_captures += 1


class Board:
    def __init__(self):
        self._start_game_board = [['W' , 'W' , 'X' , 'X' , 'X' , 'B' , 'B'] ,
                                  ['W' , 'W' , 'X' , 'R' , 'X' , 'B' , 'B'] ,
                                  ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                  ['X' , 'R' , 'R' , 'R' , 'R' , 'R' , 'X'] ,
                                  ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                  ['B' , 'B' , 'X' , 'R' , 'X' , 'W' , 'W'] ,
                                  ['B' , 'B' , 'X' , 'X' , 'X' , 'W' , 'W']
                                  ]
        self._current_game_board = [['W' , 'W' , 'X' , 'X' , 'X' , 'B' , 'B'] ,
                                    ['W' , 'W' , 'X' , 'R' , 'X' , 'B' , 'B'] ,
                                    ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                    ['X' , 'R' , 'R' , 'R' , 'R' , 'R' , 'X'] ,
                                    ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                    ['B' , 'B' , 'X' , 'R' , 'X' , 'W' , 'W'] ,
                                    ['B' , 'B' , 'X' , 'X' , 'X' , 'W' , 'W']
                                    ]
        self._previous_game_board = [['W' , 'W' , 'X' , 'X' , 'X' , 'B' , 'B'] ,
                                     ['W' , 'W' , 'X' , 'R' , 'X' , 'B' , 'B'] ,
                                     ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                     ['X' , 'R' , 'R' , 'R' , 'R' , 'R' , 'X'] ,
                                     ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                     ['B' , 'B' , 'X' , 'R' , 'X' , 'W' , 'W'] ,
                                     ['B' , 'B' , 'X' , 'X' , 'X' , 'W' , 'W']
                                     ]

    def get_start_game_board(self):
        return self._start_game_board

    def get_current_game_board(self):
        return self._current_game_board

    def get_previous_game_board(self):
        return self._previous_game_board

    def move_marble(self , player, coordinates , direction):
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        current_board = self._current_game_board
        previous_board = self._previous_game_board
        current = current_board[row_coordinate][column_coordinate]
        previous = None
        playername = player.get_name()

        if direction == "L":
            start = column_coordinate
            next = current_board[row_coordinate][column_coordinate + 1]

            while self._current_game_board[row_coordinate][column_coordinate] != "X" or column_coordinate < 6:
                previous = current
                current = next
                next = current_board[row_coordinate][column_coordinate + 1]
                next = playername
                column_coordinate += 1

            current_board[row_coordinate][start] = "X"

            if column_coordinate == 6:
                knock_off = current
                current = previous






        elif direction == "R":

        elif direction == "F":

        elif direction == "B":

class MarbleNode:
    def __init__(self, data):
        self._data = data
        self._next = None

class Marbles:
    def __init__(self):
        self._white_marbles = 8
        self._black_marbles = 8
        self._red_marbles = 13

    def total_marbles(self):
        """
        Purpose and return: Creates a tuple containing the number of white, black, and red marbles, then returns it.
        """
        marble_count = (self._white_marbles , self._black_marbles , self._red_marbles)
        return marble_count

    def remove_marble(self , color):
        """
        Purpose: When a marble is knocked off the board, this function can be called to remove the marble from the count
        :param color: String signifying what color the marble is - either "R", "B", or "W"
        Return Values: None --> updates data member associated with marble color count.
        """
        if color == "R":
            self._red_marbles -= 1
        elif color == "B":
            self._black_marbles -= 1
        elif color == "W":
            self._white_marbles -= 1


# ---------------------------------------- Tests ------------------------------------- #
# FROM CANVAS:
# game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))
# game.get_marble_count() #returns (8,8,13)
# game.get_captured('PlayerA') #returns 0
# game.get_current_turn() #returns 'PlayerB' because PlayerA has just played.
# game.get_winner() #returns None
# game.make_move('PlayerA', (6,5), 'F')
# game.make_move('PlayerA', (6,5), 'L') #Cannot make this move
# game.get_marble((5,5)) #returns 'W'


# CAROLINE'S TESTS:
game = KubaGame(("Randy" , "W") , ("John" , "B"))
print(game.get_marble((0 , 2)))
