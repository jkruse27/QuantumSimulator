import pytest
import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit
"""
Automatic tests of gate features
"""

def test_h():
    """
    Test generation of Hadamard Gate
    """
    qc = QuantumCircuit(1)
    simulator = Simulator()

    qc.h(0)

    sv = simulator.get_statevector(qc)
    ans = sparse.coo_matrix(np.array([0.70710678+0.j, 0.70710678+0.j])).todok().T

    assert np.abs(linalg.norm(sv-ans)) <= 0.001

def test_y():
    """
    Test generation of Y gate
    """
    qc = QuantumCircuit(1)
    simulator = Simulator()

    qc.h(0)
    qc.y(0)

    sv = simulator.get_statevector(qc)
    ans = sparse.coo_matrix(np.array([0.-0.70710678j, 0.+0.70710678j])).todok().T

    assert np.abs(linalg.norm(sv-ans)) <= 0.001

def test_x():
    """
    Test generation of Y gate
    """
    qc = QuantumCircuit(1)
    simulator = Simulator()

    qc.x(0)

    sv = simulator.get_statevector(qc)
    ans = sparse.coo_matrix(np.array([0, 1.+0.j])).todok().T

    assert np.abs(linalg.norm(sv-ans)) <= 0.001

def test_z():
    """
    Test generation of Y gate
    """
    qc = QuantumCircuit(1)
    simulator = Simulator()

    qc.h(0)
    qc.z(0)

    sv = simulator.get_statevector(qc)
    ans = sparse.coo_matrix([ 0.70710678+0.j, -0.70710678+0.j]).todok().T

    assert np.abs(linalg.norm(sv-ans)) <= 0.001
