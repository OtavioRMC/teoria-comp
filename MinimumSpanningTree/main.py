from MinimumSpanningTree.graph import Graph

g = Graph(7)
g.add_vertex_data(0, 'A')
g.add_vertex_data(1, 'B')
g.add_vertex_data(2, 'C')
g.add_vertex_data(3, 'D')
g.add_vertex_data(4, 'E')
g.add_vertex_data(5, 'F')
g.add_vertex_data(6, 'G')

g.add_edge(0, 1, 4)  #A-B,  4
g.add_edge(0, 6, 10) #A-G, 10
g.add_edge(0, 2, 9)  #A-C,  9
g.add_edge(1, 2, 8)  #B-C,  8
g.add_edge(2, 3, 5)  #C-D,  5
g.add_edge(2, 4, 2)  #C-E,  2
g.add_edge(2, 6, 7)  #C-G,  7
g.add_edge(3, 4, 3)  #D-E,  3
g.add_edge(3, 5, 7)  #D-F,  7
g.add_edge(4, 6, 6)  #E-G,  6
g.add_edge(5, 6, 11) #F-G, 11

print("Algoritmo de Kruskal: ")
g.kruskal()

print("Algoritmo de Prim: ")
g.prim()