"""
Quantum System Simulator
"""

import numpy as np
import random
from quantum_simulator.circuit import QuantumCircuit

class Simulator():
    def get_statevector(self, qc: QuantumCircuit):
        """
        Method that find the resulting statevector from a quantum circuit and returns it.
        """
        n_qbits = qc.get_number_of_qubits()
        initial_state = np.zeros(2**n_qbits, dtype="complex128")
        initial_state[0] = 1

        for op in qc.get_operations():
            initial_state = np.dot(op.get_circuit_unitary(n_qbits),initial_state)

        return initial_state

    def simulate(self, qc: QuantumCircuit, shots: int=1024, seed: int=124):
        """
        Method that simulates measurements given a circuit and a number of shots. Returns a dictionary
        with counts of the measured states.
        """
        np.random.seed(seed)
        statevector = self.get_statevector(qc)
        sum_probabilities = np.cumsum(np.multiply(statevector.conjugate(),statevector))

        #output_counts = {}

        random_numbers = np.random.rand(shots)
        values = [next(x for x, val in enumerate(sum_probabilities) if val > n) for n in random_numbers]
        output_counts = {index: values.count(index) for index in set(values)}

        #for i in range(shots):
        #    random_number = random.random()
        #    value = next(x for x, val in enumerate(sum_probabilities)
        #                               if val > random_number) 

        #    output_counts[value] = output_counts.get(value, 0) + 1

        keys = list(output_counts.keys())

        for key in keys:
            output_counts[format(key, '0{}b'.format(qc.get_number_of_qubits()))] = output_counts.pop(key)

        return output_counts


