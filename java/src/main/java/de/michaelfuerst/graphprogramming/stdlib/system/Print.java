package de.michaelfuerst.graphprogramming.stdlib.system;

import de.michaelfuerst.graphprogramming.NodeSpecification;
import de.michaelfuerst.graphprogramming.stdlib.Node;

import java.util.HashMap;

/**
 * A string constant node.
 *
 * @author Michael Fürst
 * @version 1.0
 */
public class Print extends Node {

    public HashMap<String, Object> tick(HashMap<String, Object> input) {
        System.out.println(input.get("val"));
        return null;
    }

    protected void initialize(HashMap<String, Object> args) {

    }

    protected boolean isInputNode() {
        return false;
    }

    public NodeSpecification getSpec() {
        NodeSpecification spec = new NodeSpecification("Print", "stdlib.system.print", "Print on the screen");
        spec.inputs.put("val", "Object");
        return spec;
    }
}
