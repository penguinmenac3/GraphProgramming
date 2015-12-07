import os
import sys


def files_by_pattern(directory, matchFunc):
    for path, dirs, files in os.walk(directory):
        for f in filter(matchFunc, files):
            yield os.path.join(path, f)


def try_load(name, verbose):
    name = name.replace("/", ".")[2:-3]
    if name == "stdlib.Node":
        return None
    if verbose:
        print("Try loading node: " + name)
    try:
        module = __import__(name, fromlist=["Node"])
    except (ImportError, SyntaxError):
        return None
    try:
        return module.Node(False, []).toJson()
    except (AttributeError, TypeError):
        return None


if __name__ == "__main__":
    verbose = False
    filename = "../grapheditor/data/Python.nodes.json"
    for arg in sys.argv:
        if arg == "-v" or arg == "--verbose":
            verbose = True
        if arg == "-h" or arg == "--help":
            print("Usage: command [options] file")
            print("Options:")
            print("-v   --verbose   verbose mode shows modules that are tried to import.")
            print("-h   --help      shows this help")

    if len(sys.argv) > 1 and not sys.argv[-1] == "-v" and not sys.argv[-1] == "--verbose" and not sys.argv[-1] == "-h" and not sys.argv[-1] == "--help":
        filename = sys.argv[-1]


    files = files_by_pattern('.', lambda fn: fn.endswith('.py'))
    txt = "["
    for file in files:
        node = try_load(file, verbose)
        if node is not None:
            txt += node + ",\n"

    if txt.endswith(",\n"):
        txt = txt[:-2]
    txt += "]\n"

    file = open(filename, 'w')
    file.write(txt)
    print("Done. If some nodes are programmed wrong. Kill this process now.")
