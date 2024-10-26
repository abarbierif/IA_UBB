from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QLCDNumber
from PyQt5.QtCore import Qt
from PyQt5 import uic

from board import Board

class TicTacToeGui(QMainWindow):
    def __init__(self):
        super(TicTacToeGui, self).__init__()

        uic.loadUi("TicTacToe.ui", self)
        self.board = Board()
        self.markerO_count = 0
        self.markerX_count = 0
        self.current_position = (0, 0)
        self.finished = False

        # widgets (buttons, combo box, etc)
        self.buttons = [self.findChild(QPushButton, f"pushButton_{i}") for i in range(9)]
        self.resetButton = self.findChild(QPushButton, "resetButton")
        self.comboMode = self.findChild(QComboBox, "comboMode")
        self.comboMark = self.findChild(QComboBox, "comboMark")
        self.markerO = self.findChild(QLCDNumber, "markerO")
        self.markerX = self.findChild(QLCDNumber, "markerX")


        # widgets connections
        self.positions = {pos:n for n, pos in enumerate([(i,j) for i in range(3) for j in range(3)])}
        for n, button in enumerate(self.buttons):
            button.clicked.connect(lambda checked, b=button, pos=list(self.positions.keys())[n]: self.clicker(b, pos))
            #button.clicked.connect(lambda checked, b=button, pos=(n // 3, n % 3): self.clicker(b, pos))
        self.resetButton.clicked.connect(self.reset)
        self.comboMode.activated[str].connect(self.change_oponent_mode)
        self.comboMark.activated[str].connect(self.change_user_mark)

        self.highlight_current_position()
        self.show()
        self.setFocus()

    # Función para destacar la posición dentro del tablero
    def highlight_current_position(self):
        for i, button in enumerate(self.buttons):
            button.setStyleSheet("")
        index = self.current_position[0] * 3 + self.current_position[1]
        self.buttons[index].setStyleSheet("background-color: gray;")

    # Función para manejar los eventos que ocurren al presionar una tecla
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.finished == False:
                button = self.buttons[self.positions[self.current_position]]
                if self.current_position in self.board.available_positions:
                    self.clicker(button, self.current_position)
        elif event.key() == Qt.Key_Up:
            if self.current_position[0] == 0:
                self.current_position = (self.current_position[0] + 2, self.current_position[1])
            else:
                self.current_position = (self.current_position[0] - 1, self.current_position[1])
        elif event.key() == Qt.Key_Down:
            if self.current_position[0] == 2:
                self.current_position = (self.current_position[0] - 2, self.current_position[1])
            else:
                self.current_position = (self.current_position[0] + 1, self.current_position[1])
        elif event.key() == Qt.Key_Left:
            if self.current_position[1] == 0:
                self.current_position = (self.current_position[0], self.current_position[1] + 2)
            else:
                self.current_position = (self.current_position[0], self.current_position[1] - 1)
        elif event.key() == Qt.Key_Right:
            if self.current_position[1] == 2:
                self.current_position = (self.current_position[0], self.current_position[1] - 2)
            else:
                self.current_position = (self.current_position[0], self.current_position[1] + 1)
        elif event.key() == Qt.Key_Z:
            if self.finished == False:
                random_position = random.choice(list(self.board.available_positions))
                button = self.buttons[self.positions[random_position]]
                self.clicker(button, random_position)
        
        self.highlight_current_position()


    # Función para
    def change_user_mark(self, mark):
        self.setFocus()
        self.board.usr_mark = mark
        self.board.oponent_mark = 'O' if self.board.usr_mark == 'X' else 'X'
        self.comboMark.setEnabled(False)
        self.comboMode.setEnabled(False)
        if self.board.usr_mark == 'O':
            # oponent move
            oponent_position = self.board.oponent_move()
            self.buttons[self.positions[oponent_position]].setText(self.board.oponent_mark)
            self.buttons[self.positions[oponent_position]].setEnabled(False)
    
    # Función para cambiar el algoritmo del oponente
    def change_oponent_mode(self, mode):
        self.setFocus()
        self.board.oponent_mode = mode
        #self.comboMode.setEnabled(False)

    # Función para poder hacer click en el tablero
    def clicker(self, button, position):
        self.comboMode.setEnabled(False)
        self.comboMark.setEnabled(False)
        self.current_position = position
        self.highlight_current_position()
        self.setFocus()

        # user move
        self.board.user_move(position)
        button.setText(self.board.usr_mark)
        button.setEnabled(False)

        # check result
        if self.board.result_check():
            self.show_winner("user")
            self.disable_buttons()
            return
        elif len(self.board.available_positions) == 0:
            self.show_winner("no one")
            self.disable_buttons()


        # oponent move
        if self.board.available_positions:
            oponent_position = self.board.oponent_move()
            self.buttons[self.positions[oponent_position]].setText(self.board.oponent_mark)
            self.buttons[self.positions[oponent_position]].setEnabled(False)
            #self.buttons[oponent_position[0] * 3 + oponent_position[1]].setText(self.board.oponent_mark)
            #self.buttons[oponent_position[0] * 3 + oponent_position[1]].setEnabled(False)

            # check result
            if self.board.result_check():
                self.show_winner("oponent")
                self.disable_buttons()
                return
            elif len(self.board.available_positions) == 0:
                self.show_winner("no one")
                self.disable_buttons()


    # Función para mostrar el resultado
    def show_winner(self, winner):
        msg = QMessageBox()
        msg.setWindowTitle("")
        if winner == 'user':
            msg.setText("you won!")
            if self.board.usr_mark == 'X':
                self.markerX_count += 1
            elif self.board.usr_mark == 'O':
                self.markerO_count += 1
        elif winner == 'oponent':
            msg.setText("you lost!")
            if self.board.usr_mark == 'X':
                self.markerO_count += 1
            elif self.board.usr_mark == 'O':
                self.markerX_count += 1
        elif winner == 'no one':
            msg.setText("draw!")

        self.markerO.display(self.markerO_count)
        self.markerX.display(self.markerX_count)

        self.finished = True

        msg.exec_()

    # Función para deshabilitar los botones (tablero)
    def disable_buttons(self):
        for button in self.buttons:
            button.setEnabled(False)

    # Función para resetear el tablero
    def reset(self):
        current_oponent_mode = self.board.oponent_mode
        self.board = Board(usr_mark='X', oponent_mode=current_oponent_mode)
        self.comboMark.setCurrentText('X')
        self.current_position = (0, 0)
        self.highlight_current_position()

        for button in self.buttons:
            button.setText("")
            button.setEnabled(True)

        self.comboMode.setEnabled(True)
        self.comboMark.setEnabled(True)
        self.finished = False
        self.setFocus()