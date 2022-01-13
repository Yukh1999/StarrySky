from qutip import coherent, Qobj, sigmaz, qeye, basis
import numpy as np
from matplotlib import pyplot as plt


def amp(_sigma):
    """
    求解脉冲振幅
    """
    # Blackman pulse 积分前面的系数
    const = 1.56246130414  # 让积分为 pi
    _amp = const / (np.sqrt(2 * np.pi) * np.max(_sigma, 3))

    return _amp


def proj(_psi, _phi=None):
    """
    构建投影算符，将 _phi 投影到 _psi 上，
    如果 _phi=None，构建将任意态投影到 _psi 上的投影算符。

    :param _psi: 投影到 _psi 上
    :param _phi: 被投影的态

    :return: 投影算符 |psi)(phi|

    """

    if _phi is None:
        return _psi * _psi.dag()
    else:
        return _psi * _phi.dag()


def pauli_oper(_dim):
    """
    构建维度为 _dim 的 0,1 子空间 pauli 算符

    :param _dim: 维度

    :return: 子空间 pauli 算符 [I, X, Y, Z]
    """
    _pauli_i = qeye(_dim)
    _pauli_x = proj(basis(_dim, 0), basis(_dim, 1)) - proj(basis(_dim, 1), basis(_dim, 0))
    _pauli_y = 1j * (proj(basis(_dim, 1), basis(_dim, 0)) - proj(basis(_dim, 0), basis(_dim, 1)))
    _pauli_z = proj(basis(_dim, 0)) - proj(basis(_dim, 1))

    return [_pauli_i, _pauli_x, _pauli_y, _pauli_z]


if __name__ == '__main__':
    # 维度
    dim = 3

    # 系数计算
    sigma_max = 3  # 振幅取 max 时，sigma=3
    amp_max = amp(_sigma=sigma_max)

    # 总时间
    T = 18 * 2
    sigma = T / 6
    steps = 4 * int(np.ceil(T))  # ceil 取大于输入的最小整数
    # 时间切片
    tlist = np.linspace(0, T, steps)


