import matplotlib.pyplot as plt
from qutip import destroy, qeye, tensor
import numpy as np
from FloatQ_FloatC_Symmetry import freq_coupling
from scipy.optimize import root


def get_n_float(f_str, n):
    """
    保留小数点后 n 位，不进行四舍五入
    """
    f_str = str(f_str)  # f_str = '{}'.format(f_str) 也可以转换为字符串
    x, y, z = f_str.partition('.')
    z = (z + "0" * n)[:n]  # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
    return ".".join([x, z])


def plot_energies(_energies_open, _energies_close):
    """
    绘制能级图

    :param _energies_open: 耦合打开的能级
    :param _energies_close: 耦合关闭的能级
    """
    plt.figure(figsize=(13, 5), dpi=80)

    plt.subplot(121)
    for index, _energy in enumerate(_energies_open):
        color = 'red'
        plt.axhline(y=_energy, color=color)
        plt.ylim([7500, 7600])
        plt.ylabel('Energy(MHz)')
        plt.title('Coupling Opening')
        plt.xticks([])

    plt.subplot(122)
    for index, _energy in enumerate(_energies_close):
        color = 'blue'
        plt.axhline(y=_energy, color=color)
        plt.ylim([7500, 7600])
        plt.ylabel('Energy(MHz)')
        plt.title('Coupling Closing')
        plt.xticks([])

    plt.show()


def plot_freq_c(_ind_junc, freq_c):
    """
    绘制 coupler 频率随 coupler Lj 的变化
    :param _ind_junc: [list]不同Lj
    :param freq_c: [list]不同 Lj 下的 coupler 频率
    """
    plt.figure(figsize=(8, 5), dpi=80)
    plt.plot(_ind_junc, freq_c, label='Freq_coupler')
    plt.legend()
    plt.xlabel(r'$L_j(nH)$')
    plt.ylabel('Freq(MHz)')
    plt.show()


def plot_coupling_energy(_ind_junc, _energies):
    """
    绘制耦合强度和本征能量随 coupler Lj 的变化
    """
    plt.figure(figsize=(7, 10), dpi=80)
    energy_symmetric = []
    energy_asymmetric = []
    # print(_energies)
    for _energy in _energies:
        for energy_ in _energy:
            if get_n_float(energy_, 8) == '7567.54770353':
                energy_symmetric.append(energy_)
            else:
                energy_asymmetric.append(energy_)

    # 变为 ndarray，可以直接相减
    energy_symmetric = np.array(energy_symmetric)
    energy_asymmetric = np.array(energy_asymmetric)

    plt.subplot(211)
    # plt.plot(_ind_junc, energy_symmetric, label='Symmetric')
    plt.axhline(y=7567.54770353, label=r'$|01\rangle + |10\rangle$', color='orange')
    plt.plot(_ind_junc, energy_asymmetric, label=r'$|01\rangle - |10\rangle$', linestyle='--')
    plt.xlabel('$L_j(nH)$')
    plt.ylabel('Energy(MHz)')
    plt.legend()
    plt.xlim([3.5, 15])

    step_length = (15 - 3.5) / 100
    n = int(np.ceil((4.28905 - 3.5) / step_length))

    plt.fill_between(x=ind_junc_c_ls[n:], y1=energy_symmetric[n:], y2=energy_asymmetric[n:],
                     facecolor='yellow', alpha=0.2)
    plt.fill_between(x=ind_junc_c_ls[0:n + 1], y1=energy_symmetric[0:n + 1], y2=energy_asymmetric[0:n + 1],
                     facecolor='green', alpha=0.2)

    plt.subplot(212)
    coupling = (energy_asymmetric - energy_symmetric) / 2
    plt.plot(_ind_junc, coupling, label='Coupling Strength')
    plt.axhline(y=0, color='purple', linestyle='--')
    plt.axvline(x=4.37, color='purple', linestyle='--')
    plt.xlabel('$L_j(nH)$')
    plt.ylabel('Coupling Strength(MHz)')

    plt.legend()
    plt.show()


def zero_point(ind_junc_c):
    """
    寻找耦合为0的点
    """

    def coupling(Lj):
        res_ = freq_coupling(ind_junc_c=Lj * 1e-9)
        freq_c_ = res_['freq'][2] * 1e-6
        couplings_ = res_['coupling']

        # 单位为 MHz，需要乘1e-6
        ham_ = hamiltonian(freq_c=freq_c_, g_1c=couplings_[0] * 1e-6,
                           g_2c=couplings_[1] * 1e-6, g_12=couplings_[3] * 1e-6)
        energies_ = ham_.eigenenergies()

        coupling_ = energies_[3] - eigen_energies[2]

        return coupling_

    return root(fun=coupling, x0=ind_junc_c)


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
freq_c_close = 6.338236983066189e3
# 耦合常数
g_1c_close = -125.4393897364878
g_2c_close = -125.4393897364878
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


# 零点
# zero = zero_point(4.3)

# 求解不同coupler电感下的能级(MHz)
eigen_energies = []
freq_c_ls = []
ind_junc_c_ls = np.linspace(3.5, 15, 100)
for ind_junc in ind_junc_c_ls:
    res = freq_coupling(ind_junc_c=ind_junc * 1e-9)  # 电感从 nH 转化为 H
    _freq_c = res['freq'][2] * 1e-6
    couplings = res['coupling']

    # 单位为 MHz，需要乘1e-6
    _ham = hamiltonian(freq_c=_freq_c, g_1c=couplings[0] * 1e-6, g_2c=couplings[1] * 1e-6, g_12=couplings[3] * 1e-6)
    energies = _ham.eigenenergies()

    freq_c_ls.append(_freq_c)
    eigen_energies.append([energies[2], energies[3]])

# 绘制Freq_c随Lj变化图
plot_freq_c(_ind_junc=ind_junc_c_ls, freq_c=freq_c_ls)

# 绘制能级随Lj变化图
plot_coupling_energy(_ind_junc=ind_junc_c_ls, _energies=eigen_energies)

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
# print('energies_open: ', energies_open)
# print('energies_close: ', energies_close)
# # 能级差
# print('-' * 100)
# print('能级差')
# print('g_open: ', g_open / 2)
# print('g_close: ', g_close / 2)

# 绘制能级图
plot_energies(_energies_open=energies_open[2:4], _energies_close=energies_close[2:4])
