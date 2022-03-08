import pytest
import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit
"""
Automatic tests of controlled gate features
"""

def test_cx():
    """
    Tests Controlled NOT aplication in systems with multiple qubits
    """
    qc = QuantumCircuit(5)
    simulator = Simulator()

    qc.h(4)
    qc.cx(4,2)

    sv = simulator.get_statevector(qc)
    print(sv)

    ans = sparse.coo_matrix([0.70710678+0.j, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0.70710678+0.j, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0]).todok().T

    assert abs(linalg.norm(sv-ans)) <= 0.001

def test_cz():
    """
    Tests Controlled PHASE aplication in systems with multiple qubits
    """
    qc = QuantumCircuit(5)
    simulator = Simulator()

    qc.h(4)
    qc.h(2)
    qc.cz(4,2)

    sv = simulator.get_statevector(qc)
    print(sv)

    ans = sparse.coo_matrix([0.5+0.j,  0,  0,  0,  0.5+0.j,  0, 0,  0,  0,  0,  0,  0,
                     0, 0,  0,  0,  0.5+0.j,  0, 0,  0, -0.5+0.j,  0,  0,  0,
                     0, 0, 0, 0, 0, 0, 0, 0]
            ).todok().T

    assert abs(linalg.norm(sv-ans)) <= 0.001
