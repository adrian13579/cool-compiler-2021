from lexing.utils import LexicographicError, set_pos

literals = [
    '+', '-', '*', '/', '~', '=', '<', ':', '{',
    '}', '@', ',', '.', '(', ')', ';', '$'
]
# keywords
reserved = {
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',
    'let': 'LET',
    'in': 'IN',
    'case': 'CASE',
    'of': 'OF',
    'esac': 'ESAC',
    'new': 'NEW',
    'isvoid': 'ISVOID',
    'not': 'NOT'
}

tokens = [
    'LESSEQ',
    'ASSIGN',
    'RET',
    'ID',
    'TYPE',
    'STRING',
    'INT',
    'COMMENT',
]
tokens = tokens + list(reserved.values())

states = (
    ('aux', 'exclusive'),
)


def t_LESSEQ(t):
    r'\<='
    set_pos(t)
    return t


def t_ASSIGN(t):
    r'\<-'
    set_pos(t)
    return t


def t_RET(t):
    r'\=>'
    set_pos(t)
    return t

def t_TYPE(t):
    r'[A-Z][a-zA-Z_0-9]*'
    set_pos(t)
    lower_case = t.value.lower()
    if lower_case in ('true', 'false'):
        t.type = 'TYPE'
        return t
    t.type = reserved.get(lower_case, 'TYPE')
    return t

def t_ID(t):
    r'[a-z_][a-zA-Z_0-9]*'
    set_pos(t)
    t.type = reserved.get(t.value.lower(), 'ID')
    return t


def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    set_pos(t)
    t.value = str(t.value)
    return t


def t_INT(t):
    r'\d+'
    set_pos(t)
    t.value = int(t.value)
    return t

# One-line comments rule


def t_COMMENT(t):
    r'(--.*(\n | $))'
    t.lexer.lineno += 1
    t.col = t.lexer.col
    t.lexer.col = 1
    # return t

# Multiline comments rules


def t_aux(t):
    r'\(\*'
    t.lexer.comm_start = t.lexer.lexpos - 2
    t.lexer.level = 1
    t.lexer.begin('aux')


def t_aux_lcomment(t):
    r'\(\*'
    t.lexer.level += 1


def t_aux_rcomment(t):
    r'\*\)'
    t.lexer.level -= 1
    if t.lexer.level == 0:
        t.value = t.lexer.lexdata[t.lexer.comm_start:t.lexer.lexpos]
        t.type = "COMMENT"
        t.lexer.lineno += t.value.count('\n')
        t.lexer.col = len(t.value) - t.value.rfind('\n')
        t.lexer.begin('INITIAL')
        # return t


def t_aux_pass(t):
    r'.|\n'
    pass

# Rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.col = 1


def t_WHITESPACE(t):
    r'\s'
    if t.value == '\t':
        t.lexer.col += 4
    else:
        t.lexer.col += len(t.value)


def t_plus(t):
    r'\+'
    t.type = '+'
    set_pos(t)
    return t


def t_minus(t):
    r'-'
    t.type = '-'
    set_pos(t)
    return t


def t_star(t):
    r'\*'
    t.type = '*'
    set_pos(t)
    return t


def t_slash(t):
    r'/'
    t.type = '/'
    set_pos(t)
    return t


def t_neg(t):
    r'~'
    t.type = '~'
    set_pos(t)
    return t


def t_equal(t):
    r'='
    t.type = '='
    set_pos(t)
    return t


def t_less(t):
    r'<'
    t.type = '<'
    set_pos(t)
    return t


def t_colon(t):
    r':'
    t.type = ':'
    set_pos(t)
    return t


def t_ocur(t):
    r'\{'
    t.type = '{'
    set_pos(t)
    return t


def t_ccur(t):
    r'\}'
    t.type = '}'
    set_pos(t)
    return t


def t_at(t):
    r'@'
    t.type = '@'
    set_pos(t)
    return t


def t_comma(t):
    r','
    t.type = ','
    set_pos(t)
    return t


def t_dot(t):
    r'\.'
    t.type = '.'
    set_pos(t)
    return t


def t_opar(t):
    r'\('
    t.type = '('
    set_pos(t)
    return t


def t_cpar(t):
    r'\)'
    t.type = ')'
    set_pos(t)
    return t


def t_semicolon(t):
    r';'
    t.type = ';'
    set_pos(t)
    return t


def t_dollar(t):
    r'\$'
    t.type = '$'
    set_pos(t)
    return t

# Error handling rule


def t_ANY_error(t):
    set_pos(t)
    t.lexer.errors.append(LexicographicError(t.lineno, t.col, t.value[0]))
    t.lexer.skip(1)


# TODO: Handle errors inside comments (unbalanced multiline comments delimeters)