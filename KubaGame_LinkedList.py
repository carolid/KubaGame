class KubaGame:
    def __init__(self , player1_tuple , player2_tuple):
        self._current_turn = None
        self._winner = None
        self._game_board = Board()
        self._player1 = Player(player1_tuple)
        self._player2 = Player(player2_tuple)
        self._marbles_count = Marbles()
        self._marble = MarbleNode
        self._marbles_linked_list = MarblesLinked()
        self._player_list = [self._player1 , self._player2]

    def get_current_turn(self):
        return self._current_turn

    def make_move(self , playername , coordinates , direction):
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        marble_mover = self._marbles_linked_list.get_node_by_pos(row_coordinate, column_coordinate)
        current = marble_mover
        previous = None

        if playername == self._player1.get_name():
            current_player = self._player1
        elif playername != self._player2.get_name():
            current_player = self._player2
        else:
            print("Player name incorrect or not found.")
            return False

        is_valid_turn = self.is_valid_turn(current_player, marble_mover, row_coordinate, column_coordinate)

        if is_valid_turn:
            if direction == "L":
                is_valid_move = self.is_valid_left_move(marble_mover , current , previous)
                if is_valid_move:
                    return self._game_board.move_marble_left(current_player, column_coordinate, row_coordinate)

            elif direction == "R":
                is_valid_move = self.is_valid_right_move(marble_mover , current , previous)
                if is_valid_move:
                    return self._game_board.move_marble_right(current_player, column_coordinate, row_coordinate)

            elif direction == "F":
                is_valid_move = self.is_valid_forward_move(marble_mover , current , previous)
                if is_valid_move:
                    return self._game_board.move_marble_forward(current_player, column_coordinate, row_coordinate)

            elif direction == "B":
                is_valid_move = self.is_valid_backward_move(marble_mover , current , previous)
                if is_valid_move:
                    return self._game_board.move_marble_backward(current_player, column_coordinate, row_coordinate)

            return False

    def is_valid_turn(self, current_player, marble_mover, row_coordinate, column_coordinate):
        if self._current_turn is None:
            self._current_turn = current_player.get_name()
            self.initialize_board()
        elif self._current_turn != current_player.get_name():
            return False

        marble_color = marble_mover.get_marble_color()

        if 0 <= row_coordinate <= 6:
            if 0 <= column_coordinate <= 6:
                if current_player.get_color() == marble_color:
                    if self._winner is None:
                        return True
                    return False
                return False
            return False
        return False

    def is_valid_left_move(self , marble_mover , current , previous):
        if marble_mover.get_previous_marble() is None or \
                marble_mover.get_next_marble() != "X" or \
                marble_mover.get_next_marble() is not None:
            return False
        while current != "X" or None:
            previous = current
            current = current.get_previous_marble()
        if current is None:
            if previous.get_marble_color() == marble_mover:
                return False
            return True
        return True

    def is_valid_right_move(self , marble_mover , current , previous):
        if marble_mover.get_next_marble() is None or \
                marble_mover.get_previous_marble() != "X" or \
                marble_mover.get_previous_marble() is not None:
            return False
        while current != "X" or None:
            previous = current
            current = current.get_next_marble()
        if current is None:
            if previous.get_marble_color() == marble_mover:
                return False
            return True
        return True

    def is_valid_forward_move(self , marble_mover , current , previous):
        if marble_mover.get_marble_above() is None or \
                marble_mover.get_below_marble() != "X" or \
                marble_mover.get_below_marble() is not None:
            return False
        while current != "X" or None:
            previous = current
            current = current.get_marble_above()
        if current is None:
            if previous.get_marble_color() == marble_mover:
                return False
            return True
        return True

    def is_valid_backward_move(self , marble_mover , current , previous):
        if marble_mover.get_below_marble() is None or \
                marble_mover.get_marble_above() != "X" or \
                marble_mover.get_marble_above() is not None:
            return False
        while current != "X" or None:
            previous = current
            current = current.get_marble_below()
        if current is None:
            if previous.get_marble_color() == marble_mover:
                return False
            return True
        return True

    def evaluate_for_capture(self):

    def evaluate_for_win(self):



    def initialize_board(self):
        current_board = self._game_board.get_current_game_board()

        for row in range(0 , len(current_board)):
            marbles_linked = self._marbles_linked_list
            for column in range(0 , len(current_board[row])):
                color = current_board[row][column]
                marbles_linked.add(color , row , column)
            self._game_board.add_linked_row(marbles_linked)
            self._marbles_linked_list.set_above_below_previous()

    def get_winner(self):
        return self._winner

    def get_captured(self , playername , captures=None):
        if self._player1.get_name() == playername:
            captures = self._player1.get_captures()
        elif self._player2.get_name() == playername:
            captures = self._player2.get_captures()
        return captures

    def get_marble(self , coordinates):
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        node = self._marbles_linked_list.get_node_by_pos(row_coordinate, column_coordinate)
        return node.get_marble_color()

    def get_marble_count(self):
        return self._marbles_count.total_marbles()


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

    def move_marble_right(self, player , row_coordinate, column_coordinate):
        pass

    def move_marble_left (self , player , row_coordinate, column_coordinate):
        pass

    def move_marble_forward(self , player , row_coordinate, column_coordinate):
        pass

    def move_marble_backward(self , player , row_coordinate, column_coordinate):
        pass


class MarbleNode:
    def __init__(self , color , row , column):
        self._color = color
        self._next = None
        self._previous = None
        self._below = None
        self._above = None
        self._row = row
        self._column = column

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


class MarblesLinked:
    def __init__(self):
        """Function that initializes the data member of the linked list - the head (first Node) of the list"""
        self._head = None
        self._node = None
        self._row = None
        self._game_board = Board()
        self._nodes_list = []

    def set_head(self , node):
        """Function that sets the head of the linked list to a Node containing the value specified"""
        self._head = node

    def get_head(self):
        """Function that returns the Node object at the head of the linked list"""
        return self._head

    def get_linked_row(self , row):
        rows = self._game_board.get_linked_rows()
        return rows[row]

    def add_node_to_list(self , node):
        self._nodes_list.append(node)

    def get_node_by_pos(self , row , column):
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
            current = self._node.get_node_by_pos(0 , column)
            for row in range(7):
                if 1 < row < 5:
                    below = self.get_node_by_pos(row + 1 , column)
                    above = self.get_node_by_pos(row - 1 , column)
                elif row == 0:
                    above = None
                elif row == 6:
                    below = None

                if column >= 1:
                    previous = self.get_node_by_pos(row, column - 1)
                elif column == 0:
                    previous = None

                current._above = above
                current._below = below
                current._previous = previous
                current = current.get_marble_below()

    def display(self):
        """
        Prints out the values in the linked list
        """
        current = self._head
        while current is not None:
            print(current.get_marble_color() , end=" ")
            current = current._next

    def move_marble(self , player , marble_mover, row_coordinate, column_coordinate , direction):
            """
            Inserts a node containing val into the linked list at position pos
            """
            current = marble_mover
            start = current
            temp = current._next
            stored = None
            captured = None
            linked_row = self.get_linked_row(row_coordinate)


            if direction == "L":

                if column_coordinate == 1:
                    temp = linked_row._head()
                    linked_row._head = marble_mover
                    self.add_node_to_list(MarbleNode("X", row_coordinate, column_coordinate))
                    captured = temp
                else:
                    while current.get_marble_color() != "X" or current is not None:
                        temp = current._previous
                        current._below = current._below._previous
                        current._above = current._above._previous
                        current._previous = current
                        current = temp
                    if current is None:
                        captured = stored
                    elif current.get_marble_color() == "X":
                        while current.get_marble_color() == "X":
                            current = current._next

                    if temp is None:
                        self.add_node_to_list(MarbleNode("X", row_coordinate, column_coordinate))
                    else:
                        start = temp

            elif direction == "R":


            elif direction == "F":

            elif direction == "B":


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
