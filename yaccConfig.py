# This file contains the BNF rules for MAlice.

import ASTNodes
from tokRules import tokens
import grammarExceptions as e

start = 'statement_list'

precedence = (
    ('left', 'B_OR'),
    ('left', 'B_XOR'),
    ('left', 'B_AND'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MOD'),
    ('right','INCREMENT', 'DECREMENT', 'B_NOT'),
)

def p_statement_list_sep_comma(p):
    'statement_list : statement SEP_COMMA statement_list'
    p[0] = ASTNodes.StatementListNode(p.lineno(1), p.clauseno(1), [p[1], p[3]])

def p_statement_list_sep_period(p):
    'statement_list : statement SEP_PERIOD statement_list'
    p[0] = ASTNodes.StatementListNode(p.lineno(1), p.clauseno(1), [p[1], p[3]])

def p_statement_list_statement(p):
    'statement_list : statement SEP_PERIOD'
    p[0] = p[1]

def p_statement_list_sep_and(p):
    'statement_list : statement SEP_AND statement_list'
    p[0] = ASTNodes.StatementListNode(p.lineno(1), p.clauseno(1), [p[1], p[3]])

def p_statement_list_sep_but(p):
    'statement_list : statement SEP_BUT statement_list'
    p[0] = ASTNodes.StatementListNode(p.lineno(1), p.clauseno(1), [p[1], p[3]])

def p_statement_list_sep_then(p):
    'statement_list : statement SEP_THEN statement_list'
    p[0] = ASTNodes.StatementListNode(p.lineno(1), p.clauseno(1), [p[1], p[3]])

def p_statement_alicespoke(p):
    'statement : expression PRINT_SPOKE'
    p[0] = ASTNodes.SpokeNode(p.lineno(1), p.clauseno(1), p[1])

def p_statement_too(p):
    'statement : statement TOO'
    p[0] = p[1]

def p_statement_wasa(p):
    'statement : ID DEC_WAS DEC_A type'
    p[0] = ASTNodes.DeclarationNode(p.lineno(1), p.clauseno(1), [p[1], p[4]])

def p_statement_became(p):
    'statement : ID ASSIGNMENT expression'
    p[0] = ASTNodes.AssignmentNode(p.lineno(1), p.clauseno(1), [p[1], p[3]])

def p_statement_expression(p):
    'statement : expression'
    p[0] = p[1]

def p_type_number(p):
    'type : TYPE_NUMBER'
    p[0] = ASTNodes.NumberTypeNode(p.lineno(1), p.clauseno(1))

def p_type_letter(p):
    'type : TYPE_LETTER'
    p[0] = ASTNodes.LetterTypeNode(p.lineno(1), p.clauseno(1))

def p_expression_not(p):
    'expression : B_NOT expression'
    p[0] = ASTNodes.UnaryNode(p.lineno(2), p.clauseno(2), p[1], p[2])

def p_expression_drank(p):
    'expression : ID DECREMENT'
    idNode = ASTNodes.IDNode(p.lineno(1), p.clauseno(1), p[1])
    p[0] = ASTNodes.UnaryNode(p.lineno(2), p.clauseno(2), p[2], idNode)

def p_expression_ate(p):
    'expression : ID INCREMENT'
    idNode = ASTNodes.IDNode(p.lineno(1), p.clauseno(1), p[1])
    p[0] = ASTNodes.UnaryNode(p.lineno(2), p.clauseno(2), p[2], idNode)

def p_expression_or(p):
    'expression : expression B_OR expression'
    p[0] = ASTNodes.BinaryNode(p.lineno(1), p.clauseno(1), p[2], [p[1],p[3]])

def p_expression_xor(p):
    'expression : expression B_XOR expression'
    p[0] = ASTNodes.BinaryNode(p.lineno(1), p.clauseno(1), p[2], [p[1],p[3]])

def p_expression_and(p):
    'expression : expression B_AND expression'
    p[0] = ASTNodes.BinaryNode(p.lineno(1), p.clauseno(1), p[2], [p[1],p[3]])
    
def p_expression_plus(p):
    'expression : expression PLUS expression'
    p[0] = ASTNodes.BinaryNode(p.lineno(1), p.clauseno(1), p[2], [p[1],p[3]])

def p_expression_minus(p):
    'expression : expression MINUS expression'
    p[0] = ASTNodes.BinaryNode(p.lineno(1), p.clauseno(1), p[2], [p[1],p[3]])

def p_expression_multiply(p):
    'expression : expression MULTIPLY expression'
    p[0] = ASTNodes.BinaryNode(p.lineno(1), p.clauseno(1), p[2], [p[1],p[3]])

#Handles division by 0 constant
def p_expression_divide(p):
    'expression : expression DIVIDE expression'
    if p[3].getValue() == 0:
        raise e.DivisionByZeroException(p.lineno(1), p.clauseno(1))
    p[0] = ASTNodes.BinaryNode(p.lineno(1), p.clauseno(1), p[2], [p[1],p[3]])

def p_expression_mod(p):
    'expression : expression MOD expression'
    p[0] = ASTNodes.BinaryNode(p.lineno(1), p.clauseno(1), p[2], [p[1],p[3]])

def p_expression_factor(p):
    'expression : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = ASTNodes.NumberNode(p.lineno(1), p.clauseno(1), p[1])

def p_factor_letter(p):
    'factor : LETTER'
    p[0] = ASTNodes.LetterNode(p.lineno(1), p.clauseno(1), p[1])

def p_factor_id(p):
    'factor : ID'
    p[0] = ASTNodes.IDNode(p.lineno(1), p.clauseno(1), p[1])
    
def p_error(p):
    if p == None:
        raise e.NoMatchException()
    else:
        raise e.SyntaxException(p.lineno, p.clauseno)
