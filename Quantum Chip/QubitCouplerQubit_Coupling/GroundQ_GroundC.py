from scipy.constants import hbar, elementary_charge as e
import numpy as np


def freq_ind_to_cap(freq, ind_junc):
    """
    利用频率和电感计算电容：这里只求解线性部分，暂时不考虑非线性修正，约瑟夫森结当做一个线性电感来处理

    :param freq: 频率(Hz)
    :param ind_junc: 约瑟夫森电感(H)

    :return: 电容值(F)
    """

    omega = freq * np.pi * 2

    cap = 1 / (ind_junc * omega ** 2)

    return cap


def cap_ind_to_freq(cap, ind_junc):
    """
    利用电容、约瑟夫森电感求解本征频率

    :param cap: 电容值(F)
    :param ind_junc: 约瑟夫森电感(H)

    :return: 本征频率(Hz)
    """
    omega = 1 / np.sqrt(cap * ind_junc)
    freq = omega / (2 * np.pi)

    return freq


def coup_stength_to_cap(cap1, cap2, ind_junc1, ind_junc2, coup_strength):
    """
    已知两个元件自电容、约瑟夫森电感，求解需要的耦合强度对应的耦合电容大小

    :param cap1: 第一个器件的电容(F)
    :param cap2: 第二个器件的电容(F)
    :param ind_junc1: 第一个器件的约瑟夫森电感(H)
    :param ind_junc2: 第二个器件的约瑟夫森电感(H)
    :param coup_strength: 需要的耦合强度

    :return: 耦合电容(F)
    """

    # 两个器件的本征频率
    freq1 = cap_ind_to_freq(cap=cap1, ind_junc=ind_junc1)
    freq2 = cap_ind_to_freq(cap=cap2, ind_junc=ind_junc2)

    # 耦合电容计算
    a = 1 - freq1 * freq2 / (4 * coup_strength ** 2)
    b = cap1 + cap2
    c = cap1 * cap2
    cap = (-b - np.sqrt(b ** 2 - 4 * a * c)) / (2 * a)

    return cap


def coup_cap_to_strength(cap1, cap2, ind_junc1, ind_junc2, coup_cap):
    """
    已知两个元件的自电容、约瑟夫森电感以及两个元件间的互电容，求解耦合强度

    :param cap1: 第一个元件的自电容(F)
    :param cap2: 第二个元件的自电容(F)
    :param ind_junc1: 第一个元件的约瑟夫森电感(H)
    :param ind_junc2: 第二个元件的约瑟夫森电感(H)
    :param coup_cap: 两个元件之间的耦合互电容(F)

    :return: 耦合强度(Hz)
    """

    # 两个元件的本征频率
    freq1 = cap_ind_to_freq(cap=cap1, ind_junc=ind_junc1)
    freq2 = cap_ind_to_freq(cap=cap2, ind_junc=ind_junc2)

    # 耦合强度
    coup_strength = coup_cap * np.sqrt(freq1 * freq2) / (2 * np.sqrt((cap1 + coup_cap) * (cap2 + coup_cap)))

    return coup_strength


def anharm(cap):
    """
    利用电容计算非谐性

    :param cap: 电容(F)

    :return: 非谐性(Hz)
    """

    # 普朗克常数
    h = hbar / (2 * np.pi)

    # 非谐性
    anharmonicity = e**2 / (cap * 2) / h

    return anharmonicity


if __name__ == '__main__':
    # 自电容
    cap_q1 = 70e-15
    cap_q2 = 70e-15
    cap_c = 45e-15

    # 耦合电容
    cap_12 = 0.00063e-15
    cap_1c = 0.03315e-15
    cap_2c = cap_1c

    # 约瑟夫森电感
    ind_junc_q1 = 10e-9
    ind_junc_q2 = 10e-9
    ind_junc_c = 16e-9

    # 本征频率
    freq1 = cap_ind_to_freq(cap=cap_q1, ind_junc=ind_junc_q1)
    print(freq1 * 1e-9, 'GHz')
