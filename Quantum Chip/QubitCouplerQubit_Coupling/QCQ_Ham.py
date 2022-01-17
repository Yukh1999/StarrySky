import matplotlib.pyplot as plt
from qutip import destroy, qeye, tensor
import numpy as np


def plot_energies(_energies_open, _energies_close):
    """
    绘制能级图

    :param _energies_open: 耦合打开的能级
    :param _energies_close: 耦合关闭的能级
    """
    plt.figure(figsize=(13, 8), dpi=80)

    plt.subplot(121)
    for index, _energy in enumerate(_energies_open):
        if index == 2 or index == 3:
            color = 'red'
        else:
            color = 'blue'
        plt.axhline(y=_energy, color=color)
        plt.ylabel('Energy(MHz)')
        plt.title('Coupling Opening')

    plt.subplot(122)
    for index, _energy in enumerate(_energies_close):
        if index == 2 or index == 3:
            color = 'red'
        else:
            color = 'blue'
        plt.axhline(y=_energy, color=color)
        plt.ylabel('Energy(MHz)')
        plt.title('Coupling Closing')

    plt.show()


# 维度
N = 2

# 湮灭创生算符
a = destroy(N)
a_dag = a.dag()

# 单位算符
iden = qeye(N)

# qubit 1
a_1 = tensor([a, iden, iden])
a_1_dag = a_1.dag()

# qubit 2
a_2 = tensor([iden, a, iden])
a_2_dag = a_2.dag()

# coupler
a_c = tensor([iden, iden, a])
a_c_dag = a_c.dag()

# 相关常数(MHz)
freq_1 = 7.5549413566083e3
freq_2 = 7.5549413566083e3

# 打开耦合
freq_c_open = 3.612354870502798e3
# 耦合常数(MHz)
g_1c_open = -94.74232984091866
g_2c_open = -94.74232984091866
g_12_open = -12.60634692464393

# 关闭耦合
freq_c_close = 6.39914575114707e3
# 耦合常数
g_1c_close = -126.04019856521623
g_2c_close = -126.04019856521623
g_12_close = -12.60634692464393


def hamiltonian(freq_c, g_1c, g_2c, g_12):
    """
    构建不同coupler调谐下的哈密顿量
    """
    # 构建哈密顿量
    ham = freq_1 * (a_1_dag * a_1) + freq_2 * (a_2_dag * a_2) + freq_c * (a_c_dag * a_c) \
          + g_1c * (a_1_dag * a_c + a_c_dag * a_1) + g_2c * (a_2_dag * a_c + a_c_dag * a_2) \
          + g_12 * (a_1_dag * a_2 + a_2_dag * a_1)

    return ham


# 哈密顿量
ham_open = hamiltonian(freq_c=freq_c_open, g_1c=g_1c_open, g_2c=g_2c_open, g_12=g_12_open)
ham_close = hamiltonian(freq_c=freq_c_close, g_1c=g_1c_close, g_2c=g_2c_close, g_12=g_12_close)

# 求解本征能谱
energies_open = ham_open.eigenenergies()
energies_close = ham_close.eigenenergies()

# 能量差
g_open = energies_open[3] - energies_open[2]
g_close = energies_close[3] - energies_close[2]

# 输出结果
# print('-' * 100)
# print('能谱')
# print(energies)
#
print('-' * 100)
print('能级差')
print('g_open: ', g_open / 2)
print('g_close: ', g_close / 2)


# 绘制能级图
plot_energies(_energies_open=energies_open[2:4], _energies_close=energies_close[2:4])


