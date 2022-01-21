from qutip import coherent, Qobj, sigmaz, qeye, basis, destroy
import numpy as np
from matplotlib import pyplot as plt
import krotov


class Wave(object):
    """
    产生波形
    """

    def __init__(self):
        # 默认波形: 20ns 脉冲为0的方波
        self.wave_form_ls = []

    def add_square_wave(self, t_start, t_stop, _amp, name='square'):
        """
        产生方波

        :param t_start: 脉冲开始时刻
        :param t_stop: 脉冲结束时刻
        :param _amp: 脉冲振幅
        :param name: 脉冲命名
        """
        # 时间切片的个数，ceil 取大于输入的最小整数
        steps = 4 * int(np.ceil(t_stop - t_start))
        # 时间切片
        tlist = np.linspace(t_start, t_stop, steps)

        # 生成脉冲波形
        wave_form = np.array([_amp for t in tlist])

        self.wave_form_ls.append([tlist, wave_form, name])

    def add_blackman(self, t_start, t_stop, _sigma, name='blackman'):
        """
        产生 blackman 脉冲

        :param t_start: 脉冲开始时刻
        :param t_stop: 脉冲结束时刻
        :param _sigma: 脉冲半高宽
        :param name: 脉冲命名
        """
        # blackman脉冲振幅
        _amp = amp(_sigma=_sigma)

        # 时间切片的个数，ceil 取大于输入的最小整数
        steps = 4 * int(np.ceil(t_stop - t_start))
        # 时间切片
        tlist = np.linspace(t_start, t_stop, steps)

        # 生成blackman脉冲波形
        wave_form = np.array([_amp * krotov.shapes.blackman(t, t_start=t_start, t_stop=t_stop) for t in tlist])

        self.wave_form_ls.append([tlist, wave_form, name])

    def plot_wave(self):
        """
        绘制脉冲波形
        """
        # 脉冲数量
        wave_num = len(self.wave_form_ls)

        # 绘图
        plt.figure(figsize=(15, 4*wave_num), dpi=80)
        for index, wave_form_info in enumerate(self.wave_form_ls):

            plt.subplot(int(f'{wave_num}1{index+1}'))
            tlist = wave_form_info[0]
            wave_form = wave_form_info[1]
            name = wave_form_info[2]

            plt.plot(tlist, wave_form, label=f'${name}$')
            plt.legend()
            plt.ylabel('Pulse Amp')

        plt.xlabel('t')
        plt.show()


def amp(_sigma):
    """
    求解脉冲振幅

    :param _sigma: sigma

    :return: 脉冲振幅
    """
    # Blackman pulse 积分前面的系数
    const = 1.56246130414  # 让积分为 pi
    _amp = const / (np.sqrt(2 * np.pi) * max([_sigma, 3]))

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
    _pauli_x = proj(basis(_dim, 0), basis(_dim, 1)) + proj(basis(_dim, 1), basis(_dim, 0))
    _pauli_y = 1j * (proj(basis(_dim, 1), basis(_dim, 0)) - proj(basis(_dim, 0), basis(_dim, 1)))
    _pauli_z = proj(basis(_dim, 0)) - proj(basis(_dim, 1))

    return [_pauli_i, _pauli_x, _pauli_y, _pauli_z]


def hamiltonian(_dim, _kerr, _omega, _amp):
    """
    生成哈密顿量(Rotating Frame)

    :param _dim: 维度
    :param _kerr: self-kerr系数 (非谐性)，单位 GHz
    :param _omega: 本征频率, 单位 GHz
    :param _amp: 驱动振幅

    :return: 哈密顿量
    """
    # 湮灭和创生算符
    a = destroy(_dim)
    a_dag = a.dag()

    # Drift term
    ham_d = (_kerr / 2) * (a_dag ** 2 * a ** 2)
    # Driving term
    ham_dr1 = a + a_dag
    ham_dr2 = a - a_dag

    amp_1 = lambda t, args: _amp
    amp_2 = lambda t, args: _amp

    _ham = [ham_d, [ham_dr1, amp_1], [ham_dr2, amp_2]]

    return _ham


if __name__ == '__main__':
    """
    所有系数定义均以 GHZ 为单位
    """
    # 维度
    dim = 3

    # 总时间
    T = 18 * 2
    sigma = T / 6
    # steps = 4 * int(np.ceil(T))  # 时间切片的个数，ceil 取大于输入的最小整数
    # 时间切片
    # tlist = np.linspace(0, T, steps)

    # 生成哈密顿量
    # 定义相关常数
    kerr_q = -2 * np.pi * 297e-3  # qubit 的非谐性
    omega_q = 6.2815 * 2 * np.pi  # qubit 本征频率
    amp_01 = 1  # 驱动振幅
    # 哈密顿量
    ham = hamiltonian(_dim=dim, _kerr=kerr_q, _omega=omega_q, _amp=amp_01)

    # 初始脉冲
    wave = Wave()
    wave.add_square_wave(t_start=0, t_stop=T, _amp=0, name='u_1(t)')
    wave.add_blackman(t_start=0, t_stop=T, _sigma=sigma, name='u_0(t)')
    wave.plot_wave()
