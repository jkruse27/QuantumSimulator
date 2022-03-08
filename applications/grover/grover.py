import scipy.sparse as sparse
import numpy as np
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit

def superposition(n_qubits):
    qc = QuantumCircuit(n_qubits, n_qubits)

    for qubit in range(n_qubits):
        qc.h(qubit)

    return qc

def oracle(n_qubits, marked_state):
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    diagonal = np.ones(2**n_qubits)
    diagonal[marked_state] = -1

    unitary = sparse.diags(diagonal, format='dok')
    qc.unitary(list(range(n_qubits)), unitary)

    return qc
    
def diffuser(n_qubits):
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    qc.compose(superposition(n_qubits))

    diagonal = np.ones(2**n_qubits)
    diagonal[0] = -1

    unitary = sparse.diags(diagonal, format='dok')
    qc.unitary(list(range(n_qubits)), unitary)

    qc.compose(superposition(n_qubits))

    return qc

n = 7
searched_state = 43

qc = QuantumCircuit(n)
qc.compose(superposition(n))

repetitions = int(np.pi/4*np.sqrt(2**n))

for i in range(repetitions):
    qc.compose(oracle(n, searched_state))
    qc.compose(diffuser(n))

simulator = Simulator()

counts = simulator.simulate(qc, shots=8192)

max_key = max(counts, key=counts.get)

print("Estado encontrado: {}\nCerteza: {}\nResposta Correta: {}".format(
            int(max_key, 2),
            counts[max_key]/sum(counts.values()),
            searched_state
    ))
