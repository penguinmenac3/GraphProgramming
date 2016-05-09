from __future__ import absolute_import
import json
"""
A node archetype.
"""


class Node(object):

    """
    A node constructor.
    @:param name the name of the node.
    @:param code the code link
    @:param defaultArgs the default arguments of the ndoe
    @:param inputs the inputs of the node
    @:param outputs the outputs of the node
    @:param description the description text for the node
    @:param verbose the verbose flag for debugging.
    @:param isInput optional if the node is an input node
    @:param isRepeating optional if the node is a repeating node
    """
    def __init__(self, name, code, defaultArgs, inputs, outputs, description, verbose, isInput=False, isRepeating=False,
                 needs_foreground = False):
        self.needs_foreground = needs_foreground
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.description = description
        self.verbose = verbose
        self.repeating = isRepeating
        self.input = isInput
        self.code = code
        self.defaultArgs = defaultArgs
        if verbose:
            print("Created " + name + "node.")

    """
    The tick of the node.
    This is the heartbeat.
    Implement your stuff here.
    @:param value The value-dict for the tick call.
    """
    def tick(self, value):
        return {}

    # ***************************************************************************
    # You should not touch these methods below!
    # ***************************************************************************

    def isInput(self):
        return self.input

    def isRepeating(self):
        return self.repeating

    def getInputs(self):
        return self.inputs

    def getOutputs(self):
        return self.outputs

    def getName(self):
        return self.name

    def getCode(self):
        return self.code

    def getDefaultArgs(self):
        return self.defaultArgs

    def getDescription(self):
        return self.description

    def toString(self):
        return self.getName() + " (" + self.getDescription() + ") [repeating:" + str(self.isRepeating()) + ", input:" + str(self.isInput()) + "]"

    def needsForeground(self):
        return self.needs_foreground

    def toJson(self):
        return '''{
    "name": "''' + self.getName() + '''",
    "code": "''' + self.getCode() + '''",
    "inputs": ''' + json.dumps(self.getInputs()) + ''',
    "outputs": ''' + json.dumps(self.getOutputs()) + ''',
    "args": ''' + json.dumps(self.getDefaultArgs()) + ''',
    "desc": "''' + self.getDescription() + '''"
}'''

if __name__ == "__main__":
    print(Node("Node", {}, {}, "A base node. Archetype for all nodes.", False).toString())
