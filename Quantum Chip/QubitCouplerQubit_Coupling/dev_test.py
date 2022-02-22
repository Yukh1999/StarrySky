from scipy.constants import hbar, elementary_charge as e
from GroundQ_GroundC import cap_ind_to_freq
import numpy as np
from matplotlib import pyplot as plt
from typing import List, Dict

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


def character_params(cap_q: List[float], cap_c: List[float], cap_qc: List, ind_junc_q: float, ind_junc_c: float):
    """
    利用Q3D仿真的电容矩阵，计算QCQ结构的特征参量

    :param cap_q: qubit 的电容参数
    [cap_12 (qubit 两个板之间的互电容), cap_gq1 (qubit 小板对地电容), cap_gq2 (qubit 大板对地电容)]
    :param cap_c: coupler 的电容参数
    [cap_34 (coupler 两个板之间的互电容), cap_gc (coupler 其中的一个板的对地电容)]
    :param cap_qc: qubit 与 coupler 之间的互电容参数
    [cap_13 (qubit1 小板与 coupler 的强耦合电容), cap_14 (qubit1 小板与 coupler 的弱耦合电容),
    cap_23 (qubit1 大板与 coupler 的强耦合电容), cap_24 (qubit1 大板与 coupler 的弱耦合电容)，
    cap_53 (qubit2 大板与 coupler 的弱耦合电容), cap_54 (qubit2 大板与 coupler 的强耦合电容),
    cap_63 (qubit2 小板与 coupler 的弱耦合电容), cap_64 (qubit2 小板与 coupler 的强耦合电容)]
    :param ind_junc_q: qubit 的约瑟夫森电感
    :param ind_junc_c: coupler 的约瑟夫森电感

    :return: {
                'freq': [freq_q1, freq_q2, freq_c],
                'anharm': [anharm_q1, anharm_q2, coupler],
                'coupling': [g_1c, g_2c, g_eff, g_12, g]
            }
    """
    # Qubit 电容信息
    # 两个板之间电容
    cap_12 = cap_56 = cap_q[0]
    # 两个板的对地电容
    cap_gq1 = cap_q[1]  # 小板对地电容
    cap_gq2 = cap_q[2]  # 大板对地电容
    # Qubit 等效对地电容
    cap_gq = 2 / (1 / cap_gq1 + 1 / cap_gq2)

    # Coupler 电容信息
    # 两个板之间电容
    cap_34 = cap_c[0]
    # 单个板对地电容
    cap_gc = cap_c[1]

    # Qubit 与 Coupler 耦合电容
    # Qubit_1 与 Coupler 互电容: Qubit_1(1,2), Coupler(3,4)
    cap_13 = cap_qc[0]
    cap_14 = cap_qc[1]
    cap_23 = cap_qc[2]
    cap_24 = cap_qc[3]

    # Qubit_2 与 Coupler 互电容: Qubit_2(5,6), Coupler(3,4)
    cap_53 = cap_qc[4]
    cap_54 = cap_qc[5]
    cap_63 = cap_qc[6]
    cap_64 = cap_qc[7]

    # 自电容能
    E_C1 = e ** 2 / (2 * cap_12 + cap_gq)
    E_C2 = E_C1
    E_Cc = e ** 2 / (2 * cap_34 + cap_gc)

    # 互电容能计算中间常数
    cap_eff = (2 * cap_12 + cap_gq) * (2 * cap_34 + cap_gc)
    # 互电容能
    E_12 = -(e ** 2 / (cap_gc * (2 * cap_12 + cap_gq) * cap_eff)) * \
           (((cap_23 + cap_24) * (cap_54 + cap_53) + cap_24 * cap_53) * cap_c + (
                   cap_23 * cap_53 + cap_54 * cap_24) * cap_gc)

    E_1c = -e ** 2 * (cap_23 - cap_24) / cap_eff

    E_2c = -e ** 2 * (cap_54 - cap_53) / cap_eff
