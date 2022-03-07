from setuptools import setup

setup(
   name='QuantumSimulator',
   version='0.1.0',
   author='João Gabriel Segato Kruse',
   author_email='soyjog@gmail.com',
   packages=['quantum_simulator', 'quantum_simulator.tests', 'quantum_simulator.circuit', 
             'quantum_simulator.transpiler', 'quantum_simulator.simulator'],
   #scripts=['bin/script1','bin/script2'],
   url='https://github.com/jkruse27/QuantumSimulator',
   license='LICENSE.txt',
   description='Quantum computing simulator for simple experiments',
   long_description=open('README.md').read(),
   install_requires=[
       "Django >= 1.1.1",
       "pytest",
       "setuptools>=42",
       "wheel",
       "networkx>=2.6.3",
       "numpy>=1.22.2",
       "ply>=3.11",
       "pycparser>=2.21",
       "pyparsing>=3.0.7",
       "rply>=0.7.8",
       "scipy>=1.8.0",
       "sympy>=1.9"
   ],
)

