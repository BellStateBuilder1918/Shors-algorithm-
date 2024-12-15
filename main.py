# -*- coding: utf-8 -*-
"""Shor's 1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KeUUGnO6_UlW_G-1LnuYgn7VBiYKRxra
"""

!pip install cirq numpy

import cirq
import numpy as np
from math import gcd
import random


def finding(a, N):

    num_qubits = 2 * int(np.log2(N))
    qu = cirq.LineQubit.range(num_qubits)
    c = cirq.Circuit()


    for q in qu[:num_qubits // 2]:
        c.append(cirq.H(q))

    def expo(a, N, control_qubit, target_qubit):
        exp = a ** 2 % N
        c.append(cirq.ControlledGate(cirq.X**exp).on(control_qubit, target_qubit))

    for i, qubit in enumerate(qu[:num_qubits // 2]):
       expo(a, N, qubit, qu[num_qubits // 2 + i])


    def qft(circuit, qubits):
        for i in range(len(qubits)):
            for j in range(i):
                circuit.append(cirq.CZ(qubits[j], qubits[i]) ** (-1 / (2 ** (i - j))))
            circuit.append(cirq.H(qubits[i]))

    qft(c, qu[:num_qubits // 2])

    c.append(cirq.measure(*qu[:num_qubits // 2], key='measurement'))

    simulator = cirq.Simulator()
    result = simulator.run(c, repetitions=10)
    measurements = result.measurements['measurement']
    return measurements


def shors(N, a=None):

    if N % 2 == 0:
        return 2

    if a is None:
        a = random.randint(2, N - 1)
    while gcd(a, N) != 1:
        a = random.randint(2, N - 1)

    print(f"Randomly chosen a: {a}")

    order_measurements = finding(a, N)
    print(f"Quantum order measurements: {order_measurements}")

    r = measurements(order_measurements, N)
    if r % 2 != 0 or pow(a, r // 2, N) == N - 1:
        return None  #

    factor1 = gcd(pow(a, r // 2) - 1, N)
    factor2 = gcd(pow(a, r // 2) + 1, N)

    return factor1, factor2


def measurements(measurements, N):
    r = 2
    return r



def main():
    try:
        N = int(input("Enter composite number N: "))
        a_input = input("Enter base a (leave blank for random selection): ")
        a = int(a_input) if a_input else None

        factors = shors(N, a)
        if factors:
            print(f"Factors of {N}: {factors}")
        else:
            print("Failed to find factors. Retry.")
    except ValueError:
        print("enter valid integers for N and a.")

if __name__ == "__main__":
    main()

