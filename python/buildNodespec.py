import os
import sys


def files_by_pattern(directory, matchFunc):
    for path, dirs, files in os.walk(directory):
        for f in filter(matchFunc, files):
            yield os.path.join(path, f)


def try_load(name, verbose, i, total):
    name = name.replace("/", ".")[2:-3]
    if verbose:
        print("[" + str(i) + "/" + str(total) + "] Parsing: " + name)
    if name == "stdlib.Node" or name == "graphex" or name == "buildNodespec" or name.endswith(
            "__init__") or name.endswith("_Lib"):
        return False, None
    try:
        module = __import__(name, fromlist=["Node"])
    except (ImportError, SyntaxError) as e:
        if verbose:
            print("Syntax or import error at: " + name)
            print(e)
        return False, (name, e)
    try:
        return True, module.Node(False, []).toJson()
    except (AttributeError, TypeError) as e:
        if verbose:
            print("Failed parsing " + name + "!")
            print(e)
        return False, (name, e)


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

    if len(sys.argv) > 1 and not sys.argv[-1] == "-v" and not sys.argv[-1] == "--verbose" and not sys.argv[
        -1] == "-h" and not sys.argv[-1] == "--help":
        filename = sys.argv[-1]

    files = [f for f in files_by_pattern('.', lambda fn: fn.endswith('.py'))]
    txt = "["
    total = len(files)
    i = 1
    errs = []
    for file in files:
        success, node = try_load(file, verbose, i, total)
        i += 1
        if success:
            txt += node + ",\n"
        elif node is not None:
            errs.append(node)

    if verbose:
        print()

    for e in errs:
        name = e[0]
        ex = e[1]
        print("ERROR in module " + name)
        print(ex)
        print()

    if txt.endswith(",\n"):
        txt = txt[:-2]
    txt += "]\n"

    file = open(filename, 'w')
    file.write(txt)
    if len(errs) > 0:
        print(str(len(errs)) + " errors occured.")
    else:
        print("Done.")