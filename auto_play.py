import random
from board import Board
import time

def auto_play(oponent_mode, n_games, seed = None):
    """
    Simula n partidas entre un usuario aleatorio y el algoritmo de oponente seleccionado.
    
    :param oponent_mode: Modo del oponente ('Random', 'DFS', 'BFS', 'GBFS', 'RFC', 'XGB', 'GNB', 'SVM')
    :param n_games: Número de partidas a jugar
    """
    user_wins = 0
    oponent_wins = 0
    draws = 0

    if seed is not None:
        random.seed(seed)  # Configurar la semilla para reproducibilidad

    for game in range(n_games):
        # Inicializar un nuevo tablero
        board = Board(usr_mark='X', oponent_mode=oponent_mode)
        finished = False

        while not finished:
            # Turno del usuario (jugada aleatoria)
            if board.available_positions:
                user_position = random.choice(list(board.available_positions))
                board.user_move(user_position)

                # Verificar si el usuario ganó
                if board.result_check():
                    user_wins += 1
                    finished = True
                    break

            # Turno del oponente
            if board.available_positions:
                oponent_position = board.oponent_move()

                # Verificar si el oponente ganó
                if board.result_check():
                    oponent_wins += 1
                    finished = True
                    break

            # Verificar empate
            if not board.available_positions:
                draws += 1
                finished = True
                break

        #print(f"Game {game + 1}/{n_games}:")

    # Resultados finales
    print("\n=== Results ===")
    print(f"Total games: {n_games}")
    print(f"User wins: {user_wins}")
    print(f"Opponent ({oponent_mode}) wins: {oponent_wins}")
    print(f"Draws: {draws}")

# Ejecutar simulación
if __name__ == "__main__":

    opponent_mode = "DFS"  # Cambiar a 'Random', 'DFS', 'BFS', 'GBFS', 'XGB', 'GNB', 'SVM', según el caso
    n_games = 100  # Número de partidas a simular
    seed = 42

    start_time = time.time()
    auto_play(opponent_mode, n_games, seed)
    end_time = time.time()

    print(f"time: {round(end_time - start_time,2)}[s]")
