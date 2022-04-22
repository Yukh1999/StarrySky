"""
QCQ引入非线性
"""

from qutip import destroy, qeye, tensor
import numpy as np

# 常数
freq_q = 5000
freq_c = 3000
N = 3
g_12 = 1
g_qc = 100
alpha = -1000


# 算符
a = destroy(N)
a_dag = a.dag()
I = qeye(N)


a1 = tensor(a, I, I)
a1_dag = a1.dag()
a2 = tensor(I, a, I)
a2_dag = a2.dag()
ac = tensor(I, I, a)
ac_dag = ac.dag()


H = freq_q * a1_dag * a1 + freq_q * a2_dag * a2 + freq_c * ac_dag * ac \
    + alpha/2 * a1_dag**2 * a1**2 + alpha/2 * a2_dag**2 * a2**2 + alpha/2 * ac_dag**2 * ac**2 \
    + g_qc * (a1_dag * ac + ac_dag*a1) + g_qc * (a2_dag * ac + ac_dag*a2) + g_12 * (a1_dag * a2 + a2_dag*a1)

print(H.eigenenergies())

alpha = 0

H = freq_q * a1_dag * a1 + freq_q * a2_dag * a2 + freq_c * ac_dag * ac \
    + alpha/2 * a1_dag**2 * a1**2 + alpha/2 * a2_dag**2 * a2**2 + alpha/2 * ac_dag**2 * ac**2 \
    + g_qc * (a1_dag * ac + ac_dag*a1) + g_qc * (a2_dag * ac + ac_dag*a2) + g_12 * (a1_dag * a2 + a2_dag*a1)

print(H.eigenenergies())
