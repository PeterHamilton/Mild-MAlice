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
    ('right', 'INCREMENT', 'DECREMENT', 'B_NOT'),
    ('left', 'L_EQUALS', 'L_LESS_THAN', 'L_GREATER_THAN', 'L_GREATER_THAN_EQUAL', 'L_LESS_THAN_EQUAL', 'L_NOT_EQUAL', 'L_AND', 'L_OR')
)

def p_statement_list_statement(p):
    'statement_list : statement SEP_PERIOD'
    p[0] = p[1]

def p_statement_list_sep(p):
    '''statement_list   : statement SEP_AND statement_list
                        | statement SEP_BUT statement_list
                        | statement SEP_THEN statement_list
                        | statement SEP_COMMA statement_list
                        | statement SEP_PERIOD statement_list'''
    p[0] = ASTNodes.StatementListNode(p.lineno(1), p.clauseno(1), [p[1], p[3]])

def p_statement_print(p):
    '''statement    : expression PRINT_SPOKE
                    | expression PRINT_SAID ALICE'''
    p[0] = ASTNodes.SpokeNode(p.lineno(1), p.clauseno(1), p[1])

def p_statement_return(p):
    'statement    : expression RETURN_FOUND'
    # TODO: IMPLEMENT NODE

def p_statement_input(p):
    'statement : INPUT_WHAT ID'
    # TODO: IMPLEMENT NODE

def p_statement_comment(p):
    'statement : expression COMMENT_THOUGHT ALICE'
    # TODO: IMPLEMENT NODE

def p_statement_too(p):
    'statement : statement TOO'
    p[0] = p[1]

def p_statement_wasa(p):
    'statement : ID DEC_WAS DEC_A type'
    p[0] = ASTNodes.DeclarationNode(p.lineno(1), p.clauseno(1), p[1], p[4])

def p_statement_became(p):
    'statement : ID ASSIGNMENT expression'
    p[0] = ASTNodes.AssignmentNode(p.lineno(1), p.clauseno(1), p[1], p[3])

#TODO: SHOULD WE ONLY MATCH ON NUMBERS e.g "a has 'a' number" readable but catch later?
def p_statement_array_has(p):
    'statement : ID ARRAY_HAS expression type'
    # TODO: IMPLEMENT NODE

def p_expression_array_access(p):
    'expression : ID expression ARRAY_PIECE'
    # TODO: IMPLEMENT NODE

def p_statement_loop(p):
    'statement : LOOP_EVENTUALLY expression LOOP_BECAUSE statement_list LOOP_ENOUGH LOOP_TIMES'
    # TODO: IMPLEMENT NODE
    
def p_statement_if_perhaps(p):
    'statement    : IF_PERHAPS expression IF_SO statement_list ALICE DEC_WAS IF_UNSURE'
    # TODO: IMPLEMENT NODE
    
def p_statement_if_perhaps_multiple(p):
    'statement    : IF_PERHAPS expression IF_SO statement_list logical_clauses'
    # TODO: IMPLEMENT NODE

def p_statement_if_either(p):
    'statement    : IF_EITHER expression IF_SO statement_list IF_OR statement_list ALICE DEC_WAS IF_UNSURE IF_WHICH'
    # TODO: IMPLEMENT NODE

def p_logical_clauses(p):
    '''logical_clauses  : logical_clause logical_clauses
                        | ALICE DEC_WAS IF_UNSURE IF_WHICH'''
    # TODO: IMPLEMENT NODE

def p_logical_clause(p):
    '''logical_clause   : IF_OR IF_MAYBE expression IF_SO statement_list
                        | IF_OR statement_list'''
    # TODO: IMPLEMENT NODE

def p_statement_function(p):
    'statement : FUNCTION_THE FUNCTION_ROOM ID L_PAREN arguments R_PAREN FUNCTION_CONTAINED DEC_A type statement_list ALICE RETURN_FOUND expression'
    # TODO: IMPLEMENT NODE

def p_arguments(p):
    '''arguments    : argument SEP_COMMA arguments
                    | argument'''
    # TODO: IMPLEMENT NODE

def p_argument(p):
    'argument : type ID'
    # TODO: IMPLEMENT NODE
    
def p_statement_pbr_function(p):
    'statement : FUNCTION_THE FUNCTION_LOOKING_GLASS ID FUNCTION_CHANGED DEC_A type'
    # TODO: IMPLEMENT NODE
    
def p_statement_call_pbr_function(p):
    'statement : ID FUNCTION_WENT FUNCTION_THROUGH ID'
    # TODO: IMPLEMENT NODE
    
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

def p_expression_inc_dec(p):
    '''expression   : ID DECREMENT
                    | ID INCREMENT'''
    idNode = ASTNodes.IDNode(p.lineno(1), p.clauseno(1), p[1])
    p[0] = ASTNodes.UnaryNode(p.lineno(2), p.clauseno(2), p[2], idNode)

def p_expression_binary(p):
    '''expression   : expression B_OR expression
                    | expression B_XOR expression
                    | expression B_AND expression
                    | expression PLUS expression
                    | expression MINUS expression
                    | expression MULTIPLY expression'''
    p[0] = ASTNodes.BinaryNode(p.lineno(1), p.clauseno(1), p[2], [p[1],p[3]])

def p_expression_logical(p):
    '''expression   : expression L_EQUALS expression
                    | expression L_LESS_THAN expression
                    | expression L_GREATER_THAN expression
                    | expression L_GREATER_THAN_EQUAL expression
                    | expression L_LESS_THAN_EQUAL expression
                    | expression L_NOT_EQUAL expression
                    | expression L_AND expression
                    | expression L_OR expression'''

#TODO: MOVE THESE EXPRESSIONS INTO GENERAL BINARY EXPRESSION ABOVE AND MOVE
# DIV/0 CHECK INTO ASTNODE CHECK FUNCTION
def p_expression_divide(p):
    '''expression   : expression DIVIDE expression
                    | expression MOD expression'''
    if p[3].getValue() == 0:
        raise e.DivisionByZeroException(p.lineno(1), p.clauseno(1))
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
