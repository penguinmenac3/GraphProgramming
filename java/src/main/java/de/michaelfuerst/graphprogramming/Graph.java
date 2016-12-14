package de.michaelfuerst.graphprogramming;


import de.michaelfuerst.graphprogramming.stdlib.Node;

import java.util.*;

/**
 * A compute graph.
 *
 * @author Michael Fürst
 * @version 1.0
 */
public class Graph {
    private final HashMap<String, Node> nodes = new HashMap<String, Node>();
    private final HashMap<String, List<String>> connections = new HashMap<String, List<String>>();

    /**
     * Create an empty compute graph.
     */
    public Graph() {}

    /**
     * Load and create a compute graph.
     * @param pathToFile The path to the file.
     */
    public Graph(final String pathToFile) {
        // TODO load graph from file into nodes and connections.
    }

    /**
     * Add a node to the graph.
     *
     * @param node The node to add to the graph.
     */
    public void addNode(final Node node) {
        nodes.put(node.getName(), node);
    }

    /**
     * Add a connection to the graph.
     *
     * @param from The starting point of the connection.
     * @param to The end point of the connection.
     */
    public void addConnection(final String from, final String to) {
        if(!connections.containsKey(from)) {
            connections.put(from, new ArrayList<String>());
        }
        connections.get(from).add(to);
    }

    /**
     * Get the receivers of a topic.
     *
     * @param topic The topic.
     * @return The list of receivers.
     */
    public List<String> getReceivers(final String topic) {
        return connections.get(topic);
    }

    /**
     * Get a node.
     *
     * @param nodeId of the node in the graph.
     * @return The Node.
     */
    public Node getNode(final String nodeId) {
        return nodes.get(nodeId);
    }

    /**
     * Get all nodes in the graph.
     *
     * @return A list of all nodes.
     */
    public Collection<Node> getNodes() {
        return this.nodes.values();
    }


}
