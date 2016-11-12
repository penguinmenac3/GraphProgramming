# Cluster Client
#
# This cluster client connects to a cluster host and sends it the language, graph and optional arguments.
# It listens on a tcp socket for the output and prints it to the console.
#
# There should be some crypto and authentication going on between client and host, so that they can be exposed to the internet! (But it should be ongoing in the background)
# There should be some scripts to setup connectability between client and host, so than when actually starting client and host you do not need to care about it.
#
# This way the cluster_client looks to the outside like a graphex-file and can be directly called by the ui.
#
# Usage: python cluster_client.py <host> <language> <path/to/file.graph.json> [args]
#
