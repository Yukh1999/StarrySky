from qutip import destroy, qeye, tensor
import numpy as np
from matplotlib import pyplot as plt

# 定义常数
N = 100  # 维度
K = 300  # 非线性强度
P = 4 * K  # 双光子驱动强度
freq_p = 10000  # 驱动频率
freq_1 = 7000  # Q1 频率（MHz）
t = 0

# 定义算符
a1 = destroy(N)
I = qeye(N)

a1_dag = a1.dag()

# 失谐关于 K 的倍率
detuning_fold = np.linspace(0, 0.1, 50)
detuning_ls = detuning_fold * K


def plot_energy_levels(_energies):
    """
    Plotting the energy levels
    """

    _n = len(_energies)
    plt.figure()
    for i in range(_n):
        if i % 2 == 0:
            plt.hlines(y=_energies[i], xmin=0, xmax=1)
        else:
            plt.hlines(y=_energies[i], xmin=1.2, xmax=2.2)

    plt.show()

even_0 = []
even_1 = []
odd_0 = []
odd_1 = []
for detuning in detuning_ls:
    H = detuning * a1_dag * a1 \
        - K / 2 * a1_dag ** 2 * a1 ** 2 \
        + P / 2 * (a1_dag ** 2 * np.exp(-1j * freq_p / 2 * t) + a1 ** 2 * np.exp(1j * freq_p / 2 * t))

    energies = H.eigenenergies()

    n = len(energies)

    even_0.append(energies[n-1])
    odd_0.append(energies[n-2])

    even_1.append(energies[n-3])
    odd_1.append(energies[n-4])


even_0 = np.array(even_0)
even_1 = np.array(even_1)
odd_0 = np.array(odd_0)
odd_1 = np.array(odd_1)

plot_energy_levels(_energies=[even_0[0], odd_0[0], even_1[0], odd_1[0]])

# 绘图
fig, axs = plt.subplots(3, 1, sharex=True)


axs[0].plot(detuning_ls, even_1-even_0, label='even_diff')
axs[0].plot(detuning_ls, odd_1-odd_0, label='odd_diff')
axs[0].legend()


axs[1].plot(detuning_ls, even_0-odd_0, label='0_diff')
axs[1].legend()

print(even_0-odd_0)

axs[2].plot(detuning_ls, even_1-odd_1, label='1_diff')
axs[2].legend()


plt.xlabel('Dutuning')
plt.ylabel('Energy')

plt.show()
