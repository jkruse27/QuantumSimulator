import pytest
import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit
"""
Automatic tests of simulation features
"""

def test_simulation_1():
    """
    Tests simulation of quantum circuits and shots (1)
    """
    qc = QuantumCircuit(2)
    simulator = Simulator(seed=111)

    qc.h(0)
    qc.cx(0,1)

    counts = simulator.simulate(qc, shots=10000)

    assert list(counts.keys())==['00', '11'] and \
            abs(counts['00']-counts['11'])/(counts['00']+counts['11']) <= 0.05

def test_simulation_2():
    """
    Tests simulation of quantum circuits and shots (2)
    """
    qc = QuantumCircuit(3)
    simulator = Simulator(seed=111)

    qc.h(0)
    qc.cx(0,1)
    qc.cx(0,2)

    counts = simulator.simulate(qc, shots=10000)

    assert list(counts.keys())==['000', '111'] and \
            abs(counts['000']-counts['111'])/(counts['000']+counts['111']) <= 0.05

def test_simulation_3():
    """
    Tests simulation of quantum circuits and shots (1)
    """
    qc = QuantumCircuit(5)
    simulator = Simulator(seed=111)

    qc.h(4)
    qc.cx(4,2)

    counts = simulator.simulate(qc, shots=10000)

    assert list(counts.keys())==['00000', '10100'] and \
           abs(counts['00000']-counts['10100'])/(counts['00000']+counts['10100']) <= 0.05

