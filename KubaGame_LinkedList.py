class KubaGame:
    def __init__(self , player1_tuple , player2_tuple):
        self._current_turn = None
        self._winner = None
        self._game_board = Board()
        self._player1 = Player(player1_tuple)
        self._player2 = Player(player2_tuple)
        self._marbles = Marbles()
        self._marbles_linked_list = MarblesLinked
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
            self.initialize_board()
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

    def initialize_board(self):
        current_board = self._game_board.get_current_game_board()
        for row in range(0, len(current_board)):
            marbles_linked = self._marbles_linked_list(row)
            for column in range(0, len(current_board[row])):
                color = current_board[row][column]
                marbles_linked.add(color, row)
            current_board.add_linked_row(marbles_linked, row)
        print(self._game_board.get_linked_rows())

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
        self._current_game_board = [['W' , 'W' , 'X' , 'X' , 'X' , 'B' , 'B', "None"] ,
                                    ['W' , 'W' , 'X' , 'R' , 'X' , 'B' , 'B', "None"] ,
                                    ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X', "None"] ,
                                    ['X' , 'R' , 'R' , 'R' , 'R' , 'R' , 'X', "None"] ,
                                    ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X', "None"] ,
                                    ['B' , 'B' , 'X' , 'R' , 'X' , 'W' , 'W', "None"] ,
                                    ['B' , 'B' , 'X' , 'X' , 'X' , 'W' , 'W', "None"]
                                    ]
        self._previous_game_board = [['W' , 'W' , 'X' , 'X' , 'X' , 'B' , 'B'] ,
                                     ['W' , 'W' , 'X' , 'R' , 'X' , 'B' , 'B'] ,
                                     ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                     ['X' , 'R' , 'R' , 'R' , 'R' , 'R' , 'X'] ,
                                     ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                                     ['B' , 'B' , 'X' , 'R' , 'X' , 'W' , 'W'] ,
                                     ['B' , 'B' , 'X' , 'X' , 'X' , 'W' , 'W']
                                     ]
        self._rows_linked_list = [[] , [] , [] , [] , [] , [] , []]

    def add_linked_row(self, linked_list, row):
        self._rows_linked_list[row] = linked_list

    def get_linked_rows(self):
        return self._rows_linked_list

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
    def __init__(self, color):
        self._color = color
        self._next = None
        self._row = None
        self._column = None

    def set_marble_color(self , color):
        """Function to set the data value of the Node object"""
        self._color = color

    def set_marble_next(self , node):
        """Function to set the next node of the current Node object"""
        self._next = node

    def set_marble_row(self, row):
        self._row = row

    def set_marble_column(self, column):
        self._column = column

    def get_marble_color(self):
        """Function to get the data value of the Node object"""
        return self._color

    def get_marble_next(self):
        """Function to get the next value of the Node object"""
        return self._next

    def get_marble_row(self):
        return self._row

    def get_marble_column(self):
        return self._column



class MarblesLinked:
    def __init__(self, row):
        """Function that initializes the data member of the linked list - the head (first Node) of the list"""
        self._head = None
        self._row = row

    def add(self, color, row):
        """
        Adds a node containing val to the linked list
        """
        self._row = row

        if self._head is None:
            self._head = MarbleNode(color)
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = MarbleNode(color)

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