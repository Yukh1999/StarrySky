"""
KPO 系统双参量调控 Rz 门的实现
体系：单体KPO系统
"""

from qutip import coherent, destroy, qeye, mesolve
import numpy as np
from scipy import integrate
import krotov
from matplotlib import pyplot as plt

# 定义相关常数
N = 20  # 空间维度
delta = 0  # KPO与双光子驱动的失谐
K = 1  # 非线性强度
P = 4 * K  # 双光子驱动强度

# 定义算符

# 湮灭算符
a = destroy(N)
a_dag = a.dag()

# 单位算符
I = qeye(N)

# 双光子驱动 KPO 系统哈密顿量
ham_0 = delta * a_dag * a + K/2 * (a_dag**2) * (a**2) - P/2 * (a_dag **2 + a ** 2)

# 全局变量
Tg = 2/K  # 门时间
phi = np.pi/2  #  旋转角度

rate_fold = 10 # 双光子变化速率参数


# 双光子调制驱动哈密顿量
def triangle_pulse(_t, _rate):
    """
    三角波脉冲
    """
    # 中间时刻
    t_mid = Tg/2
    if _t < t_mid:
        return _rate * _t
    else:
        return _rate * (Tg - _t)

def P_d2(_t):
    """
    额外的双光子调制驱动
    """
    # 绝热变化速率
    energy_gap = 4 * P
    rate = 1 / (energy_gap * rate_fold)

    return triangle_pulse(_t, _rate=rate)

def ham_2(_t):
    return -P_d2(_t)/2 * (a_dag **2 + a ** 2)


# 单光子驱动哈密顿量
# black man 脉冲
def blackman_pulse(_t):
    """
    black man pulse
    """
    sigma = Tg/6

    # 计算振幅
    # black man脉冲波形函数
    pulse = lambda t: 4 * np.sqrt(P + P_d2(t) / K) * krotov.shapes.blackman(t, 0, Tg)

    # 对时间积分
    integ = integrate.quad(pulse, 0, Tg)[0]

    amp = phi / integ

    return amp * krotov.shapes.blackman(_t, t_start=0, t_stop=Tg)


def ham_1(_t, args):
    pass
