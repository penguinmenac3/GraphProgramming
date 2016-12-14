package de.michaelfuerst.graphprogramming.stdlib;

import de.michaelfuerst.graphprogramming.ITickable;
import de.michaelfuerst.graphprogramming.NodeSpecification;

import java.util.HashMap;
import java.util.UUID;

/**
 * A node to implement.
 *
 * @author Michael Fürst
 * @version 1.0
 */
public abstract class Node implements ITickable, Cloneable {
    private String name;

    /**
     * Searches, loads and creates a new instance of a node.
     * Returns null if not found.
     *
     * @param code The code string in the graph.
     * @param args The arguments for the node to initialize.
     * @return The node.
     */
    public static Node getNewInstanceOfNode(final String code, final HashMap<String, Object> args) {
        String[] tmp = code.split(".");
        String processedCode = "de.michaelfuerst.graphprogramming.";
        for (int i = 0; i < tmp.length; i++) {
            if (i + 1 < tmp.length) {
                processedCode += tmp[i] + ".";
            } else {
                processedCode += tmp[i].substring(0, 1).toUpperCase() + tmp[i].substring(1);
            }
        }
        try {
            Node node = (Node)Class.forName(processedCode).newInstance();
            node.setName(node.getSpec().name + "_" + UUID.randomUUID().toString());
            node.initialize(args);
            return node;
        } catch (ClassNotFoundException e) {
            return null;
        } catch (InstantiationException e) {
            return null;
        } catch (IllegalAccessException e) {
            return null;
        }
    }

    /**
     * Initialize the node with the given parameters.
     *
     * They are specific for the node and specified in the GPIL.
     *
     * @param args The arguments for the node.
     */
    protected abstract void initialize(final HashMap<String, Object> args);

    /**
     * Return if the node is an input node for the net.
     * Sources should set this to true everyone else to false.
     *
     * In some cases this may be dependant on the args of the node.
     * @return if the node is an input node for the net.
     */
    protected abstract boolean isInputNode();

    /**
     * Set the name of a node.
     *
     * @param name The name.
     */
    public final void setName(final String name) {
        this.name = name;
    }

    /**
     * Get the name of the node.
     *
     * @return The name of the node.
     */
    public final String getName() {
        return name;
    }

    /**
     * Get the specification of the node.
     *
     * @return The specification of the node.
     */
    public abstract NodeSpecification getSpec();
}
