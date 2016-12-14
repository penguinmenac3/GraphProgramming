package de.michaelfuerst.graphprogramming;

import de.michaelfuerst.graphprogramming.stdlib.Node;

import java.util.HashMap;

/**
 * A tickable interface.
 *
 * @author Michael Fürst
 * @version 1.0
 */
public class TestAGraph {

    public static void main(String[] args) {
        final Graph graph = new Graph();
        final HashMap<String, Object> constArgs = new HashMap<String, Object>();
        final HashMap<String, Object> printArgs = new HashMap<String, Object>();

        constArgs.put("default", "Hello World!");
        Node strConst = Node.getNewInstanceOfNode("stdlib.string.const", constArgs);
        Node sysPrint = Node.getNewInstanceOfNode("stdlib.system.print", printArgs);

        graph.addNode(sysPrint);
        graph.addNode(strConst);

        graph.addConnection(strConst.getName() + "/result", sysPrint.getName() + "/val");

        GraphExecutor graphEx = new GraphExecutor(graph);
        graphEx.executeSingleThreaded();
    }
}
