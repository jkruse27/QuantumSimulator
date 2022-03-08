from pathlib import Path
import sys
path = str(Path(Path(Path(__file__).parent.absolute()).parent.absolute().parent.absolute()))
sys.path.insert(0, path)

import scipy.sparse as sparse
import numpy as np
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit


