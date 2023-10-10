


def _pprint(obj, stream=None, indent=0):
    if stream is None:
        import sys
        stream = sys.stdout

    if isinstance(obj, dict):
        stream.write("{\n")
        for k, v in obj.items():
            stream.write("  "*indent)
            _pprint(k, stream, indent+1)
            stream.write(": ")
            _pprint(v, stream, indent+1)
            stream.write(",\n")
        stream.write("  "*indent+"}")
    else:
        print(repr(obj), file=stream, end="")


def pformat(obj):
    import io
    buf = io.StringIO()
    _pprint(obj, buf)
    return buf.getvalue()

def pprint(obj, stream=None):
    _pprint(obj, stream)
    print(file=stream)
