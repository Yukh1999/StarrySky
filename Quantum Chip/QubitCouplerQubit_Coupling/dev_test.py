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

    :param cap_q: 关于 qubit 的电容参数
    [cap_12 (qubit 两个板之间的互电容), cap_gq1 (qubit 小板对地电容), cap_gq2 (qubit 大板对地电容)]
    :param cap_c: 关于 coupler 的电容参数
    [cap_34 (coupler 两个板之间的互电容), cap_gc (coupler 其中的一个板的对地电容)]
    :param cap_qc: qubit 与 coupler 之间的互电容参数
    [cap_13 (qubit1 小板与 coupler 的强耦合电容), cap_14 (qubit1 小板与 coupler 的弱耦合电容),
    cap_23 (qubit1 大板与 coupler 的强耦合电容), cap_24 (qubit1 大板与 coupler 的弱耦合电容)，
    cap_53 (qubit2 大板与 coupler 的弱耦合电容), cap_54 (qubit2 大板与 coupler 的强耦合电容),
    cap_63 (qubit2 小板与 coupler 的弱耦合电容), cap_64 (qubit2 小板与 coupler 的强耦合电容)]
    :param ind_junc_q: qubit 的约瑟夫森电感
    :param ind_junc_c: coupler 的约瑟夫森电感

    :return: [qubit 1
    """
