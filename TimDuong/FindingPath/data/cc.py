from __future__ import annotations

from pathlib import Path

import networkx as nx
import osmnx as ox

SYDNEY_PLACE = "Sydney, New South Wales, Australia"
RAILWAY_FILTER = '["railway"~"rail|subway|light_rail|tram|monorail|narrow_gauge|funicular"]'
OUTPUT_PATH = Path(__file__).resolve().parent / "sydney_metro.graphml"


def _to_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def build_sydney_rail_graph(output_path: Path = OUTPUT_PATH):
    print("Downloading Sydney railway network from OpenStreetMap...")
    graph = ox.graph_from_place(
        SYDNEY_PLACE,
        custom_filter=RAILWAY_FILTER,
        simplify=True,
        retain_all=True,
    )

    if not isinstance(graph, nx.MultiDiGraph):
        # Keep directed multi-edge structure expected by the app.
        graph = nx.MultiDiGraph(graph)

    missing_xy = []
    for node, data in graph.nodes(data=True):
        x = data.get("x")
        y = data.get("y")
        if x is None or y is None:
            missing_xy.append(node)
            continue
        data["x"] = _to_float(x)
        data["y"] = _to_float(y)
        if "name" in data and isinstance(data["name"], list):
            data["name"] = ", ".join(map(str, data["name"]))

    if missing_xy:
        graph.remove_nodes_from(missing_xy)

    for _, __, ___, data in graph.edges(keys=True, data=True):
        length = _to_float(data.get("length"), 1.0)
        data["length"] = max(length, 1.0)
        data["cost"] = data["length"]
        if "name" in data and isinstance(data["name"], list):
            data["name"] = ", ".join(map(str, data["name"]))
        if "ref" in data and isinstance(data["ref"], list):
            data["ref"] = ", ".join(map(str, data["ref"]))
        if "route" in data and isinstance(data["route"], list):
            data["route"] = ", ".join(map(str, data["route"]))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    ox.save_graphml(graph, output_path)

    print("Saved GraphML:", output_path)
    print("Nodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())


if __name__ == "__main__":
    build_sydney_rail_graph()
