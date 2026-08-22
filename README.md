# Shor's Algorithm & RSA Decryption / Algoritmo de Shor e Decriptografia RSA

Implementação prática do Algoritmo de Shor para fatoração de números inteiros via computação quântica, com aplicação na quebra de criptografia RSA.

## Estudo de Computação Quântica para implementação de algoritmo:
-Interações iniciais, criação de circuitos básicos;
-Transformada de Fourier Quântica;
-Estimação de Fase Quântica;

## Implementação do Algoritmo de Shor:
-Sub-rotina quântica de fatoração em co-primos; 
-Sub-rotinas de verificação de casos triviais
-De-criptografia de mensagem (input no código) utilizando inverso multiplicativo de mensagem já criptografada. 

## English (sorry for my english btw)

Practical implementation of Shor's Algorithm for integer factorization via quantum computing, with application to breaking RSA encryption.

Initial learning and experimentation stage, laying the groundwork for the algorithm's implementation:

### Quantum Computing Study
- First interactions and creation of basic quantum circuits
- Quantum Fourier Transform (QFT)
- Quantum Phase Estimation (QPE)

### Shor's Algorithm Implementation
- Quantum co-prime factoring sub-routine
- Trivial case verification sub-routines
- Message decryption (input in the code), using the multiplicative inverse of the already-encrypted message

## Como rodar / (running)

```bash
pip install qiskit qiskit-aer
python main.py
```

## Tecnologias

- Python
- Qiskit
