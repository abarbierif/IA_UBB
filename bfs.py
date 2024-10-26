# Función BFS
def BFS(graph, visited, queue):

    '''
    graph -> diccionario del grafo
    visited -> set de nodos visitados
    '''

    while queue:
        node = queue.popleft() 
        if node not in visited:
            queue.extend(graph[node])
            return node