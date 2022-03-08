import pytest
import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit
"""
Automatic tests of full measurements features
"""

def test_full_measurement_1():
    """
    Tests measurements of all qubits (1)
    """
    qc = QuantumCircuit(5)
    simulator = Simulator()

    qc.h(4)
    qc.cx(4,2)
    
    qc.measure(range(5))

    counts = simulator.simulate(qc, shots=10000, seed=111)

    assert list(counts.keys())==['00000', '10100'] and \
           abs(counts['00000']-counts['10100'])/(counts['00000']+counts['10100']) <= 0.05

def test_full_measurement_2():
    """
    Tests measurements of all qubits (2)
    """
    qc = QuantumCircuit(3)
    simulator = Simulator()

    qc.h(0)
    qc.cx(0,1)
    qc.cx(0,2)

    qc.measure(range(3))

    counts = simulator.simulate(qc, shots=10000, seed=111)

    assert list(counts.keys())==['000', '111'] and \
            abs(counts['000']-counts['111'])/(counts['000']+counts['111']) <= 0.05

def test_full_measurement_3():
    """
    Tests measurements of all qubits (3)
    """
    qc = QuantumCircuit(2)
    simulator = Simulator()

    qc.h(0)
    qc.cx(0,1)

    qc.measure(range(2))

    counts = simulator.simulate(qc, shots=10000, seed=111)

    assert list(counts.keys())==['00', '11'] and \
            abs(counts['00']-counts['11'])/(counts['00']+counts['11']) <= 0.05
