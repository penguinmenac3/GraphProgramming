# This cluster host should listen on the network for graph execution requests.
# Such requests consist out of a language identifier string (lua, python, ...) and a graph to execute as well as optional arguments for the graph.
# The graph is executed in is_cluster_server mode, which might restrict some features for security of the cluster provider.
# Outputs of the graph will be reported back over a tcp connection. Each line will be a packet.
