from qutip import destroy, qeye, tensor
import numpy as np
from matplotlib import pyplot as plt

# 定义常数
N = 10  # 维度
K = 300  # 非线性强度
P = 4 * K  # 双光子驱动强度
freq_p = 10000  # 驱动频率
freq_1 = 7000  # Q1 频率（MHz）
freq_c_ls = np.linspace(8000, 16000, 10)  # Coupler 频率
freq_2 = 7000  # Q2 频率
g_12 = 2
g_1c = 90
g_2c = 90
t = 10

# 定义算符
a = destroy(N)
I = qeye(N)

a1 = tensor(a, I, I)
ac = tensor(I, a, I)
a2 = tensor(I, I, a)

a1_dag = a1.dag()
ac_dag = ac.dag()
a2_dag = a2.dag()

E1 = list()
E2 = list()

# freq_1 * a1_dag * a1 + freq_2 * a2_dag * a2 + freq_c * ac_dag * ac \
for freq_c in freq_c_ls:
    # 建立哈密顿量
    freq_p_c = freq_c * 2
    H = \
        - K / 2 * a1_dag**2 * a1**2 - K / 2 * a2_dag**2 * a2**2 \
        + P / 2 * (a1_dag ** 2 * np.exp(-1j * freq_p/2 * 0) + a1 ** 2 * np.exp(1j * freq_p/2 * 0)) \
        + P / 2 * (a2_dag ** 2 * np.exp(-1j * freq_p/2 * 0) + a2 ** 2 * np.exp(1j * freq_p/2 * 0)) \
        + g_12 * (a1_dag * a2 + a1 * a2_dag) + + g_1c * (a1_dag * ac * np.exp(-1j * freq_1-freq_c * t)
                                                         + a1 * ac_dag * np.exp(1j * freq_1-freq_c * t)) \
        + g_2c * (a2_dag * ac * np.exp(-1j * freq_1-freq_c * t) + a2 * ac_dag * np.exp(1j * freq_1-freq_c * t))

    energies = H.eigenenergies()

    print(energies)

    E1.append(energies[1])
    E2.append(energies[2])

plt.figure()
plt.plot(freq_c_ls, E1)
plt.plot(freq_c_ls, E2)
plt.show()

