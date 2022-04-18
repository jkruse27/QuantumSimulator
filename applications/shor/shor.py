from pathlib import Path
import sys
path = str(Path(Path(Path(__file__).parent.absolute()).parent.absolute().parent.absolute()))
sys.path.insert(0, path)

import scipy.sparse as sparse
import numpy as np
from fractions import Fraction
from math import gcd
from quantum_simulator.simulator import Simulator
from quantum_simulator.circuit import QuantumCircuit

def initialize(l, m):
    n = l+m
    qc = QuantumCircuit(n)
    for qubit in range(l):
        qc.h(qubit)
    qc.x(l+m-1)
    
    return qc

def iqft(l):
    qc = QuantumCircuit(l)

    for i in range(int(l/2)):
        qc.swap(i, l-i-1)

    for i in range(l):
        qc.h(i)
        for j in range(i+1, l):
            qc.cu1(i, j, -np.pi/(2**(j-i)))
    
    return qc

def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2,7,8,11,13]:
        raise ValueError("'a' must be 2,7,8,11 or 13")

    U = QuantumCircuit(4)        
    for iteration in range(power):
        if a in [2,13]:
            U.swap(0,1)
            U.swap(1,2)
            U.swap(2,3)
        if a in [7,8]:
            U.swap(2,3)
            U.swap(1,2)
            U.swap(0,1)
        if a == 11:
            U.swap(1,3)
            U.swap(0,2)
        if a in [7,11,13]:
            for q in range(4):
                U.x(q)

    unitary = U.to_unitary()

    return unitary

def qpe_amod15(a):
    l = 3
    m = 4

    qc = initialize(l,m)

    for i, j in enumerate(list(range(l))[::-1]):
        qc.controlled_unitary(j, list(range(l,l+m)), c_amod15(a, 2**i))

    qc.compose(iqft(l))
    qc.measure(list(range(l)))
    
    simulator = Simulator()
    counts = simulator.simulate(qc, shots=1)
    readings = list(counts.keys()) 
    phase = int(readings[0],2)/(2**l)

    return phase

N = 15
a = 7
factor_found = False
attempt = 0
while not factor_found:
    attempt += 1
    print("\nAttempt %i:" % attempt)
    phase = qpe_amod15(a) # Phase = s/r
    frac = Fraction(phase).limit_denominator(N) # Denominator should (hopefully!) tell us r
    r = frac.denominator
    print("Result: r = %i" % r)
    if phase != 0:
        # Guesses for factors are gcd(x^{r/2} ±1 , 15)
        guesses = [gcd(a**(r//2)-1, N), gcd(a**(r//2)+1, N)]
        print("Guessed Factors: %i and %i" % (guesses[0], guesses[1]))
        for guess in guesses:
            if guess not in [1,N] and (N % guess) == 0: # Check to see if guess is a factor
                print("*** Non-trivial factor found: %i ***" % guess)
                factor_found = True
