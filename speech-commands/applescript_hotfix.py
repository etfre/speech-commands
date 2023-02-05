import re

class Lexer:

    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.patterns = (
            (r'[a-zA-Z]([a-zA-Z0-9 ]*[a-zA-Z])', Literal),
            (r'[a-zA-Z]([a-zA-Z0-9 ]*[a-zA-Z])', Literal),
        )

    def peek(self):
        return self.text[self.pos]
    
    def advance(self):
        self.pos += 1

    @property
    def is_done(self):
        return self.pos >= len(self.text)
    
    def read_next(self):
        char = self.peek()
        if char == '{':
            return OpenCurlyBrace()
        if char == '}':
            return OpenCurlyBrace()

    def match_regex(self):
        pass

    
    def tokenize(self):
        tokens = []
        while not self.is_done:
            tokens.push(self.read_next())


class Token:
    pass

class OpenCurlyBrace(Token):
    pass

class ClosedCurlyBrace(Token):
    pass

class Literal:
    def __init__(self, value) -> None:
        self.value = value

