"""
KPO system

Rz(φ) gate simulation
"""

from qutip import coherent, destroy, qeye, mesolve
import numpy as np
from scipy import integrate
import krotov
from matplotlib import pyplot as plt
import pandas as pd

# 定义常数
N = 20  # 维度
delta = 0  # 失谐
K = 1  # 非线性强度
p0 = 4 * K  # 双光子驱动强度

p_ls = np.linspace(1, 10, 10) * K

# 定义算符
a = destroy(N)
a_dag = a.dag()
I = qeye(N)

# 判断双光子驱动是否改变
isChangeP_2 = True


def P(_t, _phi, _Tg, _p):
    """
    Two-photon driving amplitude
    """
    if isChangeP_2:
        # 引入绝热变驱动强度
        energy_gap = 4 * _p
        rate = 1 / (70 * energy_gap)

        # 线性变化
        t_mid = _Tg / 2
        if _t < t_mid:
            return _p + rate * _t
        else:
            return _p + rate * (_Tg - _t)

    else:
        # 不引入绝热变驱动
        return _p


def P_d(_t, _phi, _Tg, _p):
    """
    Driving pulse
    """
    return np.pi * _phi * np.sin(np.pi * _t / _Tg) / (8 * _Tg * np.sqrt(_p / K))


def gaussian(_t, _phi, _Tg, _p):
    """
    Gaussian wave
    """
    sigma = _Tg / 6
    # return (np.pi / 2) / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * (_t / sigma) ** 2)
    return 1 / np.sqrt((2 * np.pi * sigma ** 2)) * np.exp(-((_t - _Tg / 2) ** 2) / (2 * sigma ** 2))


def tempPulse(_t, _phi, _Tg, _p):
    """
    Temp pulse
    """
    return np.sqrt(P(_t, _phi, _Tg, _p) / K) * krotov.shapes.blackman(_t, 0, _Tg)


def blackman_pulse(_t, _phi, _Tg, _p):
    """
    black man pulse
    """
    sigma = _Tg / 6

    # 计算振幅
    # blackman_integ = integrate.quad(krotov.shapes.blackman, 0, _Tg, args=(0, _Tg))[0]
    integ = integrate.quad(tempPulse, 0, _Tg, args=(_phi, _Tg, _p))[0]

    amp = _phi / (integ * 4)
    # factor = _phi / (4 * np.sqrt(p0 / K))

    # amp = factor / blackman_integ

    return amp * krotov.shapes.blackman(_t, t_start=0, t_stop=_Tg)


def plot_wave(wave, tls, args):
    """
    plot wave
    """
    plt.figure(figsize=(16, 12), dpi=100)

    wave_sequence = []
    for _t in tls:
        wave_sequence.append(wave(_t, *args))

    plt.plot(tls, wave_sequence, linewidth=5)
    plt.xlabel('Time', fontsize=18)
    plt.ylabel('Amp', fontsize=18)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.show()


def ham(_t, args):
    """
    Hamiltonian
    """
    ham_1 = delta * a_dag * a + K / 2 * (a_dag ** 2) * (a ** 2) - P(_t, *args) / 2 * (a_dag ** 2 + a ** 2)
    ham_d = P_d(_t, *args) * (a + a_dag)

    return ham_1 + ham_d


def ham_black(_t, args):
    """
    Hamiltonian with black man wave
    """
    # ham_1 = delta * a_dag * a + K / 2 * (a_dag ** 2) * (a ** 2) - p0 / 2 * (a_dag ** 2 + a ** 2)
    ham_1 = delta * a_dag * a + K / 2 * (a_dag ** 2) * (a ** 2) - P(_t, *args) / 2 * (a_dag ** 2 + a ** 2)
    ham_blackman = blackman_pulse(_t, *args) * (a + a_dag)

    return ham_1 + ham_blackman


# 脉冲总时间
Tg_fold = 3
Tg = Tg_fold / K
Tg_fold_ls = np.linspace(1, 10, 20)
Tg_ls = Tg_fold_ls / K

# 期望的 Rz 门旋转角度
x = 1
phi = np.pi / x
phi_ls = np.linspace(-np.pi, np.pi, 21)


def logical_state(_phi, _Tg, _p):
    """
    Logical state
    """
    # 定义逻辑比特态
    alpha = np.sqrt(_p / K)
    logical_0 = coherent(N=N, alpha=alpha)
    logical_1 = coherent(N=N, alpha=-alpha)

    return logical_0, logical_1


def get_initial_state(_phi, _Tg, _p):
    """
    Initial state
    """
    # 逻辑比特
    logical_0, logical_1 = logical_state(_phi, _Tg, _p)
    # 初态
    return (logical_0 + logical_1).unit()


def get_ideal_final_state(_phi, _Tg, _p):
    """
    Ideal final state
    """
    # 逻辑比特
    logical_0, logical_1 = logical_state(_phi, _Tg, _p)
    phase_factor = 1j * _phi / 2
    return (logical_0 * np.exp(-phase_factor) + logical_1 * np.exp(phase_factor)).unit()


# 进行含时演化
fidelity_ls = []
fidelity_BLK_ls = []


def solve_fidelity(_ham, _initial_state, tls, args):
    """
    Solving fidelity
    """
    res = mesolve(_ham, _initial_state, tlist=tls, args=args)

    # 末态
    final_state = res.states[-1]

    ideal_state = get_ideal_final_state(*args)

    return np.abs(np.array(final_state.dag() * ideal_state)[0][0]) ** 2


# plot_wave(blackman_pulse, tlist, args=(phi, Tg))
# plot_wave(P_d, tlist, args=(phi, Tg))


def get_fidelity_ham(tls, _phi, _Tg, _p):
    initial_state = get_initial_state(_phi, _Tg, _p)
    return solve_fidelity(ham, initial_state, tls, args=(_phi, _Tg, _p))


def get_fidelity_ham_blk(tls, _phi, _Tg, _p):
    initial_state = get_initial_state(_phi, _Tg, _p)
    return solve_fidelity(ham_black, initial_state, tls, args=(_phi, _Tg, _p))


# 时间列表
# tlist = np.linspace(0, Tg, 100)
# plot_wave(P, tls=tlist, args=(phi, Tg, p0))
# 求解一系列参数下的保真度
# for phi in phi_ls:
#     isChangeP_2 = True
#     # fidelity = get_fidelity_ham(tlist, phi, Tg, p0)
#     # fidelity_ls.append(fidelity)
#     fidelity_BLK = get_fidelity_ham_blk(tlist, phi, Tg, p0)
#     fidelity_BLK_ls.append(fidelity_BLK)

energy_gap = 4 * p0
rate = 1 / (1 * energy_gap)
p0 = p0 + rate*(Tg/2)
tlist = np.linspace(0, Tg, 100)
# fidelity = get_fidelity_ham(tlist, phi, Tg, p0)
# fidelity_ls.append(fidelity)
isChangeP_2 = False
fidelity_BLK = get_fidelity_ham_blk(tlist, phi, Tg, p0)
fidelity_BLK_ls.append(fidelity_BLK)

# 原始脉冲保真度
# fidelity_ls = np.array(fidelity_ls)
# infidelity_ls = 1 - fidelity_ls

fidelity_BLK_ls = np.array(fidelity_BLK_ls)
infidelity_BLK_ls = 1 - fidelity_BLK_ls

print('BLK_Infi: \n', infidelity_BLK_ls)
# print('Ori_Infi: \n', infidelity_ls)

# 存储数据
# df = pd.DataFrame({'Infidelity_BLK': infidelity_BLK_ls, 'Infidelity_Ori': infidelity_ls})
# df = pd.DataFrame({'Infidelity_BLK': infidelity_BLK_ls})
# df.to_csv(f"Infidelity_Pchange_20.csv")
# df.to_csv(f"Infidelity_Pnotchange.csv")


# 绘图
def plot_Infi(x_ls, xlabel_name):
    """
    Plot infidelity as the function of x_ls
    """
    plt.figure(figsize=(16, 12), dpi=100)
    # plt.plot(x_ls, infidelity_ls, label='infidelity', linewidth=5)
    # plt.scatter(x_ls, infidelity_ls, linewidth=6)

    plt.plot(x_ls, infidelity_BLK_ls, label='infidelity_BLK', linewidth=5)
    plt.scatter(x_ls, infidelity_BLK_ls, linewidth=6)

    plt.xlabel(xlabel_name, fontsize=18)
    plt.ylabel('Infidelity', fontsize=18)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    plt.legend(fontsize=18)
    plt.show()


# plot_Infi(phi_ls, xlabel_name=r'$\phi$')
