from simulator import Simulator
from quantum_circuit import QuantumCircuit

qc = QuantumCircuit(2)
simulator = Simulator()

qc.h(0)
qc.cx(0,1)

print(simulator.simulate(qc).real)

qc = QuantumCircuit(3)
simulator = Simulator()

qc.h(0)
qc.cx(0,2)

print(simulator.simulate(qc).real)

qc = QuantumCircuit(3)
simulator = Simulator()

qc.h(0)
qc.cx(0,1)
qc.cx(0,2)

print(simulator.simulate(qc).real)
