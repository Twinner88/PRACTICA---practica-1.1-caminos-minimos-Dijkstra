import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bryan Mendoza ")
        self.root.geometry("1000x650")

        # ====== VARIABLES ======
        self.G = nx.Graph()
        self.pos = {}
        self.node_count = 0
        self.selected_nodes = []
        self.node_color = "skyblue"

        # ====== ESTRUCTURA PRINCIPAL ======
        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill="both", expand=True)

        # --- PANEL IZQUIERDO (gráfico) ---
        self.graph_frame = ttk.LabelFrame(self.frame, text="Área de dibujo del grafo", padding=5)
        self.graph_frame.grid(row=0, column=0, rowspan=10, sticky="nsew", padx=(0, 10))

        self.figure = plt.Figure(figsize=(6, 6))
        self.ax = self.figure.add_subplot(111)
        self.ax.axis("off")
        self.figure.patch.set_facecolor("lightblue")  # color del fondo

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # --- PANEL DERECHO (controles) ---
        ttk.Label(self.frame, text="Controles del Grafo", font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w")

        ttk.Label(self.frame, text="Nodo inicial:").grid(row=1, column=1, sticky="w", pady=5)
        self.start_node = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.start_node, width=8).grid(row=1, column=2, sticky="w")

        ttk.Label(self.frame, text="Nodo final:").grid(row=2, column=1, sticky="w", pady=5)
        self.end_node = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.end_node, width=8).grid(row=2, column=2, sticky="w")

        ttk.Label(self.frame, text="Peso:").grid(row=3, column=1, sticky="w", pady=5)
        self.edge_weight = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.edge_weight, width=8).grid(row=3, column=2, sticky="w")

        # Botones de acción
        ttk.Button(self.frame, text="Agregar Conexión", command=self.agregar_conexion).grid(row=4, column=1, columnspan=2, pady=5, sticky="ew")
        ttk.Button(self.frame, text="Ejecutar Dijkstra", command=self.ejecutar_dijkstra).grid(row=5, column=1, columnspan=2, pady=5, sticky="ew")

        ttk.Label(self.frame, text="Color de nodo:").grid(row=6, column=1, sticky="w", pady=5)

        colores = [("Rojo", "lightcoral"), ("Verde", "lightgreen"), ("Azul", "skyblue"), ("Amarillo", "khaki")]
        self.color_var = tk.StringVar(value="skyblue")
        for i, (nombre, color) in enumerate(colores):
            ttk.Radiobutton(self.frame, text=nombre, value=color, variable=self.color_var, command=self.cambiar_color).grid(row=7+i, column=1, columnspan=2, sticky="w")

        # Etiqueta de resultados
        ttk.Label(self.frame, text="Resultado:", font=("Arial", 10, "bold")).grid(row=11, column=1, sticky="w", pady=(15, 0))
        self.resultados = tk.StringVar(value="Esperando ejecución...")
        ttk.Label(self.frame, textvariable=self.resultados, wraplength=250, justify="left").grid(row=12, column=1, columnspan=2, sticky="w")

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

    # ====== FUNCIONES ======
    def cambiar_color(self):
        """Cambia el color del nodo."""
        self.node_color = self.color_var.get()

    def on_click(self, event):
        """Crea un nodo en el área de dibujo."""
        if event.inaxes != self.ax:
            return

        self.node_count += 1
        nodo = self.node_count
        self.G.add_node(nodo)
        self.pos[nodo] = (event.xdata, event.ydata)
        self.dibujar_grafo()

    def agregar_conexion(self):
        """Agrega una arista entre nodos existentes."""
        try:
            u = int(self.start_node.get())
            v = int(self.end_node.get())
            w = float(self.edge_weight.get())

            if u not in self.G.nodes or v not in self.G.nodes:
                messagebox.showerror("Error", "Uno de los nodos no existe.")
                return

            self.G.add_edge(u, v, weight=w)
            self.dibujar_grafo()
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos para nodos y peso.")

    def ejecutar_dijkstra(self):
        """Ejecuta Dijkstra entre el nodo inicial y final."""
        try:
            start = int(self.start_node.get())
            end = int(self.end_node.get())
            if start not in self.G.nodes or end not in self.G.nodes:
                messagebox.showerror("Error", "Los nodos no existen en el grafo.")
                return

            dist, path = nx.single_source_dijkstra(self.G, start, end)
            camino = path
            peso_total = dist

            self.dibujar_grafo(camino)
            self.resultados.set(f"Camino mínimo: {camino}\nPeso total: {peso_total}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def dibujar_grafo(self, camino=None):
        """Dibuja el grafo y resalta el camino mínimo."""
        self.ax.clear()
        nx.draw(self.G, self.pos, with_labels=True,
                node_color=self.node_color, node_size=800, ax=self.ax)
        etiquetas = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=etiquetas, font_color="green", ax=self.ax)
        nx.draw_networkx_edges(self.G, self.pos, width=2, edge_color="green", ax=self.ax)

        # Resaltar camino mínimo
        if camino and len(camino) > 1:
            edges = list(zip(camino, camino[1:]))
            nx.draw_networkx_edges(self.G, self.pos, edgelist=edges, width=4, edge_color="red", ax=self.ax)

        self.ax.axis("off")
        self.canvas.draw()


# ====== EJECUCIÓN ======
if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()
