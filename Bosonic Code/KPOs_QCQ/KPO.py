from qutip import destroy, qeye, tensor
import numpy as np
from matplotlib import pyplot as plt

# 定义常数
N = 20  # 维度
K = 300  # 非线性强度
P = 4 * K  # 双光子驱动强度
freq_p = 10000  # 驱动频率
freq_1 = 7000  # Q1 频率（MHz）
t = 0

# 定义算符
a1 = destroy(N)
I = qeye(N)

a1_dag = a1.dag()


H = \
    - K / 2 * a1_dag**2 * a1**2 \
    + P / 2 * (a1_dag ** 2 * np.exp(-1j * freq_p/2 * t) + a1 ** 2 * np.exp(1j * freq_p/2 * t))

energies = H.eigenenergies()

n = len(energies)

plt.figure()
for i in range(n-1):
    plt.hlines(y=energies[i], xmin=0, xmax=1)
    plt.hlines(y=energies[i+1], xmin=1.5, xmax=2.5)

plt.show()
