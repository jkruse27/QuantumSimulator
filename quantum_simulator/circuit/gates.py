import functools as ft
import numpy as np
import scipy.sparse as sparse

"""
Quantum Gates
"""

ket_zero = sparse.dok_matrix([[1], [0]], dtype="complex128")
ket_one  = sparse.dok_matrix([[0], [1]], dtype="complex128") 

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

        return ft.reduce(lambda x, y: sparse.kron(x, y), operations[::-1])
        #return ft.reduce(lambda x, y: sparse.kron(x, y), operations)

    def get_qbits(self) -> sparse.dok_matrix:
        return self.qbits

    def get_cbits(self) -> sparse.dok_matrix:
        return self.cbits

    def get_name(self) -> str:
        return self.name

class I(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'I'
        self.unitary = sparse.dok_matrix([[1, 0],
                                          [0, 1]])
        self.qbits = qbits
        self.cbits = cbits

class H(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'H'
        self.unitary = (1/np.sqrt(2))*sparse.dok_matrix([[1, 1],
                                                         [1,-1]])
        self.qbits = qbits
        self.cbits = cbits
    
class X(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'X'
        self.unitary = sparse.dok_matrix([[0, 1],
                                          [1, 0]])
        self.qbits = qbits
        self.cbits = cbits

class Y(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'Y'
        self.unitary = sparse.dok_matrix([[0,  -1.j],
                                          [1.j,  0]])
        self.qbits = qbits
        self.cbits = cbits

class Z(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'Z'
        self.unitary = sparse.dok_matrix([[1,  0],
                                          [0, -1]])
        self.qbits = qbits
        self.cbits = cbits

class S(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'S'
        self.unitary = sparse.dok_matrix([[1,  0],
                                          [0, 1.j]])
        self.qbits = qbits
        self.cbits = cbits

class T(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'T'
        self.unitary = sparse.dok_matrix([[1,  0],
                                          [0, np.exp(1.j*np.pi/4)]])
        self.qbits = qbits
        self.cbits = cbits

class U1(Gate):
    def __init__(self, qbits: list[int], lambda_: float, phi: float, theta: float, cbits: list[int] = None, **kwargs):
        self.name = 'U1'
        self.unitary = sparse.dok_matrix([[1,  0],
                                          [0, np.exp(1.j*self.lambda_)]])
        self.qbits = qbits
        self.cbits = cbits

class U2(Gate):
    def __init__(self, qbits: list[int], lambda_: float, phi: float, theta: float, cbits: list[int] = None, **kwargs):
        self.name = 'U2'
        self.unitary = (1/np.sqrt(2))*sparse.dok_matrix([[1,                   -np.exp(1.j*self.lambda_)],
                                                         [np.exp(1.j*self.phi), np.exp(1.j*(self.phi+self.lambda_))]])
        self.qbits = qbits
        self.cbits = cbits

class U3(Gate):
    def __init__(self, qbits: list[int], lambda_: float, phi: float, theta: float, cbits: list[int] = None, **kwargs):
        self.name = 'U3'
        self.unitary = sparse.dok_matrix([[np.cos(self.theta/2),  -np.exp(1.j*self.lambda_)*np.sin(self.theta/2)],
                                          [np.exp(1.j*self.phi)*np.sin(self.theta/2), np.exp(1.j*(self.phi+self.lambda_))*np.cos(self.theta/2)]])
        self.qbits = qbits
        self.cbits = cbits

class CX(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'CX'
        self.unitary = sparse.dok_matrix([[1, 0, 0, 0],
                                          [0, 1, 0, 0],
                                          [0, 0, 0, 1],
                                          [0, 0, 1, 0]])
        self.qbits = qbits
        self.cbits = cbits

    def get_circuit_unitary(self, n_qbits: int) -> sparse.dok_matrix:
        identity = I([],[]).get_unitary()
        unitary  = X([],[]).get_unitary()
        
        operations_zero = [identity]*n_qbits
        operations_zero[self.qbits[0]] = ket_zero*ket_zero.T
        
        operations_one = [identity]*n_qbits
        operations_one[self.qbits[0]] = ket_one*ket_one.T
        operations_one[self.qbits[1]] = unitary

        return ft.reduce(lambda x, y: sparse.kron(x, y), operations_zero[::-1]) + \
                ft.reduce(lambda x, y: sparse.kron(x, y), operations_one[::-1])
        #return ft.reduce(lambda x, y: sparse.kron(x, y), operations_zero) + \
        #       ft.reduce(lambda x, y: sparse.kron(x, y), operations_one)

class SWAP(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'SWAP'
        self.unitary = sparse.dok_matrix([[1, 0, 0, 0],
                                          [0, 0, 1, 0],
                                          [0, 1, 0, 0],
                                          [0, 0, 0, 1]])
        self.qbits = qbits
        self.cbits = cbits

class CZ(Gate):
    def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
        self.name = 'CZ'
        self.unitary = sparse.dok_matrix([[1, 0, 0, 0],
                                          [0, 1, 0, 0],
                                          [0, 0, 1, 0],
                                          [0, 0, 0,-1]])
        self.qbits = qbits
        self.cbits = cbits

    def get_circuit_unitary(self, n_qbits: int) -> sparse.dok_matrix:
        identity = I([],[]).get_unitary()
        unitary  = Z([],[]).get_unitary()
        
        operations_zero = [identity]*n_qbits
        operations_zero[self.qbits[0]] = ket_zero*ket_zero.T

        operations_one = [identity]*n_qbits
        operations_one[self.qbits[0]] = ket_one*ket_one.T
        operations_one[self.qbits[1]] = unitary

        return ft.reduce(lambda x, y: sparse.kron(x, y), operations_zero[::-1]) + \
                ft.reduce(lambda x, y: sparse.kron(x, y), operations_one[::-1])
        #return ft.reduce(lambda x, y: sparse.kron(x, y), operations_zero) + \
        #       ft.reduce(lambda x, y: sparse.kron(x, y), operations_one)

class Measurement(Gate):
    def __init__(self, qbits: list[int], cbits: list[int], **kwargs):
        self.name = 'MEASUREMENT'
        self.unitary = None
        self.qbits = qbits
        self.cbits = cbits
