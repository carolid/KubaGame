# Author: Caroline Davis
# Date: 05/28/2021
# Description: ...


class KubaGame:
    def __init__(self , player1_tuple , player2_tuple):
        self._player1_name = player1_tuple[0]
        self._player2_name = player2_tuple[0]
        self._player1_color = player1_tuple[1]
        self._player2_color = player2_tuple[1]
        self._current_turn = None
        self._winner = None
        self._player1_captured = 0
        self._player2_captured = 0
        self._game_board = [['W' , 'W' , 'X' , 'X' , 'X' , 'B' , 'B'] ,
                            ['W' , 'W' , 'X' , 'R' , 'X' , 'B' , 'B'] ,
                            ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                            ['X' , 'R' , 'R' , 'R' , 'R' , 'R' , 'X'] ,
                            ['X' , 'X' , 'R' , 'R' , 'R' , 'X' , 'X'] ,
                            ['B' , 'B' , 'X' , 'R' , 'X' , 'W' , 'W'] ,
                            ['B' , 'B' , 'X' , 'X' , 'X' , 'W' , 'W']
                            ]

    def get_current_turn(self):
        return self._current_turn

    def make_move(self, playername, coordinates, direction):
        row_coordinate = coordinates[0]
        column_coordinate = coordinates[1]
        if playername == self._player1_name:
            color = self._player1_color
        else:
            color = self._player2_color

    def get_winner(self):
        return self._winner

    def get_captured(self, playername):
        if playername == self._player1_name:
            return self._player1_captured
        else:
            return self._player2_captured

    def get_marble(self, *coordinates):
        coordinates_list = []
        for i in range(0, len(coordinates)):
            coordinates_list.append(coordinates[i])
        row_coordinate = coordinates_list[0]
        column_coordinate = coordinates_list[1]
        return self._game_board[row_coordinate][column_coordinate]



game = KubaGame
game.get_marble((0, 2))
