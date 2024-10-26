import heapq

# Heurística
def heuristic(board, position, usr_mark, oponent_mark):
    score = 0
    win_paths = [
        [(position[0], 0), (position[0], 1), (position[0], 2)],  # Todas las filas
        [(0, position[1]), (1, position[1]), (2, position[1])]   # Todas las columnas
    ]

    # Añadir las diagonales si aplica
    if position in [(0, 0), (1, 1), (2, 2)]:
        win_paths.append([(0, 0), (1, 1), (2, 2)])  # Diagonal principal
    if position in [(0, 2), (1, 1), (2, 0)]:
        win_paths.append([(0, 2), (1, 1), (2, 0)])  # Diagonal secundaria

    # Evaluar cada camino de victoria
    for path in win_paths:
        path_symbols = [board[row][col] for row, col in path]
        if path_symbols.count(oponent_mark) == 2 and usr_mark not in path_symbols:
            score += 1000  # 2 símbolos del oponente juntos
        elif path_symbols.count(usr_mark) == 2 and oponent_mark not in path_symbols:
            score += 100  # 2 símbolos del usuario juntos
        elif path_symbols.count(usr_mark) == 1 and path_symbols.count(oponent_mark) == 0:
            score += 10  # 1 símbolo del usuario
        elif path_symbols.count(oponent_mark) == 1 and path_symbols.count(usr_mark) == 0:
            score += 1  # 1 símbolo del oponente
    return score


# Función GBFS
def GBFS(graph, board, visited, usr_mark, oponent_mark):
    priority_queue = []

    for node in graph:
        if node not in visited:
            score = heuristic(board, node, usr_mark, oponent_mark)
            heapq.heappush(priority_queue, (-score, node))  # Prioridad por el puntaje más alto

    if sum([_[0] for _ in priority_queue]) == 0 and len(visited) == 0:
        visited.add((1,1))
        return (1, 1)

    while priority_queue:
        # Desencolar el nodo con el puntaje más alto
        current_score, current_node = heapq.heappop(priority_queue)
        position = current_node
        
        #print(position, visited)
        if position not in visited:
            visited.add(position)
            return position
    return None