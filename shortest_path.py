import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk, messagebox

class NetworkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rede de Computadores")
        self.G = nx.Graph()
        
        # Criar widgets primeiro
        self.create_widgets()
        
        # Depois configurar o cenário padrão
        self.setup_scenario_1()
        
    def create_widgets(self):
        # Selecção de Cenário
        scenario_frame = ttk.LabelFrame(self.root, text="Seleção de Cenário", padding="5")
        scenario_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        ttk.Button(scenario_frame, text="Cenário 1", 
                  command=self.setup_scenario_1).grid(row=0, column=0, padx=5)
        ttk.Button(scenario_frame, text="Cenário 2", 
                  command=self.setup_scenario_2).grid(row=0, column=1, padx=5)
        
        # Encontrar Caminho
        path_frame = ttk.LabelFrame(self.root, text="Encontrar Caminho", padding="5")
        path_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        ttk.Label(path_frame, text="De:").grid(row=0, column=0, padx=5)
        self.source_var = StringVar()
        self.source_combo = ttk.Combobox(path_frame, textvariable=self.source_var)
        self.source_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(path_frame, text="Para:").grid(row=0, column=2, padx=5)
        self.dest_var = StringVar()
        self.dest_combo = ttk.Combobox(path_frame, textvariable=self.dest_var)
        self.dest_combo.grid(row=0, column=3, padx=5)
        
        ttk.Button(path_frame, text="Encontrar Caminho", 
                  command=self.find_path).grid(row=0, column=4, padx=5)
        
        # Display de Resultado
        self.result_text = Text(self.root, height=5, width=50)
        self.result_text.grid(row=2, column=0, padx=5, pady=5)
        
        # Botão de visualização da rede
        ttk.Button(self.root, text="Visualização da Rede", 
                  command=self.visualize_network).grid(row=3, column=0, pady=5)
        
    def setup_scenario_1(self):
        self.G.clear()
        
        # Add nodes with device type attribute
        self.G.add_node("R1", type="router")
        self.G.add_node("SW1", type="switch")
        self.G.add_node("SW2", type="switch")
        for i in range(1, 7):
            self.G.add_node(f"S{i}", type="server")
        
        # Add edges with weights
        edges = [
            ("R1", "SW1", 1),
            ("R1", "SW2", 1),
            ("SW1", "S1", 2),
            ("SW1", "S2", 2),
            ("SW1", "S3", 2),
            ("SW2", "S4", 2),
            ("SW2", "S5", 2),
            ("SW2", "S6", 2)
        ]
        
        self.G.add_weighted_edges_from(edges)
        self.update_device_lists()
        
    def setup_scenario_2(self):
        self.G.clear()
        
        # Adiciona nós com atributo de tipo de dispositivo
        self.G.add_node("R1", type="router")
        for i in range(1, 5):
            self.G.add_node(f"SW{i}", type="switch")
        for i in range(1, 11):
            self.G.add_node(f"S{i}", type="server")
        
        # Adiciona arestas com pesos
        edges = [
            ("R1", "SW1", 1),
            ("R1", "SW2", 1),
            ("R1", "SW3", 1),
            ("R1", "SW4", 1),
            ("SW1", "S1", 2),
            ("SW1", "S2", 2),
            ("SW2", "S3", 2),
            ("SW2", "S4", 2),
            ("SW3", "S5", 2),
            ("SW3", "S6", 2),
            ("SW3", "S7", 2),
            ("SW4", "S8", 2),
            ("SW4", "S9", 2),
            ("SW4", "S10", 2)
        ]
        
        self.G.add_weighted_edges_from(edges)
        self.update_device_lists()
        
    def update_device_lists(self):
        devices = list(self.G.nodes())
        self.source_combo['values'] = devices
        self.dest_combo['values'] = devices
        
    def find_path(self):
        source = self.source_var.get()
        dest = self.dest_var.get()
        
        if not source or not dest:
            messagebox.showerror("Erro", "Por favor selecione o dispositivo de origem e destino")
            return
            
        try:
            # Encontra o caminho mais curto e a distância
            path = nx.shortest_path(self.G, source, dest, weight='weight')
            distance = nx.shortest_path_length(self.G, source, dest, weight='weight')
            
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, f"Caminho mais curto: {' -> '.join(path)}\n")
            self.result_text.insert(END, f"Distância Total: {distance}")
        except nx.NetworkXNoPath:
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, "Não há caminho entre os dispositivos selecionados")
            
    def visualize_network(self):
        plt.figure(figsize=(12, 8))
        
        # Cria o layout spring para o grafo
        pos = nx.spring_layout(self.G)
        
        # Desenha nodes diferentes para cada tipo de dispositivo.
        device_types = {
            'router': {'color': 'red', 'nodes': []},
            'switch': {'color': 'green', 'nodes': []},
            'server': {'color': 'blue', 'nodes': []}
        }
        
        for node, attr in self.G.nodes(data=True):
            node_type = attr.get('type', 'server')
            device_types[node_type]['nodes'].append(node)
            
        for device_type, info in device_types.items():
            nx.draw_networkx_nodes(self.G, pos, 
                                 nodelist=info['nodes'],
                                 node_color=info['color'],
                                 node_size=500)
        
        # Desenha as arestas e as labels 
        nx.draw_networkx_edges(self.G, pos)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        nx.draw_networkx_labels(self.G, pos)
        
        plt.title("Topologia da Rede")
        plt.axis('off')
        plt.show()

def main():
    root = Tk()
    app = NetworkGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()