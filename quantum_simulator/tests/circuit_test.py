import pytest
import numpy as np
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit
"""
Automatic tests of the implemented features
"""

def test_h():
    """
    Test generation of Hadamard Gate
    """
    qc = QuantumCircuit(1)
    simulator = Simulator()

    qc.h(0)

    sv = simulator.get_statevector(qc)
    ans = np.array([0.70710678+0.j, 0.70710678+0.j])

    assert np.abs(np.linalg.norm(sv-ans)) <= 0.001

def test_y():
    """
    Test generation of Y gate
    """
    qc = QuantumCircuit(1)
    simulator = Simulator()

    qc.h(0)
    qc.y(0)

    sv = simulator.get_statevector(qc)
    ans = np.array([0.-0.70710678j, 0.+0.70710678j])

    assert np.abs(np.linalg.norm(sv-ans)) <= 0.001

def test_x():
    """
    Test generation of Y gate
    """
    qc = QuantumCircuit(1)
    simulator = Simulator()

    qc.x(0)

    sv = simulator.get_statevector(qc)
    ans = np.array([0, 1.+0.j])

    assert np.abs(np.linalg.norm(sv-ans)) <= 0.001

def test_z():
    """
    Test generation of Y gate
    """
    qc = QuantumCircuit(1)
    simulator = Simulator()

    qc.h(0)
    qc.z(0)

    sv = simulator.get_statevector(qc)
    ans = np.array([ 0.70710678+0.j, -0.70710678+0.j])

    assert np.abs(np.linalg.norm(sv-ans)) <= 0.001

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
    Tests Controlled NOT aplication in systems with multiple qubits
    """
    qc = QuantumCircuit(5)
    simulator = Simulator()

    qc.h(4)
    qc.cx(4,2)

    sv = simulator.get_statevector(qc)
    print(sv)

    ans = np.array([0.70710678+0.j, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0.70710678+0.j, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0])

    assert abs(np.linalg.norm(sv-ans)) <= 0.001

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

    ans = np.array([ 0.5+0.j,  0,  0,  0,  0.5+0.j,  0, 0,  0,  0,  0,  0,  0,
                     0, 0,  0,  0,  0.5+0.j,  0, 0,  0, -0.5+0.j,  0,  0,  0,
                     0, 0, 0, 0, 0, 0, 0, 0]
            )

    assert abs(np.linalg.norm(sv-ans)) <= 0.001

def test_simulation_1():
    """
    Tests simulation of quantum circuits and shots (1)
    """
    qc = QuantumCircuit(2)
    simulator = Simulator()

    qc.h(0)
    qc.cx(0,1)

    counts = simulator.simulate(qc, shots=10000, seed=111)

    assert list(counts.keys())==['00', '11'] and \
            abs(counts['00']-counts['11'])/(counts['00']+counts['11']) <= 0.05

def test_simulation_2():
    """
    Tests simulation of quantum circuits and shots (2)
    """
    qc = QuantumCircuit(3)
    simulator = Simulator()

    qc.h(0)
    qc.cx(0,1)
    qc.cx(0,2)

    counts = simulator.simulate(qc, shots=10000, seed=111)

    assert list(counts.keys())==['000', '111'] and \
            abs(counts['000']-counts['111'])/(counts['000']+counts['111']) <= 0.05

def test_simulation_3():
    """
    Tests simulation of quantum circuits and shots (1)
    """
    qc = QuantumCircuit(5)
    simulator = Simulator()

    qc.h(4)
    qc.cx(4,2)

    counts = simulator.simulate(qc, shots=10000, seed=111)

    assert list(counts.keys())==['00000', '10100'] and \
           abs(counts['00000']-counts['10100'])/(counts['00000']+counts['10100']) <= 0.05
