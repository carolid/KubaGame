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
                        return self.is_valid_move(current_player , coordinates , direction)
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
                return self._game_board.move_marble(player , coordinates , direction)
            return False

        elif direction == "R":
            if column_coordinate + 1 > 6:
                return False
            elif column_coordinate - 1 >= -1 or current_board[row_coordinate][column_coordinate - 1] == "X":
                return self._game_board.move_marble(player , coordinates , direction)
            return False

        elif direction == "F":
            if row_coordinate - 1 < 0:
                return False
            elif row_coordinate + 1 > 6 or current_board[row_coordinate + 1][column_coordinate] == "X":
                return self._game_board.move_marble(player , coordinates , direction)
            return False

        elif direction == "B":
            if row_coordinate + 1 > 6:
                return False
            elif row_coordinate - 1 < 0 or current_board[row_coordinate - 1][column_coordinate] == "X":
                return self._game_board.move_marble(player , coordinates , direction)
            return False

    def initialize_board(self):
        current_board = self._game_board.get_current_game_board()

        for row in range(0 , len(current_board)):
            marbles_linked = self._marbles_linked_list(row)
            for column in range(0 , len(current_board[row])):
                color = current_board[row][column]
                marbles_linked.add(color , row , column)
            self._game_board.add_linked_row(marbles_linked)

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
        self._current_game_board = self._start_game_board
        self._previous_game_board = self._current_game_board
        self._rows_linked_list = []

    def add_linked_row(self , linked_list):
        self._rows_linked_list.append(linked_list)

    def display_linked_row(self , row):
        row_to_display = self._rows_linked_list[row]
        row_to_display.display()

    def get_linked_rows(self):
        return self._rows_linked_list

    def get_start_game_board(self):
        return self._start_game_board

    def get_current_game_board(self):
        return self._current_game_board

    def get_previous_game_board(self):
        return self._previous_game_board

    def move_marble(self , player , coordinates , direction):
        pass
        # row_coordinate = coordinates[0]
        # column_coordinate = coordinates[1]
        # current_board = self._current_game_board
        # previous_board = self._previous_game_board
        # current = current_board[row_coordinate][column_coordinate]
        # previous = None
        # playername = player.get_name()
        #
        # if direction == "L":
        #     start = column_coordinate
        #     next = current_board[row_coordinate][column_coordinate + 1]
        #
        #     while self._current_game_board[row_coordinate][column_coordinate] != "X" or column_coordinate < 6:
        #         previous = current
        #         current = next
        #         next = current_board[row_coordinate][column_coordinate + 1]
        #         next = playername
        #         column_coordinate += 1
        #
        #     current_board[row_coordinate][start] = "X"
        #
        #     if column_coordinate == 6:
        #         knock_off = current
        #         current = previous
        #
        #
        #
        #
        #
        #
        # elif direction == "R":
        #
        # elif direction == "F":
        #
        # elif direction == "B":


class MarbleNode:
    def __init__(self , color , row , column):
        self._color = color
        self._next = None
        self._below = None
        self._above = None
        self._row = row
        self._column = column

    def set_marble_color(self , color):
        """Function to set the data value of the Node object"""
        self._color = color

    def set_marble_next(self , marble):
        """Function to set the next node of the current Node object"""
        self._next = marble

    def set_marble_row(self , row):
        self._row = row

    def set_marble_column(self , column):
        self._column = column

    def set_marble_above(self, marble):
        self._above = marble

    def set_marble_below(self, marble):
        self._below = marble

    def get_marble_color(self):
        """Function to get the data value of the Node object"""
        return self._color

    def get_next_marble(self):
        """Function to get the next value of the Node object"""
        return self._next

    def get_marble_above(self):
        return self._above

    def get_marble_below(self):
        return self._below

    def get_marble_row(self):
        return self._row

    def get_marble_column(self):
        return self._column


class MarblesLinked:
    def __init__(self , row):
        """Function that initializes the data member of the linked list - the head (first Node) of the list"""
        self._head = None
        self._node = None
        self._row = row
        self._game_board = Board()
        self._nodes_list = []


    def add_node_to_list(self , color , row , column):
        self._nodes_list.append(MarbleNode(color, row, column))


    def get_node_by_pos(self , row, column):
        for node in self._nodes_list:
            if node.get_row() == row:
                if node.get_column() == column:
                    return node
        print("Node not found")


    def add(self , color , row , column):
        """
        Adds a node containing val to the linked list
        """
        self._row = row
        self._node = MarbleNode(color, row, column)

        if self._head is None:
            self._head = self._node
        else:
            current = self._head
            while current.get_next_marble() is not None:
                current = current.get_next_marble()
            current._next = self._node

        self.add_node_to_list(color , row , column)

    def set_above_below(self):
        above = None
        below = None
        current = self._head

        for column in range(6):
            for row in range(6):
                if 0 < row < 6:
                    below = self._node.get_node_by_pos(row + 1 , column)
                    above = self._node.get_node_by_pos(row - 1 , column)
                elif row == 0:
                    above = None
                elif row == 6:
                    below = None
                current._above = above
                current._below = below
                current = current._next

        for node in self._node.get_nodes_list():
            for index in range(7):
                if node.get_below() ==

            while current.get_marble_below() is not None:
                current = current.get_marble_below()
            if self._row == 6:
                current._below = None
            else:
                below = game_board[row - 1][column]
                current._below = below

            while current.get_marble_above() is not None:
                current = current.get_marble_above()
            if self._row == 0:
                current._above = None
            current._above =

    def display(self):
        """
        Prints out the values in the linked list
        """
        current = self._head
        while current is not None:
            print(current.get_marble_color() , end=" ")
            current = current._next


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


# ---------------------------------------- Tests ------------------------------------- #
# FROM CANVAS:
game = KubaGame(('PlayerA' , 'W') , ('PlayerB' , 'B'))
print(game.get_marble_count())  # returns (8,8,13)
print(game.get_captured('PlayerA'))  # returns 0
print(game.get_current_turn())  # returns 'PlayerB' because PlayerA has just played.
print(game.get_winner())  # returns None
game.make_move('PlayerA' , (6 , 5) , 'F')
# game.make_move('PlayerA', (6,5), 'L') #Cannot make this move
# game.get_marble((5,5)) #returns 'W'
print(game._game_board.display_linked_row(1))

# CAROLINE'S TESTS:
# game = KubaGame(("Randy" , "W") , ("John" , "B"))
# print(game.get_marble((0 , 2)))
