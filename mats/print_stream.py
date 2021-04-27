import sys

from adt import adt, Case

class PrintStream:
    @adt
    class Line:
        ERROR: Case[str, str]
        LINE: Case[str, str]
        INDENTATION: Case[bool]

    def __init__(self, reset_decorator= None):
        self.reset_decorator = reset_decorator or "" 
        self.data = []
        self.indentation_level = 0

    def __indent__(self, indent = True):
        delta = 2 if indent else -2
        self.indentation_level = max(self.indentation_level + delta, 0)
    
    def line(self, line, color = None):
        self.data.append(self.Line.LINE(line, color or None))
        return self
    
    def error(self, err, color = None):
        self.data.append(self.Line.ERROR(err, color))
        return self

    def indent(self):
        self.data.append(self.Line.INDENTATION(True))
        return self
    
    def unindent(self):
        self.data.append(self.Line.INDENTATION(False))
        return self
    
    def newline(self):
        self.data.append(self.Line.LINE("", None))

    def conditional(self, condition, fun):
        if condition:
            fun(self)
        return self

    def with_indent(self, fun):
        self.indent()
        fun(self)
        self.unindent()
        return self

    def print(self):
        for line in self.data:
            line.match(
                error= lambda e, col: print(self.__pretty__(e, col), file=sys.stderr),
                line= lambda e, col: print(self.__pretty__(e, col)),
                indentation= lambda indent: self.__indent__(indent)
            )
    
    def __pretty__(self, string, color):
        if(color != None and self.error != None):
            colored =  f"{color}{string}{self.reset_decorator}"
        else:
            colored = string
        return " "*self.indentation_level + colored