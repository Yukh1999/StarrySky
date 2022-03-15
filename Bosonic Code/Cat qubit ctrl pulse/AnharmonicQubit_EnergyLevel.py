from qutip import destroy
import numpy as np
from matplotlib import pyplot as plt

# 相关常数
N = 10  # 维度
omega = 1  # 本征频率
kerr = np.linspace(0, 1, 100)  # 自克尔系数：非谐性

# 升降算符
a = destroy(N=N)
a_dag = a.dag()

# 初始化不同能级的本征能量
energy_0 = []
energy_1 = []
energy_2 = []


# 求解本征能量
def eigen_energy(_kerr):
    """
    求解不同 kerr 系数下的本征能量

    :param _kerr: kerr 系数

    :return: [energy_0, energy_1, energy_2]
    """

    # 构建哈密顿量
    ham = omega * (a_dag * a) + (_kerr / 2) * (a_dag ** 2 * a ** 2)

    # 本征能量
    energies = ham.eigenenergies()

    # 返回前三个能级的能量
    return [energies[i] for i in range(3)]


# 求解不同 kerr 系数下，不同能级的本征能量
for k in kerr:
    energy = eigen_energy(_kerr=k)
    energy_0.append(energy[0])
    energy_1.append(energy[1])
    energy_2.append(energy[2])

# 绘制不同 kerr 系数下的能级图
plt.figure(figsize=(16, 9), dpi=80)
plt.plot(kerr, energy_0, label='ground')
plt.plot(kerr, energy_1, label='excited_1')
plt.plot(kerr, energy_2, label='excited_2')

plt.legend()
plt.show()
