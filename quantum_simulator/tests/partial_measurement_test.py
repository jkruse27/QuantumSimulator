import pytest
import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit
"""
Automatic tests of partial measurements features
"""

def test_partial_measurement_1():
    """
    Tests measurements of a subset of qubits (1)
    """
    qc = QuantumCircuit(5)
    simulator = Simulator(seed=111)

    qc.h(4)
    qc.x(2)
    
    qc.measure([2,4])

    counts = simulator.simulate(qc, shots=10000)

    assert list(counts.keys())==['01', '11'] and \
           abs(counts['01']-counts['11'])/(counts['01']+counts['11']) <= 0.05

def test_partial_measurement_2():
    """
    Tests measurements of a subset of qubits (2)
    """
    qc = QuantumCircuit(3)
    simulator = Simulator(seed=111)

    qc.h(0)
    qc.measure([0])

    counts = simulator.simulate(qc, shots=10000)

    assert list(counts.keys())==['0', '1'] and \
            abs(counts['0']-counts['1'])/(counts['0']+counts['1']) <= 0.05

def test_partial_measurement_3():
    """
    Tests measurements of a subset of qubits (2)
    """
    qc = QuantumCircuit(2)
    simulator = Simulator(seed=111)

    qc.h(0)

    qc.measure([1])

    counts = simulator.simulate(qc, shots=10000)

    assert list(counts.keys())==['0']
