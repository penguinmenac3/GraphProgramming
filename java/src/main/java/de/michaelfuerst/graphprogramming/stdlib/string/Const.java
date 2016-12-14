package de.michaelfuerst.graphprogramming.stdlib.string;

import de.michaelfuerst.graphprogramming.NodeSpecification;
import de.michaelfuerst.graphprogramming.stdlib.Node;

import java.util.HashMap;

/**
 * A string constant node.
 *
 * @author Michael Fürst
 * @version 1.0
 */
public class Const extends Node {
    private String constant;

    public HashMap<String, Object> tick(HashMap<String, Object> input) {
        HashMap<String, Object> result = new HashMap<String, Object>();

        result.put("result", constant);

        return result;
    }

    protected void initialize(HashMap<String, Object> args) {
        this.constant = (String)args.get("default");
    }

    protected boolean isInputNode() {
        return true;
    }

    public NodeSpecification getSpec() {
        NodeSpecification spec = new NodeSpecification("String Const", "stdlib.string.const", "Returns the arg on the output");
        spec.outputs.put("result", "String");
        return spec;
    }
}
