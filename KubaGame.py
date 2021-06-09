class KubaGame:
    def __init__(self , player1_tuple , player2_tuple):
        self._current_turn = None
        self._winner = None
        self._player1 = Player(player1_tuple)
        self._player2 = Player(player2_tuple)
        self._marbles_count = Marbles()
        self._game_board = Board()
        self._marble = MarbleNode
        self._marbles_linked_list = MarblesLinked()
        self._player_list = [self._player1 , self._player2]

    def get_current_turn(self):
        return self._current_turn

    def get_winner(self):
        return self._winner

    def get_captured(self , playername , captures=None):
        if self._player1.get_name() == playername:
            captures = self._player1.get_red_captures()
        elif self._player2.get_name() == playername:
            captures = self._player2.get_red_captures()
        return captures

    def get_marble(self , coordinates):
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        node = self._marbles_linked_list.get_node_by_pos(row_coordinate , column_coordinate)
        return node.get_marble_color()

    def get_marble_count(self):
        return self._marbles_count.total_marbles()

    def make_move(self , playername , coordinates , direction):
        self.initialize_board()

        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        current_player = None
        marble_mover = self._marbles_linked_list.get_node_by_pos(row_coordinate , column_coordinate)
        marble_color = marble_mover.get_marble_color()

        for player in self._player_list:
            if playername == player.get_name():
                current_player = player
        if self._current_turn is None:
            self._current_turn = current_player.get_name()
        elif self._current_turn == current_player.get_name():
            if 0 <= row_coordinate <= 6:
                if 0 <= column_coordinate <= 6:
                    if current_player.get_color() == marble_color:
                        if self._winner is None:
                            return self.is_valid_move(marble_mover , current_player , row_coordinate ,
                                                      column_coordinate , direction)
                        return False
                    return False
                return False
            return False
        return False

    def is_valid_move(self , marble_mover , current_player , row_coordinate , column_coordinate , direction):
        is_valid = False
        color = marble_mover.get_marble_color()
        is_pushed_off = None

        if direction == "L":
            if marble_mover.get_previous_marble() is not None:
                if marble_mover.get_next_marble() == "X" or marble_mover.get_next_marble() is None:
                    is_valid = True

        elif direction == "R":
            if marble_mover.get_next_marble() is not None:
                if marble_mover.get_previous_marble() == "X" or marble_mover.get_previous_marble() is None:
                    is_valid = True

        elif direction == "F":
            if marble_mover.get_marble_above() is not None:
                if marble_mover.get_below_marble() == "X" or marble_mover.get_below_marble() is None:
                    is_valid = True

        elif direction == "B":
            if marble_mover.get_below_marble() is not None:
                if marble_mover.get_marble_above() == "X" or marble_mover.get_marble_above() is None:
                    is_valid = True

        if is_valid:
            self._game_board.move_marble(current_player , row_coordinate , column_coordinate , direction)
            self.evaluate_win(current_player)
            return True
        return False

    def evaluate_win(self , player):
        red_marbles = player.get_red_captures()
        opposite_marbles = player.get_opposite_captures()

        if red_marbles >= 7 or opposite_marbles == 8:
            self._winner = player.get_name()

    def initialize_board(self):
        current_board = self._game_board.get_current_game_board()

        for row in range(0 , len(current_board)):
            marbles_linked = self._marbles_linked_list
            for column in range(0 , len(current_board[row])):
                color = current_board[row][column]
                marbles_linked.add(color , row , column)
            self._game_board.add_linked_row(marbles_linked)
        self._marbles_linked_list.set_above_below_previous()


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
        self._previous_game_board = self._current_game_board
        self._rows_linked_list = []
        self._marbles = Marbles()

    def add_linked_row(self , linked_list):
        self._rows_linked_list.append(linked_list)

    def display_linked_row(self , row):
        row_to_display = self._rows_linked_list[row]
        row_to_display.display()

    def get_linked_rows(self):
        return self._rows_linked_list

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
            next_column = column_coordinate - 1
            start_column = column_coordinate
            count = start_column

            while column_coordinate != 0 and self._current_game_board[row_coordinate][column_coordinate] != "X":
                count -= 1
                column_coordinate -= 1

            if column_coordinate == 0:
                captured = self._current_game_board[row_coordinate][0]
                self._current_game_board[row_coordinate][count:start_column] = self._current_game_board \
                                                                                   [row_coordinate][count + 1:]
                self._current_game_board[row_coordinate].pop(0)

            elif self._current_game_board[row_coordinate][column_coordinate] == "X":
                self._current_game_board[row_coordinate][next_column:count + 1] = self._current_game_board \
                                                                                      [row_coordinate][
                                                                                  start_column:count]

            self._current_game_board[row_coordinate][start_column] = "X"

        elif direction == "R":
            next_column = column_coordinate + 1
            start_column = column_coordinate
            count = start_column

            while column_coordinate != 6 and self._current_game_board[row_coordinate][column_coordinate] != "X":
                count += 1
                column_coordinate += 1

            if column_coordinate == 6:
                captured = self._current_game_board[row_coordinate][6]
                self._current_game_board[row_coordinate][next_column:] = self._current_game_board \
                                                                             [row_coordinate][start_column:count]
                self._current_game_board[row_coordinate].pop(6)

            elif self._current_game_board[row_coordinate][column_coordinate] == "X":
                self._current_game_board[row_coordinate][next_column:count + 1] = self._current_game_board \
                                                                                      [row_coordinate][
                                                                                  start_column:count]

            self._current_game_board[row_coordinate][start_column] = "X"

        elif direction == "F":
            next_row = row_coordinate - 1
            start_row = row_coordinate
            count = start_row

            while row_coordinate != 0 and self._current_game_board[row_coordinate][column_coordinate] != "X":
                count -= 1
                row_coordinate -= 1

            if row_coordinate == 0:
                if self._current_game_board[0][column_coordinate] == color:
                    return False
                elif self._current_game_board[0][column_coordinate] == "R":
                    player.add_red_capture()
                    self._marbles.remove_marble("R")
                elif self._current_game_board[0][column_coordinate] == opposite_color:
                    player.add_opposite_capture()
                    self._marbles.remove_marble(opposite_color)
                self._current_game_board[0][column_coordinate].pop()

                self._current_game_board[next_row:][column_coordinate] = self._current_game_board \
                    [start_row:count + 1][column_coordinate]

            elif self._current_game_board[row_coordinate][column_coordinate] == "X":
                self._current_game_board[next_row:count - 1][column_coordinate] = self._current_game_board \
                    [start_row:count][column_coordinate]
            self._current_game_board[start_row][column_coordinate] = "X"

        elif direction == "B":
            next_row = row_coordinate + 1
            start_row = row_coordinate
            count = start_row

            while row_coordinate != 6 and self._current_game_board[row_coordinate][column_coordinate] != "X":
                count += 1
                row_coordinate += 1

            if row_coordinate == 6:
                if self._current_game_board[6][column_coordinate] == color:
                    return False
                elif self._current_game_board[6][column_coordinate] == "R":
                    player.add_red_capture()
                    self._marbles.remove_marble("R")
                elif self._current_game_board[6][column_coordinate] == opposite_color:
                    player.add_opposite_capture()
                    self._marbles.remove_marble(opposite_color)
                self._current_game_board[6][column_coordinate].pop()

                self._current_game_board[next_row:][column_coordinate] = self._current_game_board \
                    [start_row:count][column_coordinate]

            elif self._current_game_board[row_coordinate][column_coordinate] == "X":
                self._current_game_board[next_row:count + 1][column_coordinate] = self._current_game_board \
                    [start_row:count][column_coordinate]
            self._current_game_board[start_row][column_coordinate] = "X"

        if captured is not None:
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


class MarbleNode:
    def __init__(self , color , row , column):
        self._color = color
        self._row = row
        self._column = column
        self._next = None
        self._previous = None
        self._below = None
        self._above = None

    def set_marble_color(self , color):
        """Function to set the data value of the Node object"""
        self._color = color

    def set_next_marble(self , marble):
        """Function to set the next node of the current Node object"""
        self._next = marble

    def set_marble_above(self , marble):
        self._above = marble

    def set_marble_below(self , marble):
        self._below = marble

    def set_previous_marble(self , marble):
        self._previous = marble

    def set_marble_row(self , row):
        self._row = row

    def set_marble_column(self , column):
        self._column = column

    def get_marble_color(self):
        """Function to get the data value of the Node object"""
        return self._color

    def get_next_marble(self):
        """Function to get the next value of the Node object"""
        return self._next

    def get_previous_marble(self):
        return self._previous

    def get_marble_above(self):
        return self._above

    def get_marble_below(self):
        return self._below

    def get_marble_row(self):
        return self._row

    def get_marble_column(self):
        return self._column


class MarblesLinked(Board):
    def __init__(self):
        """Function that initializes the data member of the linked list - the head (first Node) of the list"""
        super().__init__()
        self._head = None
        self._node = None
        self._row = None
        self._nodes_list = []

    def set_head(self , node):
        """Function that sets the head of the linked list to a Node containing the value specified"""
        self._head = node

    def get_head(self):
        """Function that returns the Node object at the head of the linked list"""
        return self._head

    def get_linked_row(self , row):
        rows = self.get_linked_rows()
        return rows[row]

    def add_node_to_list(self , node):
        self._nodes_list.append(node)

    def get_node_by_pos(self , row , column):
        for node in self._nodes_list:
            if node.get_marble_row() == row:
                if node.get_marble_column() == column:
                    return node

    def add(self , color , row , column):
        """
        Adds a node containing val to the linked list
        """
        self._row = row
        self._node = MarbleNode(color , row , column)

        if self._head is None:
            self._head = self._node
            self._head.set_previous_marble(None)
        else:
            current = self._head
            while current.get_next_marble() is not None:
                current = current.get_next_marble()
            current.set_next_marble(self._node)
            current._next.set_previous_marble(current)

        self.add_node_to_list(self._node)

    def set_above_below_previous(self):
        above = None
        below = None
        previous = None

        for column in range(7):
            for row in range(7):
                current = self.get_node_by_pos(column , row)
                print(current)
                print(column)
                print(row)
                if 1 < row < 5:
                    below = self.get_node_by_pos(row + 1 , column)
                    above = self.get_node_by_pos(row - 1 , column)
                elif row == 0:
                    above = None
                elif row == 6:
                    below = None

                if column >= 1:
                    previous = self.get_node_by_pos(row , column - 1)
                elif column == 0:
                    previous = None

                current._above = above
                current._below = below
                current._previous = previous

    def display(self):
        """
        Prints out the values in the linked list
        """
        current = self._head
        while current is not None:
            print(current.get_marble_color() , end=" ")
            current = current._next


# ---------------------------------------- Tests ------------------------------------- #
# # FROM CANVAS:
# game = KubaGame(('PlayerA' , 'W') , ('PlayerB' , 'B'))
# print(game.get_marble_count())  # returns (8,8,13)
# print(game.get_captured('PlayerA'))  # returns 0
# print(game.get_current_turn())  # returns 'PlayerB' because PlayerA has just played.
# print(game.get_winner())  # returns None
# print(game.make_move('PlayerA' , (6 , 5) , 'F'))
# print(game.make_move('PlayerA' , (6 , 5) , 'L'))  # Cannot make this move
# print(game.get_marble((5 , 5)))  # returns 'W'
# print(game._game_board.display_linked_row(1))
#
# # CAROLINE'S TESTS:
# # game = KubaGame(("Randy" , "W") , ("John" , "B"))
# # print(game.get_marble((0 , 2)))
