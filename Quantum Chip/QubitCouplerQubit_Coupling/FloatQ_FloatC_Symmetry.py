from scipy.constants import hbar, elementary_charge as e
from GroundQ_GroundC import cap_ind_to_freq
import numpy as np
from matplotlib import pyplot as plt

# 相关常数
# 普朗克常量
h = hbar * 2 * np.pi
# 磁通量子
Phi_0 = h / (2 * e)
# 约化磁通量子
phi_0 = hbar / (2 * e)


def xi(E_C, E_J):
    """
    耦合强度计算中间常数

    :param E_C: 库柏对电容能
    :param E_J: 约瑟夫森电感能
    """
    return np.sqrt(2 * E_C / E_J)


# # 输入值
# # 自电容
# cap_q = 55.19e-15
# cap_c = 61.97e-15
#
# # 约瑟夫森电感
# ind_junc_q = 6e-9
#
# # 耦合关断: 6.399 GHz
# # ind_junc_c = 4.28905
# # 耦合打开: 3.61235 GHz
# # ind_junc_c = 13e-9
#
# # 对地电容
# cap_gq1 = 13.82e-15
# cap_gq2 = 401.11e-15
# cap_gq = 2 / (1 / cap_gq1 + 1 / cap_gq2)
# cap_gc = 152e-15
#
# # 互电容
# # qubit_1 和 coupler 互电容: qubit_1(1,2), coupler(3,4)
# cap_23 = 16.84e-15
# cap_14 = 0.08e-15
# cap_13 = 0.23e-15
# cap_24 = 2.75e-15
#
# # qubit_2 和 coupler 互电容: qubit_2(5,6), coupler(3,4)
# cap_35 = 2.75e-15
# cap_36 = 0.08e-15
# cap_46 = 0.23e-15
# cap_45 = 16.84e-15

# 输入值
# 自电容
cap_q = 51.72e-15
cap_c = 65.05e-15

# 约瑟夫森电感
ind_junc_q = 6e-9

# 耦合关断: 6.399 GHz
# ind_junc_c = 4.28905
# 耦合打开: 3.61235 GHz
# ind_junc_c = 13e-9

# 对地电容
cap_gq1 = 13.10e-15
cap_gq2 = 401.08e-15
cap_gq = 2 / (1 / cap_gq1 + 1 / cap_gq2)
cap_gc = 144.96e-15

# 互电容
# qubit_1 和 coupler 互电容: qubit_1(1,2), coupler(3,4)
cap_23 = 17.80e-15
cap_14 = 0.11e-15
cap_13 = 0.23e-15
cap_24 = 3.25e-15

# qubit_2 和 coupler 互电容: qubit_2(5,6), coupler(3,4)
cap_35 = 3.25e-15
cap_36 = 0.08e-15
cap_46 = 0.23e-15
cap_45 = 17.80e-15

# 自电容能
E_C1 = e ** 2 / (2 * cap_q + cap_gq)
E_C2 = E_C1
E_Cc = e ** 2 / (2 * cap_c + cap_gc)

# 互电容能计算中间常数
cap_eff = (2 * cap_q + cap_gq) * (2 * cap_c + cap_gc)
# 互电容能
E_12 = -(e ** 2 / (cap_gc * (2 * cap_q + cap_gq) * cap_eff)) * \
       (((cap_23 + cap_24) * (cap_45 + cap_35) + cap_24 * cap_35) * cap_c + (
               cap_23 * cap_35 + cap_45 * cap_24) * cap_gc)

E_1c = -e ** 2 * (cap_23 - cap_24) / cap_eff

E_2c = -e ** 2 * (cap_45 - cap_35) / cap_eff


def freq_coupling(ind_junc_c):
    """
    不同 coupler 电感值下的本征频率和耦合强度：模拟调频

    :param ind_junc_c: coupler 的电感

    :return: 所有的本征频率以及耦合强度[Dict]
    {
        'freq': [freq_q1, freq_q2, freq_c],
        'coupling': [g_1c, g_2c, g_eff, g_12, g]
    }
    """
    # 电感能
    E_J1 = phi_0 ** 2 / ind_junc_q
    E_J2 = E_J1
    E_Jc = phi_0 ** 2 / ind_junc_c

    # 耦合强度计算中间常数
    xi_1 = xi(E_C1, E_J1)
    xi_2 = xi(E_C2, E_J2)
    xi_c = xi(E_Cc, E_Jc)

    # 频率
    # 非线性修正
    freq_q1_ = (np.sqrt(8 * E_J1 * E_C1) - E_C1 * (1 + xi_1 / 4)) / h
    freq_q2_ = (np.sqrt(8 * E_J2 * E_C2) - E_C2 * (1 + xi_2 / 4)) / h
    freq_c_ = (np.sqrt(8 * E_Jc * E_Cc) - E_Cc * (1 + xi_c / 4)) / h

    # 耦合强度计算: 除 h 转化为频率(Hz)
    g_1c = ((E_1c / np.sqrt(2)) * (E_J1 * E_Jc / (E_C1 * E_Cc)) ** (1 / 4) * (1 - (1 / 8) * (xi_c + xi_1))) / h
    g_2c = ((E_2c / np.sqrt(2)) * (E_J2 * E_Jc / (E_C2 * E_Cc)) ** (1 / 4) * (1 - (1 / 8) * (xi_c + xi_2))) / h
    g_12 = ((E_12 / np.sqrt(2)) * (E_J1 * E_J2 / (E_C1 * E_C2)) ** (1 / 4) * (1 - (1 / 8) * (xi_1 + xi_2))) / h

    # 本征频率(Hz)
    freq_1 = cap_ind_to_freq(cap=cap_q + cap_gq / 2, ind_junc=ind_junc_q)
    freq_2 = freq_1
    freq_c = cap_ind_to_freq(cap=cap_c + cap_gc, ind_junc=ind_junc_c)

    # qubit 与 coupler 差频
    delta_1 = freq_c_ - freq_q1_
    delta_2 = delta_1

    # qubit 与 coupler 合频
    sum_1 = freq_c_ + freq_q1_
    sum_2 = sum_1

    # 等效耦合路径(Hz)
    g_eff = (g_1c * g_2c / 2) * (1 / delta_1 + 1 / sum_1 + 1 / delta_2 + 1 / sum_2)

    # qubit 之间总耦合强度
    g = g_12 - g_eff

    # 输出数据
    print('-' * 100)
    print('本征频率:')
    print('Qubit1_freq: ', freq_q1_ * 1e-9, 'GHz')
    print('Qubit2_freq: ', freq_q2_ * 1e-9, 'GHz')
    print('Coupler_freq: ', freq_c_ * 1e-9, 'GHz')
    print('-' * 100)
    print('Qubit非谐性: ', (E_C1 / h) * 1e-6, 'MHz')
    print('Coupler非谐性: ', (E_Cc / h) * 1e-6, 'MHz')
    print('-' * 100)
    print('耦合强度: ')
    print('g_1c: ', g_1c * 1e-6, 'MHz')
    print('g_2c: ', g_2c * 1e-6, 'MHz')
    print('g_eff: ', g_eff * 1e-6, 'MHz')
    print('g_12: ', g_12 * 1e-6, 'MHz')
    print('g: ', g * 1e-6, 'MHz')
    print('-' * 100)

    res = {
        'freq': [freq_q1_, freq_q2_, freq_c_],
        'coupling': [g_1c, g_2c, g_eff, g_12, g]
    }
    return res


def plot_detuning_coupling(ind_junc_c, detuning, coupling):
    """
    画出detuning和coupling随coupler电感的变化

    :param ind_junc_c: coupler电感
    :param detuning: qubit和 coupler的失谐(freq_c - freq_q)
    :param coupling: 总耦合强度
    """
    fig = plt.figure(figsize=(16, 13), dpi=80)

    # 第一条曲线
    ax1 = fig.add_subplot(111)
    ax1.plot(ind_junc_c, coupling, label='Coupling', color='r', linewidth=3)
    # 标定0耦合水平线
    ax1.axhline(y=0, linestyle='--', color='purple', linewidth=3)
    ax1.set_ylabel('Coupling(MHz)', fontsize=20)
    ax1.set_xlabel(r'$L_J$(nH)', fontsize=20)

    # 第二条曲线
    ax2 = ax1.twinx()
    ax2.plot(ind_junc_c, detuning, label='Detuning', linewidth=3)
    ax2.set_ylabel('Detuning(MHz)', fontsize=20)

    # 标定0耦合垂直线
    ax2.axvline(x=3.88, linestyle='--', color='purple', linewidth=3)

    plt.setp(ax1.get_xticklabels(), size=20)
    plt.setp(ax1.get_yticklabels(), size=20)
    plt.setp(ax2.get_yticklabels(), size=20)

    bwith = 3
    ax1.spines['bottom'].set_linewidth(bwith)
    ax1.spines['left'].set_linewidth(bwith)
    ax1.spines['top'].set_linewidth(bwith)
    ax1.spines['right'].set_linewidth(bwith)

    ax1.tick_params(which='major', width=3)
    ax2.tick_params(which='major', width=3)

    fig.legend(loc=1, bbox_to_anchor=(0.5, 1), bbox_transform=ax1.transAxes, fontsize=20)
    plt.show()


def plot_coupling_qc(coupler_freq, coupling_1c, coupling_2c):
    """
    绘制 g_1c, g_2c 随 coupler 频率的变化

    :param coupler_freq: coupler的频率列表
    :param coupling_1c: g_1c
    :param coupling_2c: g_2c
    """
    # 绘图
    plt.figure(figsize=(10, 6), dpi=80)

    plt.plot(coupler_freq, coupling_1c, label='$g_{qc}$')
    plt.xlabel('Freq_coupler (GHz)', fontsize=15)
    plt.ylabel('$g_{qc}$(MHz)', fontsize=15)

    plt.legend(fontsize='20')

    plt.show()


# 定义coupler电感变化的范围
ind_junc_c_list = np.linspace(3.5, 20, 100)
# 计算不同coupler电感下的频率以及耦合强度
detuning_list = []
coupling_list = []

for _ind_junc_c in ind_junc_c_list:
    res = freq_coupling(ind_junc_c=_ind_junc_c * 1e-9)
    freq = res['freq']
    coupling = res['coupling'][4] * 1e-6
    detuning = (freq[0] - freq[2]) * 1e-6

    detuning_list.append(detuning)
    coupling_list.append(coupling)

# 绘图
plot_detuning_coupling(ind_junc_c_list, detuning_list, coupling_list)

if __name__ == '__main__':
    coupler_freq_ls = []
    coupling_1c_ls = []
    coupling_2c_ls = []
    for ind_junc_c in ind_junc_c_list:
        res = freq_coupling(ind_junc_c=ind_junc_c * 1e-9)
        coupler_freq_ls.append(res['freq'][2] * 1e-9)
        coupling_1c_ls.append(res['coupling'][0] * 1e-6)
        coupling_2c_ls.append(res['coupling'][1] * 1e-6)

    # plot_coupling_qc(coupler_freq_ls, coupling_1c_ls, coupling_2c_ls)

    freq_coupling(ind_junc_c=20e-9)
# 输出数据
# print('-' * 100)
# print('本征频率:')
# print('Qubit1_freq: ', freq_q1_ * 1e-9, 'GHz')
# print('Qubit2_freq: ', freq_q2_ * 1e-9, 'GHz')
# print('Coupler_freq: ', freq_c_ * 1e-9, 'GHz')
# print('-' * 100)
# print('耦合强度: ')
# print('g_1c: ', g_1c * 1e-6, 'MHz')
# print('g_2c: ', g_2c * 1e-6, 'MHz')
# print('g_eff: ', g_eff * 1e-6, 'MHz')
# print('g_12: ', g_12 * 1e-6, 'MHz')
# print('g: ', g * 1e-6, 'MHz')
# print('-' * 100)
