from typing import Iterable, Optional, Set, Tuple

class Graph:
    def __init__(self, directed:bool=False):
        
        self._outgoing : dict= {}
        self._incoming : dict = {} if directed else self._outgoing


    class Vertex:
        __slots__ = '_element'

        def __init__(self, element: str):
            """
            This function should not be called directly, to inserter a vertex call insert_vertex(x)
            """
            self._element : str = element
            
        @property
        def element(self) -> str:
            return self._element
        
        def __hash__(self):
            return hash(id(self))
        
        def __repr__(self):
            return repr(str(self._element))
    
    class Edge:
        """
        Class representing an edge in the graph.
        """
        __slots__ = '_origin', '_destination',  '_element'
        
        def __init__(self, u_vertex: 'Graph.Vertex', v_vertex: 'Graph.Vertex', element: dict):
            """
            Initializes an edge object.

            Args:
                u_vertex (Graph.Vertex): Origin vertex.
                v_vertex (Graph.Vertex): Destination vertex.
                element (dict): Element associated with the edge.
            """
            self._origin: 'Graph.Vertex' = u_vertex  # Origin vertex
            self._destination: 'Graph.Vertex' = v_vertex  # Destination vertex
            self._element: dict = element  # Element associated with the edge
            
        @property
        def element(self):
            return self._element

        def endpoints(self):
            return (self._origin, self._destination)
                
        def opposite(self, v):
            return self._destination if v is self._origin else self._origin
                    
        def __hash__(self):
            return hash( (self._origin, self._destination))
                
        def __repr__(self):
            return repr(str(f"{self._origin}, {self._destination}, {self.element}"))


    

    def is_directed(self) -> bool:
        return self._incoming is not self._outgoing
    
    def vertices(self) -> Iterable:
        return self._outgoing.keys()
    
    def vertex_count(self) -> int:
        return len(self._outgoing)

    def get_edge(self, u: 'Graph.Vertex', v: 'Graph.Vertex') -> Optional['Edge']:
        return self._outgoing[u].get(v)
    
    def degree(self, v: 'Graph.Vertex', outgoing: bool = True) -> int:
        """
        Returns the degree of the vertex v.

        Args:
            v (Graph.Vertex): Vertex.
            outgoing (bool): Flag indicating whether to consider outgoing edges.

        Returns:
            int: Degree of the vertex v.
        """
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v: 'Graph.Vertex', outgoing: bool = True) -> Iterable['Edge']:
        """
        Yields the incident edges to vertex v.

        Args:
            v (Graph.Vertex): Vertex.
            outgoing (bool): Flag indicating whether to consider outgoing edges.

        Yields:
            Edge: Incident edges to vertex v.
        """
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge
    

    def edges(self) -> Set['Edge']:
        """
        Returns all the edges in the graph.

        Returns:
            Set['Edge']: Set of all the edges in the graph.
        """
        result = set()  # avoid double-reporting edges of undirected graph
        
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        
        return result


    def insert_vertex(self, x=None) -> 'Graph.Vertex':
        """
        Inserts a vertex into the graph.

        Args:
            x: Element associated with the vertex.

        Returns:
            Graph.Vertex: Vertex object inserted into the graph.
        """
        v: 'Graph.Vertex' = self.Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v
    
    def insert_edge(self, u_key: str, v_key: str, x: dict = None) -> None:
        """
        Inserts an edge between vertices u and v into the graph.

        Args:
            u_element (Any): Element associated with the origin vertex.
            v_element (Any): Element associated with the destination vertex.
            x (Any): Extra information associated with the edge. Default is None.
        """
        u_vertex: 'Graph.Vertex' = None
        v_vertex: 'Graph.Vertex' = None
        
        # print('Verices: ', end=" ")
        for vertex in self.vertices():
            # print(vertex, end=' ')
            if vertex.element == u_key:
                u_vertex = vertex
            elif vertex.element == v_key:
                v_vertex = vertex
    
        # print()
        if u_vertex is None or v_vertex is None:
            print(u_vertex, v_vertex)
            raise ValueError("One or both vertices not found.")
    
        e = self.Edge(u_vertex, v_vertex, x)
        self._outgoing[u_vertex][v_vertex] = e
        self._incoming[v_vertex][u_vertex] = e

    def bfs(self, source: 'Graph.Vertex', destination: 'Graph.Vertex') -> tuple[Optional[int], list['Graph.Vertex']]:
        # Initialize distances with infinity for all vertices except the source
        distances: dict = {vertex: float('inf') for vertex in self.vertices()}
        distances[source] = 0

        # Initialize visited status for all vertices
        visited: dict = {vertex: False for vertex in self.vertices()}
        visited[source] = True

        # Initialize queue with source vertex
        queue = [(source, [])]

        while queue:
            current_vertex, path = queue.pop(0)

            # If we have reached the destination vertex, return the distance and shortest path
            if current_vertex == destination:
                return distances[current_vertex], path + [current_vertex]

            # Check neighbors and update visited status and distances
            for edge in self.incident_edges(current_vertex):
                neighbor = edge.opposite(current_vertex)
                if not visited[neighbor]:
                    visited[neighbor] = True
                    distances[neighbor] = distances[current_vertex] + 1
                    queue.append((neighbor, path + [current_vertex]))

        # If destination is not reachable, return None
        return None, []

            
if __name__ == '__main__':
    vertices = ['A', 'B', 'C', 'D', 'E']
    gr = Graph(directed=True)
    # edges = [['A', 'B'], ['B', 'C'], ['C', 'A']]
    # edges = [['A', 'C', [10, 5]], ['B', 'C', [3, 2]]]
    edges = [['A', 'C', [10, 5]], ['B', 'C', [3, 2]], ['A', 'B', [1, 2,]], ['C', 'E', [1, 2,]] ]

    vertex_objects = {}  # Dictionary to store mapping of vertex element to Vertex object
    
    for v in vertices:
        vertex_object = gr.insert_vertex(v)
        vertex_objects[v] = vertex_object
    

    for edge in edges:
        gr.insert_edge(edge[0], edge[1], edge[2])

        
    # print(gr._outgoing)
    # print(gr._incoming)
    
    c_edges = gr.incident_edges(vertex_objects['C'], outgoing=True)
    # print(c_edges)
    
    source_vertex = vertex_objects['A']
    destination_vertex = vertex_objects['E']
    shortest_path = gr.bfs(source_vertex, destination_vertex)
    print(shortest_path)