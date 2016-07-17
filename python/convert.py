import json
import sys

class GraphConvert(object):
    def __init__(self, graph_path, node_spec_path):
        # Open the graph and parse it as json.
        data = open(graph_path, 'r').read()
        self.graph_path = graph_path
        self.raw_graph = json.loads(data)

        node_spec_data = open(node_spec_path, 'r').read()
        self.node_spec = json.loads(node_spec_data)

    def update_code_nodes(self):
        for node in self.raw_graph["nodes"]:
            code = node["code"]
            found_matching = False
            for candidate in self.node_spec:
                code_candidate = candidate["code"]
                nolib_candidate = code_candidate[code_candidate.index(".")+1:]
                if nolib_candidate == code:
                    print("Matched " + code + " -> " + code_candidate + ".")
                    node["code"] = code_candidate
                    found_matching = True
                    break
            if not found_matching:
                print("No match for " + code + ".")

    def save_graph(self):
        with open(self.graph_path, 'w') as data:
            data.write(json.dumps(self.raw_graph, indent=4, sort_keys=True))

if __name__ == "__main__":
    # Execute all graph paths passed as parameters.
    if len(sys.argv) < 3:
        print("Usage: python convert.py <graph> <nodespec>")
    else:
        offset = 2
        conv = GraphConvert("../grapheditor/" + sys.argv[1], "../grapheditor/" + sys.argv[2])
        conv.update_code_nodes()
        conv.save_graph()
