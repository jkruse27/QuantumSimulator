"""
Quantum System Simulator
"""

import random
import numpy as np
import scipy.sparse as sparse
from quantum_simulator.representations import Unitary, Statevector
from quantum_simulator.circuit import QuantumCircuit

class Simulator():
    def __init__(self, seed: int=42):
        np.random.seed(seed) 

    def get_statevector(self, qc: QuantumCircuit):
        """
        Method that find the resulting statevector from a quantum circuit and returns it.
        """
        n_qbits = qc.get_number_of_qubits()
        initial_state = Statevector.get_statevector((2**n_qbits,1))

        for op in qc.get_operations():
            if(op.get_name() == 'MEASUREMENT'):
                initial_state = Statevector.measure_superposition(initial_state, n_qbits, op.get_qbits(n_qbits))
                break
            else:
                initial_state = Statevector.evolve(initial_state, op.get_circuit_unitary(n_qbits))

        return initial_state

    def simulate(self, qc: QuantumCircuit, shots: int=1024):
        """
        Method that simulates measurements given a circuit and a number of shots. Returns a dictionary
        with counts of the measured states.
        """
        statevector = self.get_statevector(qc)
        sum_probabilities = Statevector.get_summed_probabilities(statevector)

        random_numbers = np.random.rand(shots)
        values = [next(x for x, val in enumerate(sum_probabilities) if val > n) for n in random_numbers]
        output_counts = {index: values.count(index) for index in set(values)}

        keys = list(output_counts.keys())

        for key in keys:
            output_counts[format(key, '0{}b'.format(qc.get_measured_qubits()))] = output_counts.pop(key)

        return output_counts
