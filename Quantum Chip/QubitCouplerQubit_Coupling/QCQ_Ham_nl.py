"""
QCQ引入非线性

结论：在 dispersive regime 以及弱非谐性近似下，非线性不会对 Q-Q 等效耦合强度产生影响
"""

from qutip import destroy, qeye, tensor
import numpy as np
from matplotlib import pyplot as plt

# 常数
freq_q = 5000
# freq_c = 3000
N = 4
g_12 = 8
g_qc = 100
alpha = -500


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

# 调节 coupler 频率
freq_c_ls = np.linspace(6000, 9000, 100)

E1_lin = list()
E2_lin = list()
E1_nl = list()
E2_nl = list()

E_diff_nl = list()
E_diff_lin = list()

for freq_c in freq_c_ls:
    H_nl = freq_q * a1_dag * a1 + freq_q * a2_dag * a2 + freq_c * ac_dag * ac \
        + alpha/2 * a1_dag**2 * a1**2 + alpha/2 * a2_dag**2 * a2**2 + alpha/2 * ac_dag**2 * ac**2 \
        + g_qc * (a1_dag * ac + ac_dag*a1) + g_qc * (a2_dag * ac + ac_dag*a2) + g_12 * (a1_dag * a2 + a2_dag*a1)

    energies_nl = H_nl.eigenenergies()
    E1_nl.append(energies_nl[1])
    E2_nl.append(energies_nl[2])
    E_diff_nl.append(energies_nl[2]-energies_nl[1])

    H_lin = freq_q * a1_dag * a1 + freq_q * a2_dag * a2 + freq_c * ac_dag * ac \
        + g_qc * (a1_dag * ac + ac_dag*a1) + g_qc * (a2_dag * ac + ac_dag*a2) + g_12 * (a1_dag * a2 + a2_dag*a1)

    energies_lin = H_lin.eigenenergies()
    E1_lin.append(energies_lin[1])
    E2_lin.append(energies_lin[2])
    E_diff_lin.append(energies_lin[2]-energies_lin[1])

print('E1_lin: ', E1_lin)
print('E2_lin: ', E2_lin)
print('E1_nl: ', E1_nl)
print('E2_nl: ', E2_nl)
print('E_diff_lin: ', E_diff_lin)
print('E_diff_nl', E_diff_nl)
# 绘图
fig, axs = plt.subplots(2, 2, sharex=True)
axs[0][0].plot(freq_c_ls, E1_nl, label='E1_nl')
axs[0][0].plot(freq_c_ls, E2_nl, label='E2_nl')
axs[0][0].legend()

axs[0][1].plot(freq_c_ls, E1_lin, label='E1_lin')
axs[0][1].plot(freq_c_ls, E2_lin, label='E2_lin')
axs[0][1].legend()

axs[1][0].plot(freq_c_ls, E1_nl, label='E1_nl')
axs[1][0].plot(freq_c_ls, E2_nl, label='E2_nl')
axs[1][0].plot(freq_c_ls, E1_lin, label='E1_lin')
axs[1][0].plot(freq_c_ls, E2_lin, label='E2_lin')
axs[1][0].legend()

axs[1][1].plot(freq_c_ls, E_diff_nl, label='E_diff_nl')
axs[1][1].plot(freq_c_ls, E_diff_lin, label='E_diff_lin')
axs[1][1].legend()

plt.show()


