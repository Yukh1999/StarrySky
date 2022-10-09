"""
KPO system

Rz(φ) gate simulation
"""

from qutip import coherent, destroy, qeye, mesolve, Qobj
import numpy as np
from scipy import integrate
import krotov
from matplotlib import pyplot as plt
import pandas as pd

# 定义常数
N = 40  # 维度
delta = 0  # 失谐
K = 1  # 非线性强度
p0 = 2 * K  # 双光子驱动强度


# 定义算符
a = destroy(N)
a_dag = a.dag()
I = qeye(N)

# 判断双光子驱动是否改变
isChangeP_2 = True
# 改变速率的全局变量
rate_fold = 10


def P(_t, _phi, _Tg, _p):
    """
    Two-photon driving amplitude：双光子驱动脉冲
    """
    if isChangeP_2:
        # 引入绝热变驱动强度
        energy_gap = 4 * _p
        rate = 1 / (rate_fold * energy_gap)

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
    Driving pulse：原始文献的驱动脉冲
    """
    return np.pi * _phi * np.sin(np.pi * _t / _Tg) / (8 * _Tg * np.sqrt(_p / K))


def gaussian(_t, _phi, _Tg, _p):
    """
    Gaussian wave
    """
    sigma = _Tg / 6
    # return (np.pi / 2) / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * (_t / sigma) ** 2)
    return 1 / np.sqrt((2 * np.pi * sigma ** 2)) * np.exp(-((_t - _Tg / 2) ** 2) / (2 * sigma ** 2))


def tempPulse_3(_t, _phi, _Tg, _p):
    """
    Temp pulse: 执行 Rz 加入三光子驱动脉冲时的情况
    """
    # return np.sqrt(P(_t, _phi, _Tg, _p) / K) * krotov.shapes.blackman(_t, 0, _Tg)
    # 三光子驱动
    return (np.sqrt(P(_t, _phi, _Tg, _p) / K) ** 3) * krotov.shapes.blackman(_t, 0, _Tg)


def tempPulse(_t, _phi, _Tg, _p):
    """
    Temp pulse: 计算相位时的每一时刻被积函数
    """
    return np.sqrt(P(_t, _phi, _Tg, _p) / K) * krotov.shapes.blackman(_t, 0, _Tg)


def blackman_pulse_3(_t, _phi, _Tg, _p):
    """
    black man pulse: 计算加入三光子驱动时的 black man 脉冲波形
    """
    sigma = _Tg / 6

    # 计算振幅
    # blackman_integ = integrate.quad(krotov.shapes.blackman, 0, _Tg, args=(0, _Tg))[0]
    integ = integrate.quad(tempPulse_3, 0, _Tg, args=(_phi, _Tg, _p))[0]

    amp = _phi / (integ * 4)
    # factor = _phi / (4 * np.sqrt(p0 / K))

    # amp = factor / blackman_integ

    return amp * krotov.shapes.blackman(_t, t_start=0, t_stop=_Tg)


def blackman_pulse(_t, _phi, _Tg, _p):
    """
    black man pulse：生成合适的 black man 脉冲
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
    Hamiltonian：原始文献的驱动脉冲对应的哈密顿量
    """
    ham_1 = delta * a_dag * a + K / 2 * (a_dag ** 2) * (a ** 2) - P(_t, *args['args']) / 2 * (a_dag ** 2 + a ** 2)
    ham_d = P_d(_t, *args['args']) * (a ** 1 + a_dag ** 1)

    return ham_1 + ham_d


def ham_black_3(_t, args):
    """
    Hamiltonian with black man wave：三光子驱动时的 black man 脉冲波形
    """
    # ham_1 = delta * a_dag * a + K / 2 * (a_dag ** 2) * (a ** 2) - p0 / 2 * (a_dag ** 2 + a ** 2)
    ham_1 = delta * a_dag * a + K / 2 * (a_dag ** 2) * (a ** 2) - P(_t, *args['args']) / 2 * (a_dag ** 2 + a ** 2)
    ham_blackman = blackman_pulse_3(_t, *args['args']) * (a ** 3 + a_dag ** 3)

    return ham_1 + ham_blackman


def ham_black(_t, args):
    """
    Hamiltonian with black man wave：将原始文献中的波形换为 black man 脉冲后的脉冲波形
    """
    # ham_1 = delta * a_dag * a + K / 2 * (a_dag ** 2) * (a ** 2) - p0 / 2 * (a_dag ** 2 + a ** 2)
    ham_1 = delta * a_dag * a + K / 2 * (a_dag ** 2) * (a ** 2) - P(_t, *args['args']) / 2 * (a_dag ** 2 + a ** 2)
    ham_blackman = blackman_pulse(_t, *args['args']) * (a ** 1 + a_dag ** 1)

    return ham_1 + ham_blackman


# 脉冲总时间
Tg_fold = 2
Tg = Tg_fold / K

# 期望的 Rz 门旋转角度
x = 5 / 8
phi = np.pi * x
phi_ls = np.linspace(-np.pi, np.pi, 11)


def logical_state(_phi, _Tg, _p):
    """
    Logical state
    """
    # 定义逻辑比特态
    alpha = np.sqrt(_p / K)
    logical_0 = coherent(N=N, alpha=alpha)
    logical_1 = coherent(N=N, alpha=-alpha)

    return logical_0, logical_1


def get_initial_dmatrix(_phi, _Tg, _p):
    """
    Initial state
    """
    # 逻辑比特
    logical_0, logical_1 = logical_state(_phi, _Tg, _p)
    # 初态
    initial_state = (logical_0 + logical_1).unit()

    # 初态密度矩阵
    initial_rho = initial_state * initial_state.dag()
    return initial_rho.unit()


def get_ideal_final_dmatrix(_phi, _Tg, _p):
    """
    Ideal final state
    """
    # 逻辑比特
    logical_0, logical_1 = logical_state(_phi, _Tg, _p)

    # 旋转相位
    phase_factor = 1j * _phi / 2

    # 末态
    final_state = (logical_0 * np.exp(-phase_factor) + logical_1 * np.exp(phase_factor)).unit()

    # 末态密度矩阵
    final_rho = final_state * final_state.dag()
    return final_rho.unit()


def get_fidelity(rho: Qobj, ideal_rho: Qobj):
    """
    计算演化末态与理想末态的保真度
    """
    # 计算保真度
    rho = rho.unit()
    ideal_rho = ideal_rho.unit()
    fidelity = np.abs((((rho.sqrtm() * ideal_rho * rho.sqrtm()).sqrtm()).tr()) ** 2)

    # 计算失真度
    return fidelity





def solve_fidelity(_ham, _initial_rho, tls, args):
    """
    Solving fidelity
    """

    # 求解态演化
    res = mesolve(H=_ham, rho0=_initial_rho,  tlist=tls, c_ops=[K/20*a], args={'args': args})

    # 末态
    final_rho = res.states[-1]

    ideal_rho = get_ideal_final_dmatrix(*args)

    return get_fidelity(rho=final_rho, ideal_rho=ideal_rho)


# plot_wave(blackman_pulse, tlist, args=(phi, Tg))
# plot_wave(P_d, tlist, args=(phi, Tg))


def get_fidelity_ham(tls, _phi, _Tg, _p):
    initial_rho = get_initial_dmatrix(_phi, _Tg, _p)
    return solve_fidelity(ham, initial_rho, tls, args=(_phi, _Tg, _p))


def get_fidelity_ham_blk(tls, _phi, _Tg, _p):
    initial_rho = get_initial_dmatrix(_phi, _Tg, _p)
    return solve_fidelity(ham_black, initial_rho, tls, args=(_phi, _Tg, _p))


def get_fidelity_ham_blk_3(tls, _phi, _Tg, _p):
    initial_rho = get_initial_dmatrix(_phi, _Tg, _p)
    return solve_fidelity(ham_black_3, initial_rho, tls, args=(_phi, _Tg, _p))


# 求解不同 rate 下的最大驱动强度
energy_gap = 4 * p0


def P0(_n, isPmax=True):
    """
    P0: 无用函数
    """
    if isPmax:
        rate = 1 / (_n * energy_gap)
        p0_ = p0 + rate * (Tg / 2)
        return p0_, False
    else:
        return p0, True


# 时间列表
tlist = np.linspace(0, Tg, 100)
plot_wave(P, tls=tlist, args=(phi, Tg, p0))


# 进行含时演化
fidelity_ls = []
fidelity_2fold_ls = []

fidelity_BLK_ls = []
fidelity_BLK_Pchange = []
fidelity_BLK_Pmax = []
fidelity_BLK_P0 = []
fidelity_BLK_P0_2fold = []

# 求解一系列参数下的保真度
for i, phi in enumerate(phi_ls):
    # isChangeP_2 = True
    # fidelity_BLK_Pchange.append(get_fidelity_ham_blk(tlist, phi, Tg, p0))
    #
    isChangeP_2 = False
    # fidelity_BLK_P0.append(get_fidelity_ham_blk(tlist, phi, Tg, p0))
    #
    # # BLK 脉冲的双光子驱动提升两倍
    # fidelity_BLK_P0_2fold.append(get_fidelity_ham_blk(tlist, phi, Tg, p0*2))

    # 原始论文中的单光子脉冲计算保真度
    fidelity_ls.append(get_fidelity_ham(tlist, phi, Tg, p0))

    fidelity_2fold_ls.append(get_fidelity_ham(tlist, phi, Tg, p0*1.5))



infidelity_ls = 1 - np.array(fidelity_ls)


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

    linewidth = 3
    scatterwidth = 2

    # blk 脉冲方法
    # plt.plot(x_ls, fidelity_BLK_Pchange, label='Pchange', linewidth=linewidth)
    # plt.scatter(x_ls, fidelity_BLK_Pchange, linewidth=scatterwidth)
    #
    # plt.plot(x_ls, fidelity_BLK_P0, label='P0', linewidth=linewidth)
    # plt.scatter(x_ls, fidelity_BLK_P0, linewidth=scatterwidth)
    #
    # plt.plot(x_ls, fidelity_BLK_P0_2fold, label='2P0', linewidth=linewidth)
    # plt.scatter(x_ls, fidelity_BLK_P0_2fold, linewidth=scatterwidth)

    # 原始论文方法
    plt.plot(x_ls, fidelity_ls, label='Ori', linewidth=linewidth)
    plt.scatter(x_ls, fidelity_ls, linewidth=scatterwidth)

    plt.plot(x_ls, fidelity_2fold_ls, label='Ori_2P0', linewidth=linewidth)
    plt.scatter(x_ls, fidelity_2fold_ls, linewidth=scatterwidth)

    plt.xlabel(xlabel_name, fontsize=18)
    plt.ylabel('Infidelity', fontsize=18)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    plt.legend(fontsize=18)
    plt.show()


print('ori:', fidelity_ls)
print('ori_2P0', fidelity_2fold_ls)

print('Pchange:', fidelity_BLK_Pchange)

print('BLK_P0:', fidelity_BLK_P0)

print('BLK_2P0:', fidelity_BLK_P0_2fold)

plot_Infi(phi_ls, xlabel_name=r'$\phi$')
