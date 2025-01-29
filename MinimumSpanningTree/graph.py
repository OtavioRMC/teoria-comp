""" Árvore Geradora de Peso Mínimo

A Aŕvore geradora de peso mínimo , também conhecida como Minimim Spanning Tree (MST)
é  o conjunto de arestas necessárias para conectar todos os vértices de um gráfo não
direcionado, com o peso mínimo das arestas.

É chamada de Minimum Spanning Tree porque é um gráfo, conectado , não direcionado e 
acíclico, o que é a própia definição de árvore.

O Algoritmo de Kruskal adiciona arestas à árvore , começando com as arestas
de menor peso. Arestas que forma ciclos não são adicionadas à árvore.

Para verificar se um as arestas formam ciclos, o algoritmo "Union-find cycle detection"
é utilizado dentro do algoritmo de Kruskal.

Funcionamento do Algoritmo:
  - 1. Ordenar as arestas do grafo em ordem crescente de pesos.
  - 2. Para cada aresta, começando com a que possui menor peso:
    - 2.1. Essa aresta vai criar um ciclo dentro da MST ?
      2.2. Se não , adcione a aresta como uma aresta da MST.
"""

class Graph():
  """
  Classe que representa a estrutura de dados grafo utilizando a lista de adjacência.

  Atributos:
    vertex_quantity (int): Número de vértices no grafo.
    edges_list : Lista de arestas na forma (vértice_inico,vértice_fim,peso).
    vertex_data: (List[str]): Dado associado com cada vértice.
  """
  def __init__(self,vertex_quantity:int) -> None:
    self.vertex_quantity = vertex_quantity
    self.edges_list: list = []
    self.vertex_data: list[str] = [''] * vertex_quantity 

  def add_edge(self,start_vertex,end_vertex,weight) -> None:
    if 0 <= start_vertex < self.vertex_quantity and 0 <= end_vertex < self.vertex_quantity:
      self.edges_list.append((start_vertex,end_vertex,weight))
  
  def add_vertex_data(self,vertex,data):
    if 0 <= vertex < self.vertex_quantity:
      self.vertex_data[vertex] = data
  
  def find(self,parent,i):
    if parent[i] == i:
      return i
    return self.find(parent,parent[i])
  
  def union(self, parent, rank, x, y):
    x_root = self.find(parent,x)
    y_root = self.find(parent,y)
    
    if rank[x_root] < rank[y_root]:
      parent[x_root] = y_root
    
    elif rank[x_root] > rank[y_root]:
      parent[y_root] = x_root
    
    else:
      parent[y_root] = x_root
      rank[x_root] += 1

  def kruskal(self):
    
    mst = []
    edge_count = 0

    self.edges_list = sorted(self.edges_list, key=lambda item: item[2])

    parent, rank = [], []

    for vertex in range(self.vertex_quantity):
      parent.append(vertex)
      rank.append(0)

    while edge_count < len(self.edges_list):
      start_vertex, end_vertex, weight = self.edges_list[edge_count]
      edge_count += 1

      x = self.find(parent, start_vertex)
      y = self.find(parent, end_vertex)

      if x != y:
        mst.append((start_vertex,end_vertex,weight))
        self.union(parent, rank, x, y)

    total_weight = sum(weight for start_vertex,end_vertex, weight in mst)
    print("Arrestas | Pesos")
    for start_vertex, end_vertex, weight in mst:
      print(f"{self.vertex_data[start_vertex]} - {self.vertex_data[end_vertex]} | {weight}")

    print(f"Somatório de pessos da AGPM de Kruskal: {total_weight}")

  def prim(self) -> None:
    # Criação da lista de adjacência para o algoritmo de Prim
    adj_list = [[] for _ in range(self.vertex_quantity)]
    for start, end, weight in self.edges_list:
        adj_list[start].append((end, weight))
        adj_list[end].append((start, weight))

    in_mst = [False] * self.vertex_quantity
    key_values = [float('inf')] * self.vertex_quantity
    parents = [-1] * self.vertex_quantity

    key_values[0] = 0  # Começa com o primeiro vértice

    print("Arestas\tPesos")
    for _ in range(self.vertex_quantity):
        # Escolhe o vértice u com a menor chave que ainda não está na MST
        u = min((v for v in range(self.vertex_quantity) if not in_mst[v]), key=lambda v: key_values[v])
        
        in_mst[u] = True

        if parents[u] != -1:  # Pula o primeiro vértice pois ele não tem pai
            print(f"{self.vertex_data[parents[u]]} - {self.vertex_data[u]} | {key_values[u]}")

        # Atualiza as chaves dos vizinhos de u
        for v, weight in adj_list[u]:
            if not in_mst[v] and weight < key_values[v]:
                key_values[v] = weight
                parents[v] = u

    total_weight = sum(key_values)
    print(f"Somatorio de Pesos da AGPM de Prim: {total_weight}")

  