"""
Quantum System Simulator
"""

import numpy as np
import quantum_circuit
import random

class Simulator():
    def get_statevector(self, qc):
        n_qbits = qc.get_number_of_qubits()
        initial_state = np.zeros(2**n_qbits, dtype="complex128")
        initial_state[0] = 1

        for op in qc.get_operations():
            initial_state = np.dot(op.get_circuit_unitary(n_qbits),initial_state)

        return initial_state

    def simulate(self, qc, shots=1024, seed=124):
        random.seed(seed)
        statevector = self.get_statevector(qc)
        sum_probabilities = np.cumsum(np.square(statevector))

        output_counts = {}

        for i in range(shots):
            random_number = random.random()
            value = next(x for x, val in enumerate(sum_probabilities)
                                        if val > random_number) 

            output_counts[value] = output_counts.get(value, 0) + 1

        keys = list(output_counts.keys())

        for key in keys:
            output_counts[format(key, '0{}b'.format(qc.get_number_of_qubits()))] = output_counts.pop(key)

        return output_counts


