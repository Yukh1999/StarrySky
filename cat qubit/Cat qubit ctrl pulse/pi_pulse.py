from qutip import coherent, Qobj, sigmaz, qeye, basis, destroy, Options, expect
import numpy as np
from matplotlib import pyplot as plt
import krotov


class Pulse(object):
    """
    产生脉冲波形
    """

    @staticmethod
    def square_wave(t, t_start, t_stop, _amp):
        """
        产生方波

        :param t: t时刻
        :param t_start: 脉冲开始时刻
        :param t_stop: 脉冲结束时刻
        :param _amp: 脉冲振幅

        :return: t时刻的振幅
        """
        return _amp

    def blackman_wave(self, t, t_start, t_stop, _sigma):
        """
        产生 blackman 脉冲

        :param t: t时刻
        :param t_start: 脉冲开始时刻
        :param t_stop: 脉冲结束时刻
        :param _sigma: 脉冲半高宽

        :return: t时刻的振幅
        """
        # blackman脉冲振幅
        _amp = self.amp(_sigma=_sigma)

        return _amp * krotov.shapes.blackman(t, t_start=t_start, t_stop=t_stop)

    @staticmethod
    def amp(_sigma):
        """
        求解blackman脉冲振幅

        :param _sigma: sigma

        :return: 脉冲振幅
        """
        # Blackman pulse 积分前面的系数
        const = 1.56246130414  # 让积分为 pi
        _amp = const / (np.sqrt(2 * np.pi) * max([_sigma, 3]))

        return _amp


class Hamiltonian(Pulse):
    """
    Rotating Frame 下的体系哈密顿量
    """

    def __init__(self, _dim):
        """
        :param _dim: 希尔伯特空间维度
        """
        self.driving_ls = []
        self.ham_drift = None
        self.dim = _dim
        self.a = destroy(_dim)
        self.a_dag = self.a.dag()

    def add_drift(self, kerr):
        """
        漂移项

        :param kerr: 非谐性(self-kerr)，单位GHz
        """
        a = self.a
        a_dag = self.a_dag

        ham_drift = (kerr / 2) * (a_dag ** 2 * a ** 2)

        self.ham_drift = ham_drift

    def ham_driving(self, channel: str):
        """
        驱动哈密顿量算符

        :param channel: 驱动添加通道 (x, y, z)

        :return: 对应通道的哈密顿量算符
        """
        a = self.a
        a_dag = self.a_dag
        if channel == 'x':
            ham_driving = a + a_dag
        elif channel == 'y':
            ham_driving = 1j * (a_dag - a)
        elif channel == 'z':
            ham_driving = 2 * (a_dag * a) + 1
        else:
            raise Exception('Wrong input! Please input x, y or z')

        return ham_driving

    def add_square_driving(self, channel: str, t_start: float, t_stop: float, _amp: float, steps=None):
        """
        添加方波驱动

        :param channel: 脉冲添加通道 (x, y, z)
        :param t_start: 脉冲开始时间 (单位ns)
        :param t_stop: 脉冲结束时间 (单位ns)
        :param _amp: 脉冲振幅
        :param steps: 时间切片数量
        """
        # 时间切片的个数，ceil 取大于输入的最小整数
        if steps is None:
            steps = 4 * int(np.ceil(t_stop - t_start))
        # 时间切片
        tlist = np.linspace(t_start, t_stop, steps)

        # 驱动脉冲
        def driving_pulse(t, args=None):
            """
            驱动脉冲函数: t时刻的脉冲振幅

            :param t: t时刻
            :param args: 相关参数，一般不填，为了krotov算法而设置

            :return: t时刻的脉冲振幅
            """
            return self.square_wave(t, t_start=t_start, t_stop=t_stop, _amp=_amp)

        # 驱动信息 [驱动哈密顿量, [时间列表, 脉冲波形函数], 驱动通道]
        driving_info = [self.ham_driving(channel=channel), [tlist, driving_pulse], channel]

        self.driving_ls.append(driving_info)

    def add_blackman_driving(self, channel: str, t_start: float, t_stop: float, _sigma: float, steps=None):
        """
        添加 blackman 脉冲驱动

        :param channel: 脉冲添加通道 (x, y, z)
        :param t_start: 脉冲开始时间 (单位ns)
        :param t_stop: 脉冲结束时间 (单位ns)
        :param _sigma: 脉冲标准差
        :param steps: 时间切片数量
        """
        # 时间切片的个数，ceil 取大于输入的最小整数
        if steps is None:
            steps = 4 * int(np.ceil(t_stop - t_start))
        # 时间切片
        tlist = np.linspace(t_start, t_stop, steps)

        # 驱动脉冲
        def driving_pulse(t, args=None):
            """
            驱动脉冲函数: t时刻的脉冲振幅

            :param t: t时刻
            :param args: 相关参数，一般不填，为了krotov算法而设置

            :return: t时刻的脉冲振幅
            """
            return self.blackman_wave(t, t_start=t_start, t_stop=t_stop, _sigma=_sigma)

        # 驱动信息 [驱动哈密顿量, [时间列表, 脉冲波形函数, 脉冲函数参数], 驱动通道]
        driving_info = [self.ham_driving(channel=channel), [tlist, driving_pulse], channel]

        self.driving_ls.append(driving_info)

    def ham_info(self):
        """
        总哈密顿量信息

        :return: [ham_drift, [ham_driving0, driving_pulse0], [ham_driving1, driving_pulse1], ...]
        """

        return [self.ham_drift] + [[driving_info[0], driving_info[1][1]] for driving_info in self.driving_ls]

    def plot_pulse(self):
        """
        绘制脉冲波形
        """
        # 脉冲数量
        pulse_num = len(self.driving_ls)

        # 绘图
        plt.figure(figsize=(15, 4 * pulse_num), dpi=80)
        for index, driving_info in enumerate(self.driving_ls):
            plt.subplot(int(f'{pulse_num}1{index + 1}'))
            # 脉冲的时间切片列表
            tlist = driving_info[1][0]
            # 脉冲只是函数，并不是完整列表
            pulse_func = driving_info[1][1]
            # 每一时刻脉冲的振幅
            pulse = [pulse_func(t) for t in tlist]

            name = driving_info[2]

            plt.plot(tlist, pulse, label=f'${name}$')
            plt.legend()
            plt.ylabel('Pulse Amp')

        plt.xlabel('t')
        plt.show()


class Dynamics(object):
    """
    动力学演化
    """

    def __init__(self, _ham):
        """
        :param _ham: 哈密顿量
        """
        self.ham = _ham


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
    ham_dr2 = 1j * (a_dag - a)

    amp_1 = lambda t, args: _amp
    amp_2 = lambda t, args: _amp

    _ham = [ham_d, [ham_dr1, amp_1], [ham_dr2, amp_2]]

    return _ham


def plot_population(occ, tls):
    """
    绘制布居概率随时间的变化

    :param occ: 不同时刻在所有能级上的布居数 [occ0, occ1, occ2, ...]
    :param tls: 时间切片列表
    """
    # 能级个数
    num = len(occ)
    plt.figure(figsize=(16, 10), dpi=80)

    for i in range(num):
        plt.plot(tls, occ[i], label='$|' + str(i) + r'\rangle$')
    plt.xlabel('Time(ns)')
    plt.ylabel('Occupation')
    plt.xlim([0, 30])
    plt.legend()

    plt.show()


def occupation(dyn, _dim):
    """
    计算不同时刻的布居概率

    :param dyn: mesolve演化后的函数
    :param _dim: 维度
    """
    # 在|0>, |1>, |2>态的投影算符
    occ_proj = [proj(_psi=basis(_dim, i)) for i in range(_dim)]

    # 计算布居概率
    occ = expect(occ_proj, dyn.states)

    # 绘制布居概率随时间的变化
    plot_population(occ, dyn.times)


if __name__ == '__main__':
    """
    所有系数定义均以 GHZ 为单位，时间单位为 ns
    """
    # 维度
    dim = 3

    # 总时间
    T = 20
    sigma = T / 6
    steps = 4 * int(np.ceil(T - 0))

    tlist = np.linspace(0, T, steps)

    # 生成哈密顿量
    # 定义相关常数
    kerr_q = -2 * np.pi * 297e-3  # qubit 的非谐性
    omega_q = 6.2815 * 2 * np.pi  # qubit 本征频率
    amp_01 = 1  # 驱动振幅
    # 哈密顿量
    ham = Hamiltonian(_dim=dim)
    # 添加漂移项
    ham.add_drift(kerr=kerr_q)

    # 初始脉冲
    ham.add_square_driving(channel='x', t_start=0, t_stop=T, _amp=0)
    ham.add_blackman_driving(channel='y', t_start=0, t_stop=T, _sigma=sigma)
    # 绘制脉冲
    ham.plot_pulse()

    # 动力学演化
    objective = krotov.Objective(initial_state=basis(dim, 0), target=basis(dim, 1), H=ham.ham_info())

    # 试探演化
    guess_dynamics = objective.mesolve(tlist=tlist, progress_bar=True, options=Options(nsteps=50000))

    # 布局概率随时间的演化
    # TODO 布居概率在其他时间与论文结果不符合，需要继续调试
    occupation(guess_dynamics, _dim=dim)
