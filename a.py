from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit
import scipy.sparse as sparse 
import scipy.sparse.linalg as linalg
import numpy as np
qc = QuantumCircuit(1)
simulator = Simulator()

qc.h(0)

a = simulator.simulate(qc,1000)
print(a)

