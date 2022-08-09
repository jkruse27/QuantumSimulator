# QuantumSimulator
Simulador de sistemas quânticos

## Introdução e Objetivo

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Este projeto tem como objetivo geral compreender profundamente como um computador quântico funciona baseado em conceitos fundamentais de mecânica quântica; como a propriedade de interferência quântica, que é uma das principais propriedades para explicar o experimento de dupla fenda; e que é também uma das principais propriedades quânticas utilizadas em computação quântica [1, 2]. O objetivo específico do projeto é o desenvolvimento de um conjunto de ferramentas computacionais para um programa de computador para simular o efeito de portas quânticas e do algoritmo de busca quântica de Grover [3] e a utilização de computadores quânticos disponíveis online [4].   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; O uso de computação quântica e informação quântica estão no centro de diversas propostas que podem revolucionar o modo como nos comunicamos e processamos informação, sendo importanteo entendimento a base destas propostas. O objetivo de longo prazo deste projeto é utilizar este aprendizado para formar uma base sólida nos alunos em tópicos modernos de computação quântica, física, e programação em sistemas quânticos, e prepará-los para o desenvolvimento de projetos mais avançados neste fascinante campo de pesquisa.

## Desenvolvimento

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A implementação para o simulador em sua totalidade foi feita utilizando a linguagem de programação Python, e foi baseada no projeto apresentado em [5].
    
### Registrador Quântico
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Um sistema quântico contendo N qubits pode ser representado na base computacional como:
        $$\alpha_0|0\rangle+\alpha_1|1\rangle+...+\alpha_{2^N}|2^N\rangle$$
onde $\alpha_j$ é uma amplitude complexa e estamos usando a forma decimal do valor dos estados da base. Assim, sabendo as $2^N$ amplitudes nós podemos representar exatamente o estado do sistema.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Um registrador quântico composto por N qubits pode ser descrito pelas suas $2^N$ amplitudes complexas correspondendo a cada uma das bases computacionais. Esse estado quântico será representado como um vetor coluna, que em Python pode ser implementado como uma lista, numpy array, ou, por motivos que veremos depois, sparse matrix. Nessa representação o índice do vetor está associado com a amplitude do estado cuja representação em decimal corresponde a tal índice (assumindo que partimos do índice 0). Assim, em um sistema com 3 qubits por exemplo teremos um vetor coluna de 8 posições com o índice 0 sendo o estado $|000\rangle$, o índice 1 o estado $|001\rangle$ e assim em diante até o índice 7 sendo o estado $|111\rangle$ como mostra a equação 1.  

$$|\psi\rangle = \alpha_0|0\rangle+\alpha_1|1\rangle+...+\alpha_{2^N}|2^N\rangle \equiv \begin{bmatrix}\alpha_0 \\\\ \alpha_1 \\\\ ...\\\\ \alpha_{2^N} \end{bmatrix}, \\;\\; eq. 1$$
        
### Portas Quânticas
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Na subseção anterior nós vimos como descrever um estado quântico utilizando vetores, e agora veremos como podemos atuar em cima desses estados. Em um computador quântico real, o sistema quântico segue a equação de Schrödinger, que para um certo período de tempo é equivalente a aplicação de um operador unitário ao estado. Para a nossa representação do sistema como um vetor, isso corresponde à multiplicação do vetor de estados pela matriz representando o operador unitário e tendo dimensões $2^N$ x $2^N$, onde N é o número de qubits, resultando em:
        $$|\psi\rangle \xrightarrow[]{} U|\psi\rangle$$

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Algumas das portas mais usadas e suas representações matriciais correspondentes podem ser vistas na Figura 1.  
  <p align="center"><a href="https://commons.wikimedia.org/wiki/File:Quantum_Logic_Gates.png#/media/File:Quantum_Logic_Gates.png"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Quantum_Logic_Gates.png/1200px-Quantum_Logic_Gates.png" alt="Quantum Logic Gates.png"></a><br><b>Figura 1: Exemplos de portas quânticas (imagem adaptada de https://en.wikipedia.org/wiki/Quantum_logic_gate)</b></p>
        
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Para sua representação foi optado pelo uso de classes contendo sua matriz unitária correspondente, nome e qubits alvo, seguindo a interface mostrada no Listing 1.
```
            class Gate:
                def __init__(self, qbits: list[int], cbits: list[int] = None, **kwargs):
                    self.name = ''
                    self.unitary = None
                    self.qbits = None
                    self.cbits = None
            
                def get_unitary(self) -> np.array:
                    return self.unitary
            
                def get_qbits(self) -> np.array:
                    return self.qbits
```
<p align='center'><b>Listing 1: Exemplo de classe para Portas Lógicas Quânticas</b></p>
        
### Aplicando Portas Quânticas em Sistemas com Múltiplos Qubits

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Quando temos um sistema com apenas um qubit, seu vetor de estados possui dimensão 2, de modo que podemos aplicar portas quânticas de 1 qubit nele simplesmente multiplicando-o pela matriz do operador (que é 2x2), como visto anteriormente. No entanto, quando temos mais de um qubit é necessário que obtenhamos a matriz $2^Nx2^N$ que corresponde a aplicação da porta em um qubit específico. Para isso, utilizamos a operação conhecida como produto tensorial ($\otimes$), que nos permitirá definir qual operação será realizada em cada qubit individualmente em nossa unitária. Assim, a operação que será aplicada ao sistema quando desejamos aplicar uma certa unitária U ao qubit k corresponde à:  

$$\hat{U}^{(k)} = 1 \otimes 1 \otimes ...\otimes \hat{U} \otimes...\otimes 1$$
     
ou seja, estamos aplicando identidades (não fazendo nada) em todos os qubits com exceção do k-ésimo, no qual aplicamos U. Por exemplo, caso desejemos aplicar uma porta Hadamard ao segundo qubit de um sistema de 3 qubits nós teríamos a seguinte unitária:
            
$$\hat{H}^{2} = 1 \otimes H \otimes 1 = 
\begin{bmatrix}1 & 0\\\\0 & 1\end{bmatrix} \otimes
\begin{bmatrix}1 & 1\\\\ 1 & -1\end{bmatrix} \otimes
\begin{bmatrix}1 & 0\\\\ 0 & 1\end{bmatrix} = 
\begin{bmatrix} 1 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 1 & 0 & 0 & 0 & 0 \\
1 & 0 &-1 & 0 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 &-1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 1 \\
0 & 0 & 0 & 0 & 1 & 0 &-1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 &-1 \\
\end{bmatrix}$$
            
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outro fato interessante é que com essa forma de obter as unitárias correspondentes, é possível também aplicar múltiplas portas individuais em paralelo (contanto que em qubits diferentes), bastando substituir a identidade na posição do qubit pelo operador de interesse. Sendo assim, o operador que aplica uma porta Hadamard no qubit 2 enquanto que aplica uma porta Not no qubit 1 em um sistema de 3 qubits poderia ser obtido como $X \otimes H \otimes 1$.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A implementação disso em python é exemplificada no Listing 2.

```
                def create_multiqubit_gate(self, n_qbits: int, gates: list[Gate]) -> np.array:
                    # Iniciamos criando um vetor com a matriz do operador que sera aplicado
                    # em cada qubit (inicialmente assumimos que eh identidade em todos)
                    identity = np.array([1,0],[0,1])
                    operations = [identity]*n_qbits
                    
                    # Para cada porta recebida como entrada, adiciona a matriz correspondente na
                    # posicao referente ao qubit na qual ela atua
                    for gate in gates:
                        operations[gate.qbits[0]] = gate.unitary

                    # Retorna a matriz resultante do produto tensorial de todas as operacoes
                    return ft.reduce(lambda x, y: np.kron(x, y), operations)
```
<p align='center'><b>Listing 2: Função para a obtenção da unitária para múltiplos qubits</b></p>

            
### Portas Quânticas Controladas

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Até agora, nós vimos como aplicar portas em 1 qubit no registrador, mas um outro conjunto essencial para algoritmos quânticos são portas de múltiplos qubits, especialmente portas controladas. Nelas, uma operação é aplicada em um qubit alvo apenas quando um segundo qubit de controle for $|1\rangle$. Um dos exemplos mais comuns desse tipo de operação é a porta CNOT, dada por:   
$$CNOT = \begin{bmatrix} 1 & 0 & 0 & 0 \\\\ 0 & 1 & 0 & 0 \\\\ 0 & 0 & 0 & 1 \\\\ 0 & 0 & 1 & 0 \end{bmatrix}$$
                                     
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Uma forma simples de implementar portas controladas faz o uso dos operadores de projeção $P_0$ e $P_1$ que são dados por:
$$P_0 = |0\rangle\langle0| = \begin{bmatrix}1 & 0 \\\\ 0 & 0\end{bmatrix}, \\;\\; P_1 = |1\rangle\langle1| = \begin{bmatrix}0 & 0 \\\\ 0 & 1\end{bmatrix}$$
             
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Esses projetores nos permitem selecionar o que é aplicado ao sistema com base no estado de um qubit, já que quando o estado for $|0\rangle$, $P_0$ manterá o estado e $P_1$ será 0, e o inverso ocorre quando o estado for $|1\rangle$. Assim, obtemos um operador controlado somando os casos do que ocorre quando o controle é $|0\rangle$ (aplicando o projetor $P_0$ no qubit de controle) e quando o controle é $|1\rangle$ (aplicando o projetor $P_1$ no qubit de controle e a operação desejada no qubit alvo). Na representação por produto tensorial isso seria representado como:
                $$CU = (1 \otimes ... \otimes P_0 \otimes ... \otimes 1) + (1 \otimes ... \otimes P_1 \otimes ... \otimes U \otimes ... \otimes 1)$$
            
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; O que está ocorrendo conceitualmente é que, quando o controle é $|0\rangle$, o segundo termo dessa soma se anula (pois $|0\rangle$ e $|1\rangle$ são ortogonais), restando apenas a aplicação de identidades nos qubits restantes (e o qubit de controle se manterá $|0\rangle$). Por outro lado, quando o controle é $|1\rangle$, o primeiro termo que se anula, restando a aplicação da unitária ao qubit alvo (e o qubit de controle se manterá $|1\rangle$). Quando o qubit está em superposição ocorre uma mistura de ambos esses casos.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Para exemplificar, vamos mostrar a formulação da porta CNOT para 3 qubits, sendo o qubit 1 o alvo e o 3 o controle. Esse operador será dado por:

$$CNOT_{3\xrightarrow[]{}1} = 1 \otimes 1 \otimes P_0 \\; + \\; X \otimes 1 \otimes P_1 = \begin{bmatrix}1&0\\\\0&1\end{bmatrix} \otimes \begin{bmatrix}1&0\\\\0&1\end{bmatrix} \otimes \begin{bmatrix}1&0\\\\0&0\end{bmatrix} + \begin{bmatrix}0&1\\\\1&0\end{bmatrix} \otimes \begin{bmatrix}1&0\\\\0&1\end{bmatrix} \otimes \begin{bmatrix}0&0\\\\0&1\end{bmatrix} =$$  

$$\begin{bmatrix}1&0&0&0&0&0&0&0\\\\0&0&0&0&0&0&0&0\\\\0&0&1&0&0&0&0&0\\\\0&0&0&0&0&0&0&0\\\\0&0&0&0&1&0&0&0\\\\0&0&0&0&0&0&0&0\\\\0&0&0&0&0&0&1&0\\\\0&0&0&0&0&0&0&0\end{bmatrix}\\;+\\;\begin{bmatrix}0&0&0&0&0&0&0&0\\\\0&0&0&0&0&1&0&0\\\\0&0&0&0&0&0&0&0\\\\0&0&0&0&0&0&0&1\\\\0&0&0&0&0&0&0&0\\\\0&1&0&0&0&0&0&0\\\\0&0&0&0&0&0&0&0\\\\0&0&0&1&0&0&0&0\end{bmatrix} =\begin{bmatrix}1&0&0&0&0&0&0&0\\\\0&0&0&0&0&1&0&0\\\\0&0&1&0&0&0&0&0\\\\0&0&0&0&0&0&0&1\\\\0&0&0&0&1&0&0&0\\\\0&1&0&0&0&0&0&0\\\\0&0&0&0&0&0&1&0\\\\0&0&0&1&0&0&0&0\end{bmatrix}$$
             
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Com essa implementação podemos aplicar qualquer porta controlada entre quaisquer qubits do sistema, mesmo eles não sendo vizinhos. Uma implementação possível para a geração dessa porta controlada é mostrada no Listing 3.
   
 ```
                def get_controlled_gate(self, n_qbits: int, gate: Gate) -> np.array:
                    # Iniciamos criando um vetor com a matriz do operador que sera aplicado
                    # em cada qubit para cada um dos casos (inicialmente assumimos que eh identidade
                    # em todos)
                    identity = np.array([1,0],[0,1])
                    operations_zero = [identity]*n_qbits
                    operations_one = [identity]*n_qbits
                    
                    # Adicionamos os operadores de projecao na posicao do qubit de controle (por
                    # padrao o primeiro qubit no vetor de qubits da porta) nas respectivas listas
                    operations_zero[gate.qbits[0]] = np.outer(ket_zero, ket_zero)
                    operations_one[gate.qbits[0]] = np.outer(ket_one, ket_one)
                    
                    # Adicionamos a unitária que sera aplicada ao qubit alvo na lista que contem P_1
                    operations_one[self.qbits[1]] = gate.unitary
            
                    # Retornamos a soma das matrizes resultantes dos produtos tensoriais para cada
                    # um dos dois casos do projetor 
                    return ft.reduce(lambda x, y: np.kron(x, y), operations_zero) + \
                           ft.reduce(lambda x, y: np.kron(x, y), operations_one)   
```
<p align='center'><b>Listing 3: Função para a obtenção de uma porta controlada de dois qubits</b></p>
 
### Medições

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Devido às propriedades da mecânica quântica, nós sabemos que ao medirmos um estado em superposição quântica, ele irá colapsar para um dos estados base do operador que está sendo medido. Ademais, a probabilidade dessa medição resultar no estado $|k\rangle$ corresponde à norma de seu coeficiente $\alpha_k$ ($|\alpha_k|^2$) e a soma da probabilidade de todos os estados precisa resultar em 1. Um outro conceito que será importante é o de soma cumulativa de um vetor, que é um vetor no qual o valor em cada posição é a soma de todos os elementos do vetor original até essa, resultando em uma sequência crescente que, nesse caso vai de 0 à 1. Dessa forma, uma maneira simples de simular uma medição é gerar um número aleatório no intervalo 0-1 e verificar qual a primeira posição do vetor de soma acumulada das probabilidades que é menor que ele, cujo índice corresponderá ao estado da base (em decimal) para o qual o sistema colapsará. Vale ressaltar que nesse caso estamos fazendo uma medição na base computacional (Z). Para obter uma distribuição do estado, basta repetir o processo diversas vezes, o que é equivalente a realizar diversas medições. O trecho de código no Listing 4 exemplifica esse processo.
        
```
            import numpy as np
            import random
        
            def measure(self, statevector: np.array, shots: int = 1024, seed: int = 124) -> dict:
                # Definindo a seed para os numeros aleatorios
                random.seed(seed)

                # Gerando o vetor de probabilidades acumuladas
                sum_probabilities = np.cumsum(np.multiply(statevector.conjugate(), statevector))

                # Dicionario para guardar as medicoes resultantes em cada estado
                output_counts = {}

                # Para cada shot
                for i in range(shots):
                    # Gera numero aleatorio
                    random_number = random.random()
                    # Encontra primeiro indice maior que o numero gerado
                    value = next(x for x, val in enumerate(sum_probabilities)
                                                if val > random_number) 
                    
                    # Adiciona resultado ao dicionario (chaves sao o estado em decimal)
                    output_counts[value] = output_counts.get(value, 0) + 1
                
                return output_counts
```
 <p align='center'><b>Listing 4: Função para simular um conjunto de medições</b></p>
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Nesse caso, estamos medindo sempre todos os qubits do sistema, mas para alguns algoritmos apenas um certo subconjunto dos qubits precisa ser medido. Para esses casos, basta realizar o mesmo procedimento já visto, mas desta vez a probabilidade de cada estado do subconjunto de qubits correspondendo a soma da probabilidade (note que nesse caso estamos somando as probabilidades, e não as amplitudes) de todos os estados que contenham esse subconjunto. Pensando em um caso simples de um sistema de 2 qubits cujas probabilidades são, na forma vetorial, como mostradas abaixo:  

$$\begin{bmatrix} 0,10 \\\\ 0,25 \\\\ 0,35 \\\\ 0,30\end{bmatrix}$$  
        
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; as probabilidades na medição do primeiro qubit são:  
$$p(0) = p(|00\rangle)+p(|10\rangle) = 0,10+0,35 = 0,45$$  

$$p(1) = p(|01\rangle)+p(|11\rangle) = 0,25+0,30 = 0,55$$
        
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; e podemos fazer o mesmo para o segundo qubit de forma equivalente.
        
### Circuito Quântico
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; O circuito quântico possui duas representações primária. A primeira e mais simples consiste em uma lista contendo as portas quânticas a serem aplicadas. Nela, as portas são salvas sequencialmente na ordem de aplicação e cada porta guarda os qubits na qual atua. Essa representação possui a vantagem de ser muito facilmente implementada e a adição de novas portas ao sistema pode ser feita adicionando estas à lista, no entanto para outras operações mais complexas como transformações no circuito, uma outra forma de representação se mostra mais adequada: Grafos Direcionados Acíclicos (DAG's).  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Circuitos quânticos podem ser vistos como grafos direcionados acíclicos, nos quais os vértices representam portas quânticas e as arestas dependências entre qubits [6]. Usando essa representação, podemos definir ainda camadas do circuito, sendo a primeira camada o conjunto de vértices sem predecessores. Removendo a primeira camada, podemos aplicar a mesma definição no circuito resultante para obter a segunda, e assim sucessivamente. Unindo esse conhecimento com o de formulação de portas em sistemas com múltiplos qubits, vemos que podemos aplicar todas as portas de uma mesma camada paralelamente criando uma única unitária, caso assim desejemos. A Figura 2 mostra um exemplo do paralelo entre o circuito quântico e o DAG.  

<p align="center">
  <img width="200" src="https://www.researchgate.net/publication/362385758/figure/fig1/AS:1184103818891264@1659323758053/The-Quantum-circuit-and-DAG-of-decomposed-Toffoli-gate_W640.jpg">
<b>Figura 2: Paralelo entre um circuito quântico e seu DAG equivalente. Adaptado de [7]</b>
</p>        
    
### Otimizações
#### Matrizes Esparsas

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Pela forma como o estado do sistema é representado, a quantidade de armazenamento e a ordem das operações matricial cresce exponencialmente com o aumento do número de qubits, já que as estruturas envolverão matrizes e vetores de números complexos com $2^N$ e $2^N$ x $2^N$ elementos. Por conta disso, precisamos de estratégias para amenizar esse problema. Uma maneira de fazer isso é com o uso de matrizes esparsas, já que estados e operadores quânticos geralmente apresentam esparsidade [8]. Com o uso de matrizes esparsas como as implementadas em scipy.sparse em Python, uma quantidade significativa de memória pode ser economizada armazenando apenas as entradas das matrizes que não são nulas (a economia claramente depende da matriz em questão, mas como foi comentado, estados quânticos muitas vezes são esparsas). Essa alteração pode ser feita de forma trivial nos códigos apresentados substituindo as numpy array's por scipy.sparse array's.
            
#### Ordenação das Portas

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Como estamos usando matrizes esparsas, é de nosso interesse que nossas matrizes mantenham essa propriedade o máximo possível pelo maior tempo possível. Para tentar conseguir isso, podemos seguir a ideia apresentada em [8], na qual portas como a Hadamard, $R_x$ e $R_y$, que tendem a aumentar o número de estados da base depois de sua aplicação (o que significaria um aumento de entradas não nulas nos vetores), são postergadas o máximo possível, executando inicialmente portas mais simples. Essa fila criada de portas pode ser feita facilmente a partir da representação do circuito como DAG, pois ela apresenta já as dependências necessárias para cada porta, possibilitando que as portas sejam atrasadas o máximo possível antes que seja necessária sua aplicação para que a simulação possa prosseguir.
            
#### Identidades

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Outra forma de simplificar e acelerar a simulação do circuito é reduzindo o número de operações aplicadas. Isso pode ser feito identificando identidades nos circuitos e substituindo-as por relações de equivalência mais simples [9,10,11]. A implementação dessa etapa envolve uma análise do circuito em sua representação como grafo, a comparação da sequência das portas com equivalências pré-definidas em código já e então sua substituição pela sequência reduzida de portas, como foi feito em [12]. A figura 3 exemplifica algumas das possíveis substituições.
    
            \begin{figure}[H]
              \begin{center}
                \centering
                \includegraphics[width=\columnwidth]{images/FIG-A13-Circuit-identities-The-circuit-in-a-implements-the-controlled-RyphZ.png}
              \caption{Figura 3: Exemplos de equivalências entre circuitos quânticos. Adaptado de [13]}
              \label{fig:identity}
              \end{center}
            \end{figure}  
    
### Compilador
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Para simplificar a implementação e simulação de circuitos quânticos, foi também colocado um interpretador de código em OpenQASM, uma linguagem de interface que permite a descrição de circuitos de pouca profundidade [14]. Isso permite que o usuário crie e execute seus programas sem precisar criar um código em python correspondente, já que o compilador se responsabiliza pela conversão do código para o formato de QuantumCircuit que será usado na simulação.
        
### Simulação
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Tendo inicialmente um circuito quântico já criado, seja diretamente em python através da classe QuantumCircuit (de forma muito semelhante ao Qiskit) ou interpretando um código em OpenQASM, podemos partir para sua simulação. Nessa etapa, o simulador executará sequencialmente as portas quânticas do circuito recebido, o que resultará em um vetor de estados final. Nesse ponto, existem duas opções: receber o próprio vetor de estados como saída ou realizar um conjunto de medições e receber suas contagens de forma análoga ao que ocorreria ao realizar o experimento em um computador quântico real. O código apresentado no Listing 5 exemplifica a execução do circuito para a obtenção do vetor de estados resultante (que poderia ser medido posteriormente com a função no Listing 5).
   
```
            def execute_quantum_circuit(self, qc):
                n_qbits = qc.get_number_of_qubits()
                
                # Cria o vetor de estado inicial (assume-se que o circuito sempre inicia
                # no estado 0)
                initial_state = np.zeros(2**n_qbits, dtype="complex128")
                initial_state[0] = 1

                # Para cada operacao no circuito quantico, aplica ela ao estado atual
                for op in qc.get_operations():
                    initial_state = np.dot(op.get_circuit_unitary(n_qbits),initial_state)
                
                return initial_state
```
<p align='center'><b>Listing 5: Função para a execução de um circuito quântico e obtenção do vetor de estados</b></p>

### Testes
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Para validar o programa foi criado um conjunto de circuitos aleatórios que são executados no simulador e cujas saídas são comparadas com os resultados obtidos pela execução do mesmo circuito usando o framework Qiskit, que já é bem estabelecido. Desta forma é possível verificar a veracidade dos resultados e garantir que o simulador esteja funcionando da forma esperada conforme o código vai sendo modificado e atualizado.
        
## Referências

[1] Nielsen, M. A. & Chuang, I. Quantum computation and quantum information 2002.  
[2] Haroche, S., Raimond, J. & Press, O. U. Exploring the Quantum: Atoms, Cavities, and Photons isbn: 9780198509141. https://books.google.com.br/books?id=ynwSDAAAQBAJ (OUP Oxford, 2006).  
[3] Grover, L. K. A fast quantum mechanical algorithm for database search. Proceedings of the Annual ACM Symposium on Theory of Computing Part F1294, 212–219. issn: 07378017. http://arxiv.org/abs/quant- ph/9605043 (mai. de 1996).  
[4] IBM. IBM Q Experience 2019. https://quantumexperience.ng.bluemix.net/qx/experience.  
[5] Candela, D. Undergraduate computational physics projects on quantum computing. American Journal of Physics 83, 688–702. https://doi.org/10.1119/1.4922296 (2015)  
[6] Childs, A. M., Schoute, E. & Unsal, C. M. Circuit Transformations for Quantum Architectures. en. http://drops.dagstuhl.de/opus/volltexte/2019/10395/ (2019).  
[7] Liu, L. & Dou, X. A New Qubits Mapping Mechanism for Multi-programming Quantum Computing Apr. 2020.  
[8] Jaques, S. & H ̈aner, T. Leveraging state sparsity for more efficient quantum simulations 2021. arXiv:2105.01533 [quant-ph]  
[9] Lomont, C. Quantum Circuit Identities 2003. arXiv: quant-ph/0307111 [quant-ph].  
[10] Abbas, A. et al. Learn Quantum Computation Using Qiskit http://community.qiskit.org/textbook.  
[11] Pointing, J. et al. Quanto: Optimizing Quantum Circuits with Automatic Generation of Circuit Identities 2021. arXiv: 2111.11387 [quant-ph].  
[12] Jang, W. et al. Quantum Gate Pattern Recognition and Circuit Optimization for Scientific Applications. EPJ Web of Conferences 251 (eds Biscarat, C. et al.) 03023. issn: 2100-014X. http://dx.doi.org/10.1051/epjconf/202125103023 (2021).
[13] Friis, N. et al. Flexible resources for quantum metrology. New Journal of Physics 19 (Oct. 2016).  
[14] Cross, A. W., Bishop, L. S., Smolin, J. A. & Gambetta, J. M. Open Quantum Assembly Language 2017. arXiv: 1707.03429 [quant-ph]  
