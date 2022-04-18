import scipy.sparse as sparse
import functools as ft
import numpy as np

class Unitary():
    @staticmethod
    def get_unitary(unitary):
        return sparse.lil_matrix(unitary, dtype='complex128')

    @staticmethod
    def mul(x, y):
        return x*y

    @staticmethod
    def dot(matrices):
        return ft.reduce(lambda x, y: x.dot(y), matrices)

    @staticmethod
    def reduce_kron(operations):
        return ft.reduce(lambda x, y: sparse.kron(x, y), operations)


class Statevector():
    @staticmethod
    def get_statevector(shape: tuple, values: np.array = None, initial_state: str = '0'):
        if(values is None):
            statevector = sparse.lil_matrix(shape, dtype='complex128')
            statevector[int(initial_state, 2)] = 1
        else:
            statevector = sparse.csr_matrix(values, dtype='complex128')
        return statevector

    @staticmethod
    def get_summed_probabilities(statevector):
        return np.cumsum(statevector.multiply(statevector.conjugate()).toarray())
    
    @staticmethod
    def evolve(statevector, unitary: Unitary):
        return unitary.dot(statevector)

    @staticmethod
    def measure_superposition(statevector, n_qbits: int, qbits: list[int]):
        superposition = sparse.lil_matrix((2**len(qbits),1))
        cx = sparse.coo_matrix(statevector)

        for i,j,v in zip(cx.row, cx.col, cx.data):
            index = int("".join(np.array(list(format(i,'0{}b'.format(n_qbits))))[qbits]), 2) 
            superposition[index,j] += abs(v)**2  

        return superposition.power(1/2)

