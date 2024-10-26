from PyQt5.QtWidgets import QMainWindow, QApplication
import sys

from tictactoegui import TicTacToeGui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    TicTacToeWindow = TicTacToeGui()
    app.exec_()