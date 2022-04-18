import itertools
import functools as ft
import numpy as np
import scipy.sparse as sparse
from quantum_simulator.utils import isconsecutive
from quantum_simulator.representations import Unitary

"""
Quantum Gates
"""

ket_zero = Unitary.get_unitary([[1], [0]])
ket_one  = Unitary.get_unitary([[0], [1]]) 

class Gate:
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = ''
        self.unitary = None
        self.qbits = None
        self.cbits = None

    def get_unitary(self) -> sparse.dok_matrix:
        return self.unitary

    def get_circuit_unitary(self, n_qbits: int) -> sparse.dok_matrix:
        identity = I([],[]).get_unitary()
        unitary  = self.unitary
        
        operations = [identity]*n_qbits
        operations[self.qbits[0]] = unitary

        return Unitary.reduce_kron(operations[::-1])

    def get_qbits(self) -> sparse.dok_matrix:
        return self.qbits

    def get_cbits(self) -> sparse.dok_matrix:
        return self.cbits

    def get_name(self) -> str:
        return self.name

class UnitaryGate(Gate):
    def __init__(self, unitary: sparse.dok_matrix, qbits: list[int], cbits: list[int] = None, **kwargs):
        if(not isconsecutive(qbits)):
            raise Exception("The qubits must be consecutives") 
        
        self.name = 'Unitary'
        self.unitary = unitary

        self.qbits = qbits
        self.cbits = cbits

    def get_circuit_unitary(self, n_qbits: int) -> sparse.dok_matrix:
        if(n_qbits < len(self.qbits)):
            raise Exception("Unitary's size is incompatible with the system") 

        identity = I([],[]).get_unitary()
        unitary  = self.unitary

        operations = [identity]*(n_qbits-len(self.qbits)+1)
        operations[self.qbits[0]] = unitary

        return Unitary.reduce_kron(operations[::-1])
        
class ControlledUnitary(Gate):
    def __init__(self, unitary: sparse.dok_matrix, qbits: list[int], cbits: list[int] = None, **kwargs):
        if(not isconsecutive(qbits[1:])):
            raise Exception("The qubits must be consecutives") 
        
        self.name = 'CUnitary'
        self.unitary = unitary
        self.qbits = qbits
        self.cbits = cbits

    def get_circuit_unitary(self, n_qbits: int) -> sparse.dok_matrix:
        if(n_qbits < len(self.qbits)):
            raise Exception("Unitary's size is incompatible with the system") 

        identity = I([],[]).get_unitary()
        unitary  = self.unitary
       
        operations_zero = [identity]*n_qbits
        operations_zero[self.qbits[0]] = Unitary.mul(ket_zero,ket_zero.T)
        
        operations_one = [identity]*(n_qbits-len(self.qbits)+2)
        operations_one[self.qbits[0]] = Unitary.mul(ket_one,ket_one.T)
        operations_one[self.qbits[1]] = unitary

        return Unitary.reduce_kron(operations_zero[::-1]) + \
               Unitary.reduce_kron(operations_one[::-1])


class I(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'I'
        self.unitary = Unitary.get_unitary([[1, 0],
                                            [0, 1]])
        self.qbits = qbits
        self.cbits = cbits

class H(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'H'
        self.unitary = (1/np.sqrt(2))*Unitary.get_unitary([[1, 1],
                                                           [1,-1]])
        self.qbits = qbits
        self.cbits = cbits
    
class X(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'X'
        self.unitary = Unitary.get_unitary([[0, 1],
                                            [1, 0]])
        self.qbits = qbits
        self.cbits = cbits

class Y(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'Y'
        self.unitary = Unitary.get_unitary([[0,  -1.j],
                                            [1.j,  0]])
        self.qbits = qbits
        self.cbits = cbits

class Z(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'Z'
        self.unitary = Unitary.get_unitary([[1,  0],
                                            [0, -1]])
        self.qbits = qbits
        self.cbits = cbits

class S(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'S'
        self.unitary = Unitary.get_unitary([[1,  0],
                                            [0, 1.j]])
        self.qbits = qbits
        self.cbits = cbits

class T(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'T'
        self.unitary = Unitary.get_unitary([[1,  0],
                                            [0, np.exp(1.j*np.pi/4)]])
        self.qbits = qbits
        self.cbits = cbits

class U1(Gate):
    def __init__(self, qbits: list[int], lambda_: float, cbits: list[int] = None, **kwargs):
        self.name = 'U1'
        self.lambda_ = lambda_
        self.unitary = Unitary.get_unitary([[1,  0],
                                            [0, np.exp(1.j*self.lambda_)]])
        self.qbits = qbits
        self.cbits = cbits

class U2(Gate):
    def __init__(self, qbits: list[int], lambda_: float, phi: float, cbits: list[int] = None, **kwargs):
        self.name = 'U2'
        self.lambda_ = lambda_
        self.phi = phi
        self.unitary = (1/np.sqrt(2))*Unitary.get_unitary([[1,                   -np.exp(1.j*self.lambda_)],
                                                           [np.exp(1.j*self.phi), np.exp(1.j*(self.phi+self.lambda_))]])
        self.qbits = qbits
        self.cbits = cbits

class U3(Gate):
    def __init__(self, qbits: list[int], lambda_: float, phi: float, theta: float, cbits: list[int] = None, **kwargs):
        self.name = 'U3'
        self.lambda_ = lambda_
        self.phi = phi
        self.theta = theta
        self.unitary = Unitary.get_unitary([[np.cos(self.theta/2),  -np.exp(1.j*self.lambda_)*np.sin(self.theta/2)],
                                            [np.exp(1.j*self.phi)*np.sin(self.theta/2), np.exp(1.j*(self.phi+self.lambda_))*np.cos(self.theta/2)]])
        self.qbits = qbits
        self.cbits = cbits

class CU1(Gate):
    def __init__(self, qbits: list[int], lambda_: float, cbits: list[int] = None, **kwargs):
        self.name = 'CU1'
        self.lambda_ = lambda_
        self.unitary = Unitary.get_unitary([[1,  0],
                                            [0, np.exp(1.j*self.lambda_)]])
        self.qbits = qbits
        self.cbits = cbits

    def get_circuit_unitary(self, n_qbits: int) -> sparse.dok_matrix:
        identity = I([],[]).get_unitary()
        unitary  = self.get_unitary()
        
        operations_zero = [identity]*n_qbits
        operations_zero[self.qbits[0]] = Unitary.mul(ket_zero,ket_zero.T)
        
        operations_one = [identity]*n_qbits
        operations_one[self.qbits[0]] = Unitary.mul(ket_one,ket_one.T)
        operations_one[self.qbits[1]] = unitary

        return Unitary.reduce_kron(operations_zero[::-1]) + \
               Unitary.reduce_kron(operations_one[::-1])

class CX(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'CX'
        self.unitary = Unitary.get_unitary([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 0, 1],
                                            [0, 0, 1, 0]])
        self.qbits = qbits
        self.cbits = cbits

    def get_circuit_unitary(self, n_qbits: int) -> sparse.dok_matrix:
        identity = I([],[]).get_unitary()
        unitary  = X([],[]).get_unitary()
        
        operations_zero = [identity]*n_qbits
        operations_zero[self.qbits[0]] = Unitary.mul(ket_zero,ket_zero.T)
        
        operations_one = [identity]*n_qbits
        operations_one[self.qbits[0]] = Unitary.mul(ket_one,ket_one.T)
        operations_one[self.qbits[1]] = unitary

        return Unitary.reduce_kron(operations_zero[::-1]) + \
               Unitary.reduce_kron(operations_one[::-1])

class SWAP(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'SWAP'
        self.unitary = Unitary.get_unitary([[1, 0, 0, 0],
                                            [0, 0, 1, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 0, 1]])
        self.qbits = qbits
        self.cbits = cbits

    def get_circuit_unitary(self, n_qbits: int) -> sparse.dok_matrix:
        cx_12 = CX(self.qbits)
        cx_21 = CX(self.qbits[::-1])

        cx_12 = cx_12.get_circuit_unitary(n_qbits)
        cx_21 = cx_21.get_circuit_unitary(n_qbits)

        return cx_12.dot(cx_21.dot(cx_12)).T

class CZ(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'CZ'
        self.unitary = Unitary.get_unitary([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 1, 0],
                                            [0, 0, 0,-1]])
        self.qbits = qbits
        self.cbits = cbits

    def get_circuit_unitary(self, n_qbits: int) -> sparse.dok_matrix:
        identity = I([],[]).get_unitary()
        unitary  = Z([],[]).get_unitary()
        
        operations_zero = [identity]*n_qbits
        operations_zero[self.qbits[0]] = Unitary.mul(ket_zero,ket_zero.T)

        operations_one = [identity]*n_qbits
        operations_one[self.qbits[0]] = Unitary.mul(ket_one,ket_one.T)
        operations_one[self.qbits[1]] = unitary

        return Unitary.reduce_kron(operations_zero[::-1]) + \
               Unitary.reduce_kron(operations_one[::-1])

class Measurement(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        if(min(qbits) < 0):
            raise Exception("Invalid qubits") 

        self.name = 'MEASUREMENT'
        self.unitary = None
        self.qbits = qbits
        self.cbits = cbits

    def get_qbits(self, n_qbits: int) -> list[int]:
        if(max(self.qbits) > n_qbits):
            raise Exception("Measured qubits out of range")

        return [n_qbits-1-qbit for qbit in self.qbits][::-1]

    def get_measured_superposition(self, n_qbits: int, statevector: sparse.dok_matrix) -> sparse.dok_matrix:
        if(max(self.qbits) > n_qbits):
            raise Exception("Measured qubits out of range") 
       
        qbits = [n_qbits-1-qbit for qbit in self.qbits][::-1]
        superposition = sparse.lil_matrix((2**len(qbits),1))
        cx = sparse.coo_matrix(statevector)

        for i,j,v in zip(cx.row, cx.col, cx.data):
            index = int("".join(np.array(list(format(i,'0{}b'.format(n_qbits))))[qbits]), 2) 
            superposition[index,j] += abs(v)**2  

        return superposition.power(1/2).todok()
