import pytest
import numpy as np
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit

def test_bell_2q():
    """
    Test generation of bell state with 2 qubits
    """
    qc = QuantumCircuit(2)
    simulator = Simulator()

    qc.h(0)
    qc.cx(0,1)

    sv = simulator.get_statevector(qc)
    ans = np.array([0.70710678+0.j, 0, 0, 0.70710678+0.j])

    assert np.abs(np.linalg.norm(sv-ans)) <= 0.001

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
    ans = np.array([0.70710678+0.j, 0, 0, 0, 0, 0, 0, 0.70710678+0.j])

    assert abs(np.linalg.norm(sv-ans)) <= 0.001

def test_cx():
    """
    Tests cx aplication in systems with multiple qubits
    """
    qc = QuantumCircuit(5)
    simulator = Simulator()

    qc.h(4)
    qc.cx(4,2)

    sv = simulator.get_statevector(qc)

    ans = np.array([0.70710678+0.j, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0.70710678+0.j, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0])

    assert abs(np.linalg.norm(sv-ans)) <= 0.001
