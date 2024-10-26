# Función DFS
def DFS(graph, visited, stack):

    '''
    graph -> diccionario del grafo
    visited -> set de nodos visitados
    '''

    while stack:
        node = stack.pop() 
        if node not in visited:
            stack.extend(graph[node])
            return node