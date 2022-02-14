import numpy as np

"""
Quantum Gates
"""


class Gate:
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.name = ''
        self.unitary = None
        self.qbits = None
        self.cbits = None

    def get_unitary(self) -> np.array:
        return self.unitary

    def get_qbits(self) -> np.array:
        return self.qbits

    def get_cbits(self) -> np.array:
        return self.cbits

    def get_name(self) -> str:
        return self.name

class H(Gate):
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.name = 'H'
        self.unitary = (1/np.sqrt(2))*np.array([[1, 1],
                                                [1,-1]])
        self.qbits = qbits
        self.cbits = cbits
    
class X(Gate):
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.name = 'X'
        self.unitary = np.array([[0, 1],
                                 [1, 0]])
        self.qbits = qbits
        self.cbits = cbits

class Y(Gate):
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.name = 'Y'
        self.unitary = np.array([[0,  -1.j],
                                 [1.j,  0]])
        self.qbits = qbits
        self.cbits = cbits

class Z(Gate):
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.name = 'Z'
        self.unitary = np.array([[1,  0],
                                 [0, -1]])
        self.qbits = qbits
        self.cbits = cbits

class S(Gate):
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.name = 'S'
        self.unitary = np.array([[1,  0],
                                 [0, 1.j]])
        self.qbits = qbits
        self.cbits = cbits

class T(Gate):
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.name = 'T'
        self.unitary = np.array([[1,  0],
                                 [0, np.exp(1.j*np.pi/4)]])
        self.qbits = qbits
        self.cbits = cbits

class U1(Gate):
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.lambda_ = kwargs.get('lambda', 0)

        self.name = 'U1'
        self.unitary = np.array([[1,  0],
                                 [0, np.exp(1.j*self.lambda_)]])
        self.qbits = qbits
        self.cbits = cbits

class U2(Gate):
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.lambda_ = kwargs.get('lambda', 0)
        self.phi = kwargs.get('phi', 0)

        self.name = 'U2'
        self.unitary = (1/np.sqrt(2))*np.array([[1,                   -np.exp(1.i*self.lambda_)],
                                                [np.exp(1.i*self.phi), np.exp(1.j*(self.phi+self.lambda_))]])
        self.qbits = qbits
        self.cbits = cbits

class U3(Gate):
    def __init__(self, qbits: iter, cbits: iter, **kwargs):
        self.lambda_ = kwargs.get('lambda', 0)
        self.phi = kwargs.get('phi', 0)
        self.theta = kwargs.get('theta', 0)

        self.name = 'U3'
        self.unitary = np.array([[np.cos(self.theta/2),  -np.exp(1.i*self.lambda_)*np.sin(self.theta/2)],
                                 [np.exp(1.i*self.phi)*np.sin(self.theta/2), np.exp(1.j*(self.phi+self.lambda_))*np.cos(self.theta/2)]])
        self.qbits = qbits
        self.cbits = cbits

class CX(Gate):
    def __init__(self, qbits: iter, cbits=[]: iter, **kwargs):
        self.name = 'CX'
        self.unitary = np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 0, 1],
                                 [0, 0, 1, 0]])
        self.qbits = qbits
        self.cbits = cbits

class SWAP(Gate):
    def __init__(self, qbits: iter, cbits=[]: iter, **kwargs):
        self.name = 'SWAP'
        self.unitary = np.array([[1, 0, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 0, 1]])
        self.qbits = qbits
        self.cbits = cbits

class CZ(Gate):
    def __init__(self, qbits: iter, cbits=[]: iter, **kwargs):
        self.name = 'CZ'
        self.unitary = np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0,-1]])
        self.qbits = qbits
        self.cbits = cbits
