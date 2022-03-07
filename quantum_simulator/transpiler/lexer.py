import numpy as np
import ply.lex as lex
from rply import LexerGenerator
from quantum_simulator.circuit import QuantumCircuit

"""
Class for the conversion from QASM to Quantum Circuits
"""


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.add('QUBIT', r'qubit')
        self.lexer.add('SINGLE_GATE', r'[HXYZTS]{1}')
        self.lexer.add('DOUBLE_GATE', r'(CX|CZ|SWAP)')
        self.lexer.add('PARAMETRIC_GATE', r'U[123]{1}')
        self.lexer.add('NUMBER', r'[0-9]+(.[0-9]*)?')
        self.lexer.add('QREG_NAME', r'[a-zA-Z0-9\_]+(\[[0-9]+\])?')
        self.lexer.add('SEPARATOR', r',')
        self.lexer.add('START', r'^\s*' )
        self.lexer.add('END', r'\s*;')
        self.lexer.add('SPACE', r'\s+')
        self.lexer.add('NONE', '.+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
