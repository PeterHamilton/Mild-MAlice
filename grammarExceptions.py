class GrammarException(Exception):
    def __init__( self, lineno, clauseno ):
        self.lineno = lineno
        self.clauseno = clauseno
        
class SemanticException(GrammarException):
    def __init__( self, lineno, clauseno, value = "" ):
        super(SemanticException, self).__init__(lineno, clauseno)       
        self.value = "Oh No! Silly you!" + value
        
class SyntaxException(GrammarException):
    def __init__( self, lineno, clauseno, value = "" ):
        super(SyntaxException, self).__init__(lineno, clauseno)        
        self.value = "Oh No! You started writing utter nonsense." + value
       
class DivisionByZeroException(GrammarException):
    def __init__( self, lineno, clauseno, value = "" ):
        super(DivisionByZeroException, self).__init__(lineno, clauseno)       
        self.value = "Oops!" + value
    
class LexicalException(GrammarException):
    def __init__( self, lineno, clauseno, value = "" ):
        super(LexicalException, self).__init__(lineno, clauseno)       
        self.value = "Oh No! Silly you!"
       
class NoMatchException(GrammarException):
    def __init__( self, value = "" ):
        super(NoMatchException, self).__init__(0, 0)
        self.value = "Oh No! You were writing such silly things at the start of the story." + value
    
