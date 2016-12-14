package de.michaelfuerst.graphprogramming;


import java.util.HashMap;

/**
 * A node specification.
 *
 * @author Michael Fürst
 * @version 1.0
 */
public class NodeSpecification {
    public final String name;
    public final String code;
    public final String desc;
    public final HashMap<String, Object> args = new HashMap<String, Object>();
    public final HashMap<String, String> inputs = new HashMap<String, String>();
    public final HashMap<String, String> outputs = new HashMap<String, String>();

    public NodeSpecification(final String name, final String code, final String desc) {
        this.name = name;
        this.code = code;
        this.desc = desc;
    }

}
