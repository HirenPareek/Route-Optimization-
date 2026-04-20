import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq
import time
import random

# Cities and positions
cities = ['Chennai', 'Sriperumbudur', 'Vellore', 'Salem', 'Krishnagiri', 'Hosur', 'Bangalore', 'Chittoor', 'Kanchipuram', 'Tiruvannamalai', 'Dharmapuri', 'Mysore']
positions = {
    'Chennai': (0, 0),
    'Sriperumbudur': (3, 0),
    'Vellore': (9, 3),
    'Salem': (12, -6),
    'Krishnagiri': (18, 3),
    'Hosur': (24, 3),
    'Bangalore': (30, 3),
    'Chittoor': (15, 9),
    'Kanchipuram': (6, -1.5),
    'Tiruvannamalai': (12, 0),
    'Dharmapuri': (21, -3),
    'Mysore': (33, 0)
}

# Traffic penalties
traffic_penalties = {'Low': 10, 'Medium': 50, 'Heavy': 100}

# Create graph
G = nx.Graph()
for city, pos in positions.items():
    G.add_node(city, pos=pos)

# Edges with distance and traffic
edges = [
    ('Chennai', 'Sriperumbudur', {'distance': 50, 'traffic': 'Low'}),
    ('Sriperumbudur', 'Vellore', {'distance': 100, 'traffic': 'Medium'}),
    ('Sriperumbudur', 'Kanchipuram', {'distance': 60, 'traffic': 'Low'}),
    ('Sriperumbudur', 'Salem', {'distance': 150, 'traffic': 'Heavy'}),
    ('Vellore', 'Krishnagiri', {'distance': 80, 'traffic': 'Low'}),
    ('Vellore', 'Chittoor', {'distance': 60, 'traffic': 'Medium'}),
    ('Vellore', 'Tiruvannamalai', {'distance': 70, 'traffic': 'Low'}),
    ('Salem', 'Krishnagiri', {'distance': 120, 'traffic': 'Medium'}),
    ('Salem', 'Dharmapuri', {'distance': 90, 'traffic': 'Heavy'}),
    ('Krishnagiri', 'Hosur', {'distance': 70, 'traffic': 'Low'}),
    ('Krishnagiri', 'Dharmapuri', {'distance': 50, 'traffic': 'Medium'}),
    ('Hosur', 'Bangalore', {'distance': 40, 'traffic': 'Heavy'}),
    ('Hosur', 'Mysore', {'distance': 120, 'traffic': 'Medium'}),
    ('Bangalore', 'Mysore', {'distance': 140, 'traffic': 'Low'}),
    ('Chittoor', 'Krishnagiri', {'distance': 90, 'traffic': 'Medium'}),
    ('Kanchipuram', 'Tiruvannamalai', {'distance': 100, 'traffic': 'Medium'}),
    ('Tiruvannamalai', 'Dharmapuri', {'distance': 110, 'traffic': 'Heavy'}),
]

for u, v, data in edges:
    G.add_edge(u, v, **data)

# Heuristic function (Euclidean distance)
def heuristic(node, goal):
    x1, y1 = positions[node]
    x2, y2 = positions[goal]
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

# Dijkstra algorithm
def dijkstra(G, start, goal):
    queue = [(0, start, [])]  # cost, node, path
    visited = set()
    costs = {node: float('inf') for node in G.nodes}
    costs[start] = 0
    visited_order = []
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        visited_order.append(node)
        path = path + [node]
        if node == goal:
            return path, cost, len(visited), visited_order
        for neighbor in G.neighbors(node):
            edge_data = G[node][neighbor]
            dist = edge_data['distance']
            traf = edge_data['traffic']
            penalty = traffic_penalties[traf]
            new_cost = cost + dist + penalty
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor, path))
    return None, float('inf'), len(visited), visited_order

# A* algorithm
def astar(G, start, goal):
    queue = [(0 + heuristic(start, goal), 0, start, [])]  # f, g, node, path
    visited = set()
    costs = {node: float('inf') for node in G.nodes}
    costs[start] = 0
    visited_order = []
    while queue:
        f, g, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        visited_order.append(node)
        path = path + [node]
        if node == goal:
            return path, g, len(visited), visited_order
        for neighbor in G.neighbors(node):
            edge_data = G[node][neighbor]
            dist = edge_data['distance']
            traf = edge_data['traffic']
            penalty = traffic_penalties[traf]
            new_g = g + dist + penalty
            if new_g < costs[neighbor]:
                costs[neighbor] = new_g
                f = new_g + heuristic(neighbor, goal)
                heapq.heappush(queue, (f, new_g, neighbor, path))
    return None, float('inf'), len(visited), visited_order

# Randomize traffic
def randomize_traffic():
    traffics = ['Low', 'Medium', 'Heavy']
    for u, v in G.edges:
        G[u][v]['traffic'] = random.choice(traffics)
        G[u][v]['distance'] = random.randint(50, 200)
    draw_graph()

# Draw graph
def draw_graph(path=None, visited_order=None):
    ax.clear()
    ax_seq.clear()
    pos = nx.get_node_attributes(G, 'pos')
    # Optional: overlay map image (uncomment and add 'india_map.png' in the directory)
    # ax.imshow(plt.imread('india_map.png'), extent=[-3, 36, -9, 12], alpha=0.3)
    # Draw nodes
    if visited_order:
        import matplotlib.cm as cm
        colors = cm.plasma([i / len(visited_order) for i in range(len(visited_order))])
        node_colors = ['lightblue'] * len(G.nodes)
        for i, node in enumerate(visited_order):
            idx = list(G.nodes).index(node)
            node_colors[idx] = colors[i]
    else:
        node_colors = 'lightblue'
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=400)
    # Draw edges with traffic colors
    edge_colors = []
    edge_labels = {}
    for u, v in G.edges:
        traf = G[u][v]['traffic']
        dist = G[u][v]['distance']
        if traf == 'Low':
            color = 'green'
        elif traf == 'Medium':
            color = 'orange'
        else:
            color = 'red'
        edge_colors.append(color)
        edge_labels[(u, v)] = f"{dist}\n{traf}"
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=2)
    # Highlight path if provided
    if path:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax, edge_color='blue', width=4, arrows=True, arrowstyle='->')
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
    nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax, font_size=6)
    
    # Draw sequence
    if visited_order:
        ax_seq.set_title("Exploration Sequence")
        ax_seq.set_xlim(-1, len(visited_order))
        ax_seq.set_ylim(-1, 1)
        ax_seq.axis('off')
        for i, node in enumerate(visited_order):
            ax_seq.scatter(i, 0, color=colors[i], s=200, zorder=5)
            ax_seq.text(i, 0.5, node, ha='center', va='bottom', fontsize=8, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
            if i < len(visited_order) - 1:
                ax_seq.arrow(i, 0, 0.8, 0, head_width=0.1, head_length=0.1, fc=colors[i], ec=colors[i], zorder=4)
    else:
        ax_seq.set_title("Exploration Sequence")
        ax_seq.text(0.5, 0.5, "Run an algorithm to see the sequence", ha='center', va='center', transform=ax_seq.transAxes)
    
    canvas.draw()

# Run algorithm
def run_algorithm():
    start = source_var.get()
    goal = dest_var.get()
    algo = algo_var.get()
    start_time = time.time()
    if algo == 'Dijkstra':
        path, cost, visited, visited_order = dijkstra(G, start, goal)
    else:
        path, cost, visited, visited_order = astar(G, start, goal)
    end_time = time.time()
    exec_time = end_time - start_time
    text_area.delete(1.0, tk.END)
    if path:
        text_area.insert(tk.END, f"Path: {' -> '.join(path)}\n")
        text_area.insert(tk.END, f"Total Cost: {cost}\n")
        text_area.insert(tk.END, f"Nodes Visited: {visited}\n")
        text_area.insert(tk.END, f"Execution Time: {exec_time:.4f} s\n")
        text_area.insert(tk.END, f"Visited Order: {' -> '.join(visited_order)}\n")
        if algo == 'A*':
            heuristics = {node: round(heuristic(node, goal), 2) for node in G.nodes}
            text_area.insert(tk.END, f"Heuristics: {heuristics}\n")
        draw_graph(path, visited_order)
    else:
        text_area.insert(tk.END, "No path found\n")

# GUI setup
root = tk.Tk()
root.title("Pathfinding Demo")

source_var = tk.StringVar(value=cities[0])
dest_var = tk.StringVar(value=cities[-1])
algo_var = tk.StringVar(value='Dijkstra')

ttk.Label(root, text="Source:").pack()
source_menu = ttk.Combobox(root, textvariable=source_var, values=cities)
source_menu.pack()

ttk.Label(root, text="Destination:").pack()
dest_menu = ttk.Combobox(root, textvariable=dest_var, values=cities)
dest_menu.pack()

ttk.Label(root, text="Algorithm:").pack()
algo_menu = ttk.Combobox(root, textvariable=algo_var, values=['Dijkstra', 'A*'])
algo_menu.pack()

run_btn = tk.Button(root, text="Run", command=run_algorithm)
run_btn.pack(pady=(10, 2))

rand_btn = tk.Button(root, text="Randomize Traffic", command=randomize_traffic)
rand_btn.pack(pady=(0, 10))

text_area = tk.Text(root, height=14, width=80, font=("Segoe UI", 11, "bold"), bg="#f5f5f5", relief="groove", bd=3, wrap="word")
text_area.pack(fill='x', padx=10, pady=(0, 10))

fig, (ax, ax_seq) = plt.subplots(2, 1, figsize=(12, 12))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Initial draw
draw_graph()

root.geometry("1400x1100")
root.mainloop()