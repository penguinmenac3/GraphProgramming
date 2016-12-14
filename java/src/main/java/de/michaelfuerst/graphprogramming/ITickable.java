package de.michaelfuerst.graphprogramming;

import java.util.HashMap;

/**
 * A tickable interface.
 *
 * @author Michael Fürst
 * @version 1.0
 */
public interface ITickable {
    HashMap<String, Object> tick(HashMap<String, Object> input);
}
