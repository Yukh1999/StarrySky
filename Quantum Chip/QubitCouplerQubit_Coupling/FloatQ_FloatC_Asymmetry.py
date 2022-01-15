from scipy.constants import hbar, elementary_charge as e
from GroundQ_GroundC import cap_ind_to_freq
import numpy as np

# 相关常数
# 普朗克常量
h = hbar * 2 * np.pi
# 磁通量子
Phi_0 = h / (2*e)
# 约化磁通量子
phi_0 = hbar / (2*e)


def xi(E_C, E_J):
    """
    耦合强度计算中间常数

    :param E_C: 库柏对电容能
    :param E_J: 约瑟夫森电感能
    """
    return np.sqrt(2 * E_C / E_J)


# 输入值
# 自电容
cap_q = 55.19e-15
cap_c = 61.97e-15

# 约瑟夫森电感
ind_junc_q = 6e-9

# 耦合关断: 6.399 GHz
# ind_junc_c = 4.28905
# 耦合打开: 3.61235 GHz
ind_junc_c = 13e-9

# 对地电容
cap_gq1 = 13.82e-15
cap_gq2 = 401.11e-15
cap_gq = 2 / (1/cap_gq1 + 1/cap_gq2)
cap_gc = 152e-15

# 互电容
# qubit_1 和 coupler 互电容: qubit_1(1,2), coupler(3,4)
cap_23 = 16.84e-15
cap_14 = 0.08e-15
cap_13 = 0.23e-15
cap_24 = 2.75e-15

# qubit_2 和 coupler 互电容: qubit_2(5,6), coupler(3,4)
cap_35 = 2.75e-15
cap_36 = 0.08e-15
cap_46 = 0.23e-15
cap_45 = 16.84e-15


# 自电容能
E_C1 = e**2 / (2 * cap_q + cap_gq)
E_C2 = E_C1
E_Cc = e**2 / (2 * cap_c + cap_gc)


# 互电容能计算中间常数
cap_eff = (2*cap_q + cap_gq) * (2*cap_c + cap_gc)
# 互电容能
E_12 = (-e**2 / (cap_gc * (2*cap_q + cap_gq) * cap_eff)) * \
       (((cap_23 + cap_24) * (cap_45 + cap_35) + cap_24*cap_35) * cap_c + (cap_23*cap_35 + cap_45*cap_24)*cap_gc)

E_1c = -e**2 * (cap_23 - cap_24) / cap_eff

E_2c = -e**2 * (cap_45 - cap_35) / cap_eff

# 电感能
E_J1 = phi_0**2 / ind_junc_q
E_J2 = E_J1
E_Jc = phi_0**2 / ind_junc_c


# 耦合强度计算中间常数
xi_1 = xi(E_C1, E_J1)
xi_2 = xi(E_C2, E_J2)
xi_c = xi(E_Cc, E_Jc)

# 频率
# 非线性修正
freq_q1_ = (np.sqrt(8*E_J1 * E_C1) - E_C1 * (1 + xi_1/4)) / h
freq_q2_ = (np.sqrt(8*E_J2 * E_C2) - E_C2 * (1 + xi_2/4)) / h
freq_c_ = (np.sqrt(8*E_Jc * E_Cc) - E_Cc * (1 + xi_c/4)) / h

# 耦合强度计算: 除 h 转化为频率(Hz)
g_1c = ((E_1c / np.sqrt(2)) * (E_J1 * E_Jc / (E_C1 * E_Cc))**(1/4) * (1-(1/8)*(xi_c+xi_1))) / h
g_2c = ((E_2c / np.sqrt(2)) * (E_J2 * E_Jc / (E_C2 * E_Cc))**(1/4) * (1-(1/8)*(xi_c+xi_2))) / h
g_12 = ((E_12 / np.sqrt(2)) * (E_J1 * E_J2 / (E_C1 * E_C2))**(1/4) * (1-(1/8)*(xi_1+xi_2))) / h

# 本征频率(Hz)
freq_1 = cap_ind_to_freq(cap=cap_q + cap_gq/2, ind_junc=ind_junc_q)
freq_2 = freq_1
freq_c = cap_ind_to_freq(cap=cap_c + cap_gc, ind_junc=ind_junc_c)

# qubit 与 coupler 差频
delta_1 = freq_c_ - freq_q1_
delta_2 = delta_1

# qubit 与 coupler 合频
sum_1 = freq_c_ + freq_q1_
sum_2 = sum_1

# 等效耦合路径(Hz)
g_eff = (g_1c * g_2c / 2) * (1/delta_1 + 1/sum_1 + 1/delta_2 + 1/sum_2)

# qubit 之间总耦合强度
g = g_12 - g_eff


# 输出数据
print('-' * 100)
print('本征频率:')
print('Qubit1_freq: ', freq_q1_*1e-9, 'GHz')
print('Qubit2_freq: ', freq_q2_*1e-9, 'GHz')
print('Coupler_freq: ', freq_c_*1e-9, 'GHz')
print('-' * 100)
print('耦合强度: ')
print('g_1c: ', g_1c * 1e-6, 'MHz')
print('g_2c: ', g_2c * 1e-6, 'MHz')
print('g_eff: ', g_eff * 1e-6, 'MHz')
print('g_12: ', g_12 * 1e-6, 'MHz')
print('g: ', g * 1e-6, 'MHz')
print('-' * 100)
