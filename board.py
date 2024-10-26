import random
from collections import deque

from bfs import *
from dfs import *
from gbfs import *

class Board:
    def __init__(self, usr_mark='X', oponent_mode='Random'):
        self.idle_char = 'I'
        self.board = [[self.idle_char for j in range(3)] for i in range(3)]
        self.graph = {(0, 0): [(0, 1), (1, 1), (1, 0)],
                      (0, 1): [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)],
                      (0, 2): [(0, 1), (1, 1), (1, 1)],
                      (1, 0): [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)],
                      (1, 1): [(0, 0), (0, 1), (0, 1), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
                      (1, 2): [(0, 2), (0, 1), (1, 1), (2, 1), (2, 2)],
                      (2, 0): [(1, 0), (1, 1), (2, 1)],
                      (2, 1): [(2, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
                      (2, 2): [(2, 1), (1, 1), (1, 2)]}
        self.available_positions = {(i, j) for i in range(3) for j in range(3)}
        self.not_available_positions = set()
        self.usr_mark = usr_mark
        self.oponent_mark = 'O' if usr_mark == 'X' else 'X'

        self.oponent_mode = oponent_mode
        self.start_position = (random.choice(list(self.available_positions)))

        self.stack = [self.start_position]
        #self.stack = [(0,0)]
        self.queue = deque([self.start_position])
        #self.queue = deque([(0,0)])


    # Método para checkear el resultado
    def result_check(self):
        if self.board[0][0] == self.board[0][1] == self.board[0][2] != self.idle_char:
            return True
        elif self.board[1][0] == self.board[1][1] == self.board[1][2] != self.idle_char:
            return True
        elif self.board[2][0] == self.board[2][1] == self.board[2][2] != self.idle_char:
            return True
        elif self.board[0][0] == self.board[1][0] == self.board[2][0] != self.idle_char:
            return True
        elif self.board[0][1] == self.board[1][1] == self.board[2][1] != self.idle_char:
            return True
        elif self.board[0][2] == self.board[1][2] == self.board[2][2] != self.idle_char:
            return True
        elif self.board[0][0] == self.board[1][1] == self.board[2][2] != self.idle_char:
            return True
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] != self.idle_char:
            return True
        else:
            return False

    # Método para manejar el movimiento del usuario
    def user_move(self, position):
        if position in self.available_positions:
            self.board[position[0]][position[1]] = self.usr_mark
            self.available_positions.remove(position)
            self.not_available_positions.add(position)

    # Método para manejar el movimiento del oponente
    def oponent_move(self):
        if self.oponent_mode == 'Random':
            oponent_position = random.choice(list(self.available_positions))
        elif self.oponent_mode == 'DFS':
            oponent_position = DFS(self.graph, self.not_available_positions, self.stack)
            if oponent_position == None:
                self.stack.extend(self.graph[self.start_position])
                oponent_position = DFS(self.graph, self.not_available_positions, self.stack)
        elif self.oponent_mode == 'BFS':
            oponent_position = BFS(self.graph, self.not_available_positions, self.queue)
            if oponent_position == None:
                self.queue.extend(self.graph[self.start_position])
        elif self.oponent_mode == 'GBFS':
            oponent_position = GBFS(self.graph, self.board, self.not_available_positions, self.usr_mark, self.oponent_mark)
            if oponent_position == None:
                self.queue.extend(self.graph[self.start_position])
        
        self.board[oponent_position[0]][oponent_position[1]] = self.oponent_mark
        self.available_positions.remove(oponent_position)
        self.not_available_positions.add(oponent_position)

        return oponent_position