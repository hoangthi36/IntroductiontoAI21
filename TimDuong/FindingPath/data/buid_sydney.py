import osmnx as ox
import networkx as nx

print("Đang tải dữ liệu metro Sydney từ OSM...")

# Bộ lọc railway
custom_filter = (
    '["railway"~"rail|subway|light_rail"]'
)

# Tải graph
G = ox.graph_from_place(
    "Sydney, New South Wales, Australia",
    custom_filter=custom_filter,
    simplify=True
)

print("Số node:", len(G.nodes))
print("Số edge:", len(G.edges))

# Đảm bảo edge có length
for u, v, k, data in G.edges(keys=True, data=True):

    if "length" not in data:
        data["length"] = 1.0

    # Cost mặc định
    data["cost"] = float(data["length"])

# Đảm bảo node có x/y
remove_nodes = []

for node, data in G.nodes(data=True):

    if "x" not in data or "y" not in data:
        remove_nodes.append(node)

for n in remove_nodes:
    G.remove_node(n)

print("Sau khi làm sạch:")
print("Nodes:", len(G.nodes))
print("Edges:", len(G.edges))

# Lưu graphml
output_path = "sydney_metro.graphml"

ox.save_graphml(G, output_path)

print(f"Đã lưu: {output_path}")