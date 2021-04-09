# (c) 2019 Paul Sokolovsky, MIT license
from token import *
from ucollections import namedtuple


NL = 55
ENCODING = 56
tok_name[NL] = "NL"
tok_name[ENCODING] = "ENCODING"


class TokenInfo(namedtuple("TokenInfo", ("type", "string", "start", "end", "line"))):

    def __str__(self):
        return "TokenInfo(type=%d (%s), string=%r, line=%r)" % (
            self.type, tok_name[self.type], self.string, self.line
        )


def get_indent(l):
    for i in range(len(l)):
        if l[i] != " ":
            return i, l[i:]


def generate_tokens(readline):

    indent = 0
    indent_lvl = 0

    # generate_tokens() doesn't yield this, only tokenine() does.
    #yield TokenInfo(ENCODING, "utf-8", 0, 0, "")

    while True:
        l = readline()
        org_l = l
        if not l:
            break
        i, l = get_indent(l)

        if l == "\n":
            yield TokenInfo(NL, l, 0, 0, org_l)
            continue

        if i > indent:
            yield TokenInfo(INDENT, " " * (i - indent), 0, 0, org_l)
            indent_lvl += 1
        elif i < indent:
            yield TokenInfo(DEDENT, "", 0, 0, org_l)
            indent_lvl -= 1
        indent = i

        while l:
            if l[0].isdigit():
                t = ""
                while l and (l[0].isdigit() or l[0] == "."):
                    t += l[0]
                    l = l[1:]
                yield TokenInfo(NUMBER, t, 0, 0, org_l)
            elif l[0].isalpha():
                name = ""
                while l and (l[0].isalpha() or l[0].isdigit()):
                    name += l[0]
                    l = l[1:]
                yield TokenInfo(NAME, name, 0, 0, org_l)
            elif l[0] == "\n":
                yield TokenInfo(NEWLINE, "\n", 0, 0, org_l)
                break
            elif l[0].isspace():
                l = l[1:]
            else:
                yield TokenInfo(OP, l[0], 0, 0, org_l)
                l = l[1:]

    while indent_lvl:
        yield TokenInfo(DEDENT, "", 0, 0, "")
        indent_lvl -= 1

    yield TokenInfo(ENDMARKER, "", 0, 0, "")
