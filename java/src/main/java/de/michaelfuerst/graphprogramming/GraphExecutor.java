package de.michaelfuerst.graphprogramming;

import de.michaelfuerst.graphprogramming.stdlib.Node;

import java.util.HashMap;
import java.util.List;

/**
 * The graph executor.
 *
 * Maybe interpret this as a sheduler for a compute graph.
 *
 * @author Michael Fürst
 * @version 1.0
 */
public class GraphExecutor {
    private final Graph graph;
    private List<Node> inputNodes;

    /**
     * Create a graph executor for a graph.
     *
     * @param graph The graph for which to create the executor.
     */
    public GraphExecutor(final Graph graph) {
        this.graph = graph;
    }

    /**
     * Execute the graph in an old fashioned single threaded manner.
     */
    public void executeSingleThreaded() {
        // TODO do magic stuff.
    }

    /**
     * Execute the graph in a parallel multi threaded way.
     */
    public void executeMultiThreadded() {
        throw new UnsupportedOperationException("Not yet implemented!");
    }

    public HashMap<String, Object> getResult() {
        return new HashMap<String, Object>();
    }
}
