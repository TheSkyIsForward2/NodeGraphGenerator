import string
import random
import tkinter as tk
from tkinter import messagebox
import os
import json

class Node:
    def __init__(self, id, Type, width, depth):
        self.id = id         # as a string
        self.Type = Type     # as a string
        self.width = width   # as a int
        self.depth = depth   # as a int

    def __str__(self):
        return f"ID: {self.id}, Type: {self.Type}, Width: {self.width}, Depth: {self.depth}"

class Edge:
    def __init__(self, From, To, Directed = True):
        self.From = From     # number as string
        self.To = To         # number as string
        self.Directed = Directed  # boolean

class Graph:
    def __init__(self):
        self.nodes = {}   # {node_id: Node}
        self.edges = []   # [Edge]
        self.adj = {}     # {node_id: [Edge]}

    def addNode(self, node: Node):
        self.nodes[node.id] = node
        self.adj[node.id] = []   #adjacency list of node

    def addEdge(self, edge: Edge):
        self.edges.append(edge)

        # add edge to adjacency list
        self.adj[edge.From].append(edge)

        # if undirected, add reverse connection
        if not edge.Directed:
            self.adj[edge.To].append(edge)

    def getNode(self, node_id: string):
        return self.nodes[node_id]

    def __str__(self):
        output = ""
        
        for node_id, edges in self.adj.items():
            output += f"{node_id}: "

            if edges:
                for edge in edges:
                    output += f"{edge.To} "
            else:
                output += ""

            output += "\n"

        return output

# tunable variables
max_depth = 7     # number of columns
max_width = 4     # maximum number of nodes in a column
min_width = 2     # minimum width of a column  

# --------------------------- GENERATOR --------------------------- 
def generate():
    # create graph
    graph = Graph()

    # create root node (id: 0, type: root, width: 0, depth: 0)
    graph.addNode(Node("0", "root", 0, 0))
    node_id = 1

    # create "columns" of nodes with depth, randomly creating 1 to max_width number of nodes
    column_width = random.choice([min_width+1, (min_width+max_width)//2])
    for depth in range(1, max_depth-1):

        for width in range(0, column_width):
            graph.addNode(Node(f"{node_id}", "mid", width, depth))
            node_id += 1

        if column_width == min_width and column_width != max_width:
            column_width += 1
        elif column_width == max_width:
            column_width -= 1
        else:
            column_width += random.choice([-1,1])

    #create end node (id: ?, type: end, width: ?, depth: max_depth-1)
    graph.addNode(Node(f"{node_id}", "end", width, max_depth-1))

    # find all nodes by depth
    nodes_by_depth = {}

    for node in graph.nodes.values():
        nodes_by_depth.setdefault(node.depth, []).append(node)

    # by depth, create edges for depth+1 children
    for depth in range(0, max_depth - 2):

        parents = nodes_by_depth.get(depth, [])
        children = nodes_by_depth.get(depth + 1, [])

        if not parents or not children:
            continue

        if depth == 0:
            for child in children:
                graph.addEdge(Edge(parents[0].id, child.id))
            continue

        # Link to width-adjacent children
        if len(parents) < len(children):
            for parent in parents:
                links = [
                n for n in children if n.width == parent.width or n.width == parent.width+1
                ]
                for link in links:
                    graph.addEdge(Edge(parent.id, link.id))
        elif depth != max_depth-2:
            for parent in parents:
                links = [
                n for n in children if n.width == parent.width or n.width == parent.width-1
                ]
                for link in links:
                    graph.addEdge(Edge(parent.id, link.id))

    end_node = graph.getNode(str(node_id))

    for parent in nodes_by_depth.get(max_depth - 2, []):
        graph.addEdge(Edge(parent.id, end_node.id))

    return graph

# --------------------------- DISPLAY --------------------------- 
NODE_RADIUS = 18 # how big nodes are
X_SPACING = 140  # space between columns
Y_SPACING = 70   # space between nodes in a column
MARGIN = 60      # margin size

# create TK and canvas
root = tk.Tk()
root.title("Procedural Graph Visualization")

message = tk.Label(root, text=f"Variables - Max Depth: {max_depth}, " + f"Max Width: {max_width}, " + f"Min Width: {min_width}")
message.pack()

canvas_width = max_depth * X_SPACING + 2 * MARGIN
canvas_height = 600

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

current_graph = ""

# parameters and buttons panel on bottom (set from left to right)

# frame to hold parameter controls
param_frame = tk.Frame(root)
param_frame.pack(padx=10, pady=10, side="left")

# StringVars to hold user input
max_depth_var = tk.StringVar(value=str(max_depth))
max_width_var = tk.StringVar(value=str(max_width))
min_width_var = tk.StringVar(value=str(min_width))

def update_parameters():
    global max_depth, max_width, min_width

    try:
        new_depth = int(max_depth_var.get())
        new_max_width = int(max_width_var.get())
        new_min_width = int(min_width_var.get())

        if new_depth > 2 and new_min_width > 0 and new_max_width > new_min_width:
            max_depth = new_depth
            max_width = new_max_width
            min_width = new_min_width

            message.config(
                text=f"Variables - Max Depth: {max_depth}, "
                     f"Max Width: {max_width}, "
                     f"Min Width: {min_width}"
            )
    except ValueError:
        messagebox.showinfo('Invalid Characters Detected', 'Please select an appropriate numerical value for all parameters')


# Max Depth
tk.Label(param_frame, text="Max Depth").pack(side="left")
tk.Entry(param_frame, textvariable=max_depth_var, width=5).pack(side="left")

# Max Width
tk.Label(param_frame, text="Max Width").pack(side="left")
tk.Entry(param_frame, textvariable=max_width_var, width=5).pack(side="left")

# Min Width
tk.Label(param_frame, text="Min Width").pack(side="left")
tk.Entry(param_frame, textvariable=min_width_var, width=5).pack(side="left")

# Apply button
button = tk.Button(
    param_frame,
    text="Apply",
    command=update_parameters
)

button.pack(side="left", padx=5)

# generate button function
def generate_clicked():
    current_graph = generate()
    draw_graph(current_graph)

def write_graph_to_json(graph):
    if graph is None:
        return

    nodes_data = []
    edges_data = []

    # Export nodes
    for node in graph.nodes.values():
        nodes_data.append({
            "id": node.id,
            "type": node.Type,
            "width": node.width,
            "depth": node.depth
        })

    # Export edges
    for from_id, edge_list in current_graph.adj.items():
        for edge in edge_list:
            edges_data.append({
                "from": edge.From,
                "to": edge.To
            })

    data = {
        "nodes": nodes_data,
        "edges": edges_data
    }

    file_path = "Saved_Graph_Output.json"

    # fresh file
    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        file.flush()
        os.fsync(file.fileno())

    message.config(text="Saved graph to JSON.")

# save to JSON button function
def save_to_json_clicked():
    write_graph_to_json(current_graph)

# create generate button
button = tk.Button(root, 
                   text="Generate", 
                   command=generate_clicked,
                   activebackground="red", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="darkblue",
                   cursor="hand2",
                   disabledforeground="blue",
                   fg="white",
                   font=("Arial", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=10,
                   pady=5,
                   width=15,
                   wraplength=100)

button.pack(padx=20, pady=20, side="left")

# create save button
button = tk.Button(root, 
                   text="Save to JSON", 
                   command=save_to_json_clicked,
                   activebackground="black", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgray",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=10,
                   pady=5,
                   width=15,
                   wraplength=100)

button.pack(padx=20, pady=20, side="left")


# draw graph function
def draw_graph(graph):
    canvas.delete('all')

    # group nodes by depth
    nodes_by_depth = {}
    for node in graph.nodes.values():
        nodes_by_depth.setdefault(node.depth, []).append(node)

    # compute positions : dict - {note.id : (x,y)} (ig. key is the node id, value is the position coordinate)
    positions = {}

    # iterate nodes by depth
    for depth, nodes in nodes_by_depth.items():
        x = MARGIN + depth * X_SPACING
        total_height = (len(nodes) - 1) * Y_SPACING
        start_y = canvas_height // 2 - total_height // 2

        for i, node in enumerate(nodes):
            y = start_y + i * Y_SPACING
            # save coordinate of node
            positions[node.id] = (x, y)

    # draw edges
    for edge in graph.edges:
        # start point
        x1, y1 = positions[edge.From]
        # end point
        x2, y2 = positions[edge.To]

        canvas.create_line(
            x1 + NODE_RADIUS, # the right side of the parent node
            y1,
            x2 - NODE_RADIUS, # the left side of the child node
            y2,
            arrow=tk.LAST,
            width=2
        )

    # draw nodes
    for node_id, (x, y) in positions.items():
        node = graph.getNode(node_id)

        if node.Type == "root":
            color = "#000000"
        elif node.Type == "end":
            color = "#d3d00d"
        else:
            color = random.choice(["#ffffff", "#0000ff", "#ff0000", "#00ff00"])

        canvas.create_oval(
            x - NODE_RADIUS,
            y - NODE_RADIUS,
            x + NODE_RADIUS,
            y + NODE_RADIUS,
            fill=color,
            outline="black"
        )

current_graph = generate()
draw_graph(current_graph)

root.mainloop()