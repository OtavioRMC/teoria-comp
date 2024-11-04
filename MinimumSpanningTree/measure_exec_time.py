import timeit
import random
import copy
from graph import Graph

def generate_custom_graph(num_nodes, num_edges):
    graph = Graph(num_nodes)
    edges_added = 0
    
    while edges_added < num_edges:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v:
            weight = random.randint(1, 100)
            graph.add_edge(u, v, weight)
            graph.add_vertex_data(u, str(u))  # Add vertex labels
            graph.add_vertex_data(v, str(v))
            edges_added += 1
    return graph

class MeasureTime(Graph):
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
                mst.append((start_vertex, end_vertex, weight))
                self.union(parent, rank, x, y)
        
        total_weight = sum(weight for _, _, weight in mst)
        return total_weight  
    
    def prim(self):
        adj_list = [[] for _ in range(self.vertex_quantity)]
        for start, end, weight in self.edges_list:
            adj_list[start].append((end, weight))
            adj_list[end].append((start, weight))
            
        in_mst = [False] * self.vertex_quantity
        key_values = [float('inf')] * self.vertex_quantity
        parents = [-1] * self.vertex_quantity
        
        key_values[0] = 0
        
        for _ in range(self.vertex_quantity):
            u = min((v for v in range(self.vertex_quantity) if not in_mst[v]), 
                   key=lambda v: key_values[v])
            
            in_mst[u] = True
            
            for v, weight in adj_list[u]:
                if not in_mst[v] and weight < key_values[v]:
                    key_values[v] = weight
                    parents[v] = u
        
        total_weight = sum(weight for weight in key_values if weight != float('inf'))
        return total_weight  

def measure_execution_time(graph, algorithm):
    graph_copy = copy.deepcopy(graph)
    
    if not isinstance(graph_copy, MeasureTime):
        modified_graph = MeasureTime(graph_copy.vertex_quantity)
        modified_graph.edges_list = graph_copy.edges_list
        modified_graph.vertex_data = graph_copy.vertex_data
        graph_copy = modified_graph
    
    start_time = timeit.default_timer()
    if algorithm == "kruskal":
        total_weight = graph_copy.kruskal()
    else:  # prim
        total_weight = graph_copy.prim()
    elapsed_time = timeit.default_timer() - start_time
    
    return elapsed_time, total_weight

def run_performance_analysis():
    scenarios = [
        (10, 14),
        (100, 140),
        (1000, 1400),
        (10000, 14000)
    ]
    
    results = {}
    for num_nodes, num_edges in scenarios:
        print(f"\nGerando grafo com {num_nodes} vertices e {num_edges} arestas...")
        G = generate_custom_graph(num_nodes, num_edges)
            
        time_kruskal, weight_kruskal = measure_execution_time(G, 'kruskal')
        
        time_prim, weight_prim = measure_execution_time(G, 'prim')
        
        results[(num_nodes, num_edges)] = {
            "Kruskal": {"Time": time_kruskal, "Weight": weight_kruskal},
            "Prim": {"Time": time_prim, "Weight": weight_prim}
        }
        
        
        print(f"\nResultados para o grafo com {num_nodes} vertices e {num_edges} arestas:")
        print(f"Algoritmo de Kruskal:")
        print(f"  - Tempo de Execução: {time_kruskal:.6f} segundos")
        print(f"  - Peso total da AGPM: {weight_kruskal}")
        print(f"Algoritmo de Prim:")
        print(f"  - Tempo de Execução: {time_prim:.6f} seconds")
        print(f"  - Peso total da AGPM: {weight_prim}")
    
    return results

if __name__ == "__main__":
    results = run_performance_analysis()