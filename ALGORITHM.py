"""Algoritmo de Shor / Shor's Algorithm"""

import math
import random
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from math import gcd
from fractions import Fraction
from qiskit.circuit.library import QFTGate, UnitaryGate
from qiskit.quantum_info import Operator
from qiskit_aer import AerSimulator
import numpy as np


N = int(input("Digite o N: ")) 
L = math.ceil(math.log2(N))         #função que calcula Log2(N) 

'==================  Função cria matriz =================='

def cria_matriz(N, a, L):

    dimensao = 2**L
    M = np.zeros((dimensao, dimensao))  #numpy para criar matriz de zeros 2^L x 2^L
    for y in range(dimensao):
        if y < N:
            M[(a * y) % N, y] = 1     #para a colyna y (primeiro registrador) 1 na linha a^yMod(N)
        else:
            M[y,y] = 1      #garante unitariedade para o nosso operador, evitando linhas/colunas vazias
    
    return M

'==================  Preparando o Circuito =================='

num_alvo = L  # Número de qubits alvo (L)
num_controle = (L + 4)  # Número de qubits de controle (t)
sucesso = False
while True:
    a = random.randint(2, N-1)
    if gcd(a, N) != 1:      #"a" não é coprimo com N, sorteia outro
        continue
    M = cria_matriz(N, a, L)
    gate_U = UnitaryGate(M, label=f"U_{a}")

    '==================  Cria o circuito =================='

    alvo = QuantumRegister(num_alvo, name="L")
    controle = QuantumRegister(num_controle, name="t")
    saida = ClassicalRegister(num_controle)
    shor = QuantumCircuit(controle, alvo, saida) # Declara sistema (t, L e bits clássicos)

    for k in range(num_controle):
        shor.h(controle[k])         #coloca registradores "t" em superpsição
    shor.x(alvo[0])                 #coloca registrador "L" em estado |1>

    '==================  Aplica as operações =================='

    for j in range(num_controle):
        U_power = gate_U.power(2**j).control(1)     #aplica as portas controladas nos j níveis
        shor.append(U_power, [controle[j]] + list(alvo))
       
    '==================  Aplica QFT inversa =================='

    shor.append(QFTGate(num_controle).inverse(), range(num_controle))      #porta do qiskit que aplica a qft QFTGate((qubits a serem aplicados), (bits clássicos))
    shor.measure(range(num_controle), range(num_controle))

    '==================  Simulador =================='
    
    sim = AerSimulator()
    trans = transpile(shor, sim)
    result = sim.run(trans, shots=1024).result()
    counts = result.get_counts(shor)

    '==================  Maior pico =================='
    condicao_mudar_a = False
    while True:
        while True:                                    #Laço garante que não escolheremos |0...00>
            if not counts:                        #verifica se nenhum dos picos do nosso a gera um valor válido para r
                condicao_mudar_a = True
                break
            candidato_maior_pico = max(counts, key = counts.get)        #extrai o pico mais frequente 
            l = int(candidato_maior_pico, 2)                        #transforma valor binário do pico mais frequente em base decimal
            if l > 0:
                break
            del counts[candidato_maior_pico]            #se não entrar no if, candidato_maior_pico = 0...000 e, assim, é deletado, laço escolhe próximo pico

        if condicao_mudar_a:                #se condição for verdadeira, já verificamos todos os picos e o "a" atual não é válido
            break
        '==================  Frações contínuas para extrair r =================='

        fracao = l / 2**num_controle    #equivalente à fração l/2^t
        frac = Fraction(fracao).limit_denominator(N)         #função do python que calcula a menor simplificação
        r = frac.denominator
    
        '==================  Extraindo fatores primos =================='

        if r % 2 != 0:
            del counts[candidato_maior_pico]
            continue
        exp_mod = pow(a, r // 2, N)
        
        if exp_mod == N - 1:
            condicao_mudar_a = True         #achados fatores triviais, break quebra o laço atual para mudar de a
            break
        elif exp_mod == 1:
            del counts[candidato_maior_pico]
            continue
        
        fator_1 = gcd(exp_mod -1, N)
        fator_2 = gcd(exp_mod +1, N)
        if fator_1 * fator_2 != N:
            del counts[candidato_maior_pico]
            continue
        else:
            sucesso = True
            break

    if sucesso:
        print(f"a = {a}")
        print(f"r = {r}")       
        print(f"gcd({a}^{r}/2 -1, {N}) = {fator_1}")
        print(f"gcd({a}^{r}/2 +1, {N})= {fator_2}")
        print(f"para N = {N} e a = {a}, nossos fatores primos são {fator_1} e {fator_2}")
        break
    
'==================  Decriptando Mensagem =================='

phi = (fator_1 - 1) * (fator_2 -1)      
chave_publica_e = int(input("Digite o e: "))   
d = pow(chave_publica_e, -1, phi)                      
C = int(input("Digite a mensagem criptografada: "))     
M = pow(C, d, N)          


digitos = []
temp = M
while temp > 0:
    digitos.append(temp % 26)
    temp //= 26

digitos.reverse()

mensagem = ""
for d in digitos:
    mensagem += chr(d + ord('A'))

print(mensagem)
