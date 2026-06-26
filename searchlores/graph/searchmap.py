import networkx as nx
from typing import Dict, List

class SearchMap:
    def __init__(self, context):
        self.context = context
        self.graph = nx.DiGraph()
        self._build()

    def _build(self):
        self.graph.add_node("PROMPT", type="origin", content=self.context.prompt[:50])

        for layer in self.context.layers:
            node_id = f"{layer['stratum']}_{layer['plugin']}"
            self.graph.add_node(node_id,
                              type="stratum",
                              stratum=layer['stratum'],
                              findings=layer['findings'])
            self.graph.add_edge("PROMPT", node_id, relation="excavated_by")

        for i, contradiction in enumerate(self.context.contradictions):
            node_id = f"contradiction_{i}"
            self.graph.add_node(node_id, type="tension", **contradiction)
            self.graph.add_edge("PROMPT", node_id, relation="contains_tension")

        for i, vector in enumerate(self.context.power_vectors):
            node_id = f"power_{i}"
            self.graph.add_node(node_id, type="power", description=vector)
            self.graph.add_edge("PROMPT", node_id, relation="legitimized_by")

        for omission in self.context.omissions:
            node_id = f"silence_{omission}"
            self.graph.add_node(node_id, type="absence", dimension=omission)
            self.graph.add_edge("PROMPT", node_id, relation="occults")

    def to_mermaid(self) -> str:
        lines = ["graph TD"]
        for node, data in self.graph.nodes(data=True):
            safe_node = node.replace(" ", "_").replace("-", "_")
            label = data.get('type', 'node')
            lines.append(f"    {safe_node}[{label}]")

        for u, v, data in self.graph.edges(data=True):
            safe_u = u.replace(" ", "_").replace("-", "_")
            safe_v = v.replace(" ", "_").replace("-", "_")
            rel = data.get('relation', '->')
            lines.append(f"    {safe_u} -->|{rel}| {safe_v}")

        return "\n".join(lines)

    def critical_path(self) -> List[str]:
        power_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'power']
        return power_nodes