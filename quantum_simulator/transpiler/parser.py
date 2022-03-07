from rply import ParserGenerator
from quantum_simulator.transpiler import Lexer

pg = ParserGenerator(
    ['QUBIT', 'SINGLE_GATE', 'DOUBLE_GATE',
     'PARAMETRIC_GATE', 'NUMBER', 'QREG_NAME', 'SEPARATOR',
     'START', 'END', 'SPACE', 'NONE',
    ]
)

@pg.production('qubit : START QUBIT SPACE QREG_NAME END')
def start_register(p):
    print(p[3])

@pg.production('single : START SINGLE_GATE SPACE QREG_NAME END')
def single_gate(p):
    print(p[1])

@pg.production('double : START DOUBLE_GATE SPACE QREG_NAME SEPARATOR QREG_NAME END')
def double_gate(p):
    print(p[1])

@pg.production('parametric1 : START PARAMETRIC_GATE SPACE QREG_NAME END')
def param1_gate(p):
    print(p[1])

@pg.production('parametric2 : START PARAMETRIC_GATE SPACE QREG_NAME SEPARATOR QREG_NAME END')
def param2_gate(p):
    print(p[1])

@pg.production('parametric3 : START PARAMETRIC_GATE SPACE QREG_NAME SEPARATOR QREG_NAME SEPARATOR QREG_NAME END')
def param3_gate(p):
    print(p[1])

@pg.production('parametric3 : START PARAMETRIC_GATE SPACE QREG_NAME SEPARATOR QREG_NAME SEPARATOR QREG_NAME END')
def param3_gate(p):
    print(p[1])
parser = pg.build()

a = """
qubit a[2];
qubit b;

H a[1];
CX a[1], b;
"""

lexer = Lexer().get_lexer()
parser.parse(lexer.lex(a))
