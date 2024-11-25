import random
from collections import deque
import joblib
import sklearn

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

        #ML algorithms
        self.predicted_positions = {
            '0': (0, 0),
            '1': (0, 1),
            '2': (0, 2),
            '3': (1, 0),
            '4': (1, 1),
            '5': (1, 2),
            '6': (2, 0),
            '7': (2, 1),
            '8': (2, 2)
        }

        self.current_state_board = {
            (0,0): '0', 
            (0,1): '1', 
            (0,2): '2', 
            (1,0): '3', 
            (1,1): '4', 
            (1,2): '5', 
            (2,0): '6', 
            (2,1): '7', 
            (2,2): '8'
        }

        # load LabelEconder
        self.le = joblib.load("label_encoders.pkl")

        # Random Forest Classifer
        self.rfc = joblib.load("rfc.pkl")

        # XGBoost Classifier
        self.xgb = joblib.load("xgboost.pkl")

        # Gaussian Naive Bayes
        self.gnb = joblib.load("gnb.pkl")

        # Support Vector Machine
        self.svm = joblib.load("svm.pkl")

    def board_encoding(self, board_current_state):
        board_encoded = []
        for i, item in enumerate(board_current_state):
            col_name = f'point_{i + 1}'
            if col_name in self.le:
                encoded_item = self.le[col_name].transform([str(item)])[0]
                board_encoded.append(encoded_item)

        return board_encoded

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
            self.current_state_board[position] = 'h'

    # Método para manejar el movimiento del oponente
    def oponent_move(self):
        if self.oponent_mode == 'Random':
            oponent_position = random.choice(list(self.available_positions))
        elif self.oponent_mode == 'DFS':
            oponent_position = DFS(self.graph, self.not_available_positions, self.stack)
            if oponent_position is None:
                self.stack.extend(self.graph[self.start_position])
                #oponent_position = DFS(self.graph, self.not_available_positions, self.stack)
                oponent_position = random.choice(list(self.available_positions))
        elif self.oponent_mode == 'BFS':
            oponent_position = BFS(self.graph, self.not_available_positions, self.queue)
            if oponent_position is None:
                self.queue.extend(self.graph[self.start_position])
                #oponent_position = BFS(self.graph, self.not_available_positions, self.stack)
                oponent_position = random.choice(list(self.available_positions))
        elif self.oponent_mode == 'GBFS':
            oponent_position = GBFS(self.graph, self.board, self.not_available_positions, self.usr_mark, self.oponent_mark)
            if oponent_position == None:
                self.queue.extend(self.graph[self.start_position])
        elif self.oponent_mode == 'RFC':
            encoded_current_board_state = self.board_encoding(list(self.current_state_board.values()))
            oponent_position = self.predicted_positions[str(self.rfc.predict([encoded_current_board_state])[0])]
        elif self.oponent_mode == 'XGB':
            encoded_current_board_state = self.board_encoding(list(self.current_state_board.values()))
            oponent_position = self.predicted_positions[str(self.xgb.predict([encoded_current_board_state])[0])]
        elif self.oponent_mode == 'GNB':
            encoded_current_board_state = self.board_encoding(list(self.current_state_board.values()))
            oponent_position = self.predicted_positions[str(self.gnb.predict([encoded_current_board_state])[0])]
        elif self.oponent_mode == 'SVM':
            encoded_current_board_state = self.board_encoding(list(self.current_state_board.values()))
            oponent_position = self.predicted_positions[str(self.svm.predict([encoded_current_board_state])[0])]


        self.board[oponent_position[0]][oponent_position[1]] = self.oponent_mark
        self.available_positions.remove(oponent_position)
        self.not_available_positions.add(oponent_position)
        self.current_state_board[oponent_position] = 'c'

        return oponent_position