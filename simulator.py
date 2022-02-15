"""
Quantum System Simulator
"""

import numpy as np
import quantum_circuit

class Simulator():
    def simulate(self, qc):
        n_qbits = qc.get_number_of_qubits()
        initial_state = np.zeros(2**n_qbits, dtype="complex128")
        initial_state[0] = 1

        for op in qc.get_operations():
            initial_state = np.dot(op.get_circuit_unitary(n_qbits),initial_state)

        return initial_state
