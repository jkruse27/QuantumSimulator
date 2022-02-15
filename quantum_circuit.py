import numpy as np
import gates
from gates import Gate

"""
Class for quantum circuit representation
"""

class QuantumCircuit():
    def __init__(self, qbits: int, cbits: int = 0):
        self.operations = []
        self.qbits = qbits
        self.cbits = cbits

    def add_gate(self, gate: Gate):
        self.operations.append(gate)

    def x(self, qbit: int):
        self.operations.append(gates.X([qbit]))

    def y(self, qbit: int):
        self.operations.append(gates.Y([qbit]))

    def z(self, qbit: int):
        self.operations.append(gates.Z([qbit]))

    def h(self, qbit: int):
        self.operations.append(gates.H([qbit]))

    def t(self, qbit: int):
        self.operations.append(gates.T([qbit]))

    def s(self, qbit: int):
        self.operations.append(gates.S([qbit]))

    def cx(self, control: int, target: int):
        self.operations.append(gates.CX([control, target]))

    def swap(self, qbit1: int, qbit2: int):
        self.operations.append(gates.SWAP([qbit1, qbit2]))

    def cz(self, qbit1: int, qbit2: int):
        self.operations.append(gates.CZ([qbit1, qbit2]))

    def u1(self, qbit: int, lambda_: float):
        self.operations.append(gates.U1([qbit], lambda_))

    def u2(self, qbit: int, lambda_: float, phi: float):
        self.operations.append(gates.U2([qbit], lambda_, phi))

    def u3(self, qbit: int, lambda_: float, phi: float, theta: float):
        self.operations.append(gates.U3([qbit], lambda_, phi, theta))

    def get_number_of_qubits(self):
        return self.qbits

    def get_operations(self):
        return self.operations

    def draw(self):
        circuit = ''

        for op in operations:
            pass
