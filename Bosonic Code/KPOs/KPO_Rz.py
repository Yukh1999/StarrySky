"""
KPO system

Rz(φ) gate simulation
"""

from qutip import coherent, destroy, qeye, mesolve
import numpy as np
from matplotlib import pyplot as plt


# 定义常数
N = 20  # 维度
delta = 0  # 失谐
K = 1  # 非线性强度
P = 4 * K  # 双光子驱动强度

# 定义算符
a = destroy(N)
a_dag = a.dag()
I = qeye(N)

# 定义逻辑比特态
alpha = np.sqrt(P/K)
logical_0 = coherent(N=20, alpha=alpha)
logical_1 = coherent(N=20, alpha=-alpha)


def P_d(_t, _phi, _Tg):
    """
    Driving pulse
    """

    return np.pi * _phi * np.sin(np.pi * _t / _Tg) / (8 * _Tg * np.sqrt(P/K))


def ham(_t, *args):
    """
    Hamiltonian
    """

    ham_1 = delta * a_dag * a + K/2 * (a_dag ** 2) * (a ** 2) - P/2 * (a_dag ** 2 + a ** 2)
    ham_d = P_d(_t, *args) * (a + a_dag)

    return ham_1 + ham_d


# 脉冲总时间
Tg = 2/K
phi = np.pi / 4
tlist = np.linspace(0, Tg, 100)

initial_state = (logical_0 + logical_1) / np.sqrt(2)

final_state = mesolve(ham, initial_state, tlist=tlist, args=[phi, Tg])

phase_factor = 1j * phi / 2
ideal_state = (logical_0 * np.exp(-phase_factor) + logical_1 * np.exp(phase_factor)) / np.sqrt(2)

fidelity = 1


