from simulator import Simulator
from quantum_circuit import QuantumCircuit

qc = QuantumCircuit(2)
simulator = Simulator()

qc.h(0)
qc.cx(0,1)

print(simulator.get_statevector(qc).real)
print(simulator.simulate(qc, shots=2048))

qc = QuantumCircuit(3)
simulator = Simulator()

qc.h(0)
qc.cx(0,2)

print(simulator.get_statevector(qc).real)
print(simulator.simulate(qc))

qc = QuantumCircuit(3)
simulator = Simulator()

qc.h(0)
qc.cx(0,1)
qc.cx(0,2)

print(simulator.get_statevector(qc).real)
print(simulator.simulate(qc))
