import more_itertools
import networkx as nx
import numpy as np
from quantum_simulator.circuit import gates
from quantum_simulator.circuit import Gate

"""
Class for quantum circuit representation
"""

class QuantumCircuit():
    def __init__(self, qbits: int, cbits: int = 0):
        self.operations = []
        self.qbits = qbits
        self.cbits = cbits
        self.dag = None

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

    def to_dag(self):
        self.dag = nx.DiGraph()

        edges = [['q_{}'.format(i)] for i in range(self.qbits)]

        count = 0
        for idx, op in enumerate(self.operations):
            qubits = op.get_qbits()
            name = '{}_{}'.format(op.get_name(), count)
            count += 1

            for i in qubits:
                edges[i].append(name)

        for i in range(self.qbits):
            edges[i].append('c_{}'.format(i))

        edges = [list(more_itertools.pairwise(line)) for line in edges] 
        edges = [item for sublist in edges for item in sublist]
        
        self.dag.add_edges_from(edges)
        return self.dag

    def draw_dag(self):
        nx.draw(self.dag, with_labels=True)
        plt.show()
