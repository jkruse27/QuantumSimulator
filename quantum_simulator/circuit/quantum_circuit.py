import more_itertools
import networkx as nx
import numpy as np
import scipy.sparse as sparse
from quantum_simulator.representations import Unitary
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
        self.measured = 0

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

    def cu1(self, control: int, target: int, lambda_: float):
        self.operations.append(gates.CU1([control, target], lambda_))

    def unitary(self, qbits: list[int], unitary: Unitary):
        self.operations.append(gates.UnitaryGate(unitary, qbits))

    def controlled_unitary(self, control: int, targets: list[int], unitary: sparse.dok_matrix):
        self.operations.append(gates.ControlledUnitary(unitary, [control]+targets))

    def measure(self, qbits: list[int]):
        self.measured = len(qbits)
        self.operations.append(gates.Measurement(qbits))

    def get_measured_qubits(self):
        return self.measured if self.measured != 0 else self.qbits

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

    def compose(self, qc):
        if(self.qbits == qc.get_number_of_qubits()):
            self.operations += qc.get_operations()

    def draw_dag(self):
        nx.draw(self.dag, with_labels=True)
        plt.show()

    def to_unitary(self):
        unitary = self.operations[0].get_circuit_unitary(self.qbits)
    
        for op in self.operations[1:]:
            unitary = op.get_circuit_unitary(self.qbits).dot(unitary)

        return unitary

