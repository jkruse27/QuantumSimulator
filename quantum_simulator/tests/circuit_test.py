import pytest
import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit
"""
Automatic tests of quantum circuit features
"""

def test_bell_2q():
    """
    Test generation of bell state with 2 qubits
    """
    qc = QuantumCircuit(2)
    simulator = Simulator()

    qc.h(0)
    qc.cx(0,1)

    sv = simulator.get_statevector(qc)
    ans = sparse.coo_matrix([0.70710678+0.j, 0, 0, 0.70710678+0.j]).todok().T

    assert np.abs(linalg.norm(sv-ans)) <= 0.001

def test_bell_3q():
    """
    Test generation of bell state with 3 qubits
    """
    qc = QuantumCircuit(3)
    simulator = Simulator()

    qc.h(0)
    qc.cx(0,1)
    qc.cx(0,2)

    sv = simulator.get_statevector(qc)
    ans = sparse.coo_matrix([0.70710678+0.j, 0, 0, 0, 0, 0, 0, 0.70710678+0.j]).todok().T

    assert abs(linalg.norm(sv-ans)) <= 0.001
