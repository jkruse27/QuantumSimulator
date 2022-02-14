import numpy as np

"""
Class for quantum circuit representation
"""

class QuantumCircuit():
    def __init__(self, qbits: int, cbits=0: int):
        self.operations = []
        self.qbits = qbits
        self.cbits = cbits

    def add_gate(self, gate: Gate):
        self.operations.append(gate)

    def draw(self):
        circuit = ''

        for op in operations:
            pass
