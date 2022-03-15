import numpy as np
from qutip import coherent, wigner
from matplotlib import pyplot as plt

# 维度
N = 40

# 相干态
alp = 2

# |α>, |-α>
alpha = coherent(N=N, alpha=alp)
alpha_m = coherent(N=N, alpha=-alp)

# |iα>, |-iα>
alpha_i = coherent(N=N, alpha=1j * alp)
alpha_i_m = coherent(N=N, alpha=-1j * alp)

# 逻辑比特编码态
logic_0 = np.sqrt(2) * (alpha + alpha_m)
logic_1 = np.sqrt(2) * (alpha_i + alpha_i_m)

# 编码态的密度矩阵
rho_0 = logic_0 * logic_0.dag()
rho_1 = logic_1 * logic_1.dag()


# wigner 函数既可以输入量子态，也可以输入密度矩阵
# 0 态的 wigner 函数
vec = np.linspace(-5, 5, 200)  # 计算范围
W0 = wigner(psi=logic_0, xvec=vec, yvec=vec)

# 1 态的 wigner 函数
W1 = wigner(psi=logic_1, xvec=vec, yvec=vec)


# 绘制 wigner 函数图像
plt.figure(figsize=(13, 6))
plt.subplot(121)
plt.contourf(vec, vec, W0, 100, cmap=plt.get_cmap('bwr'))

plt.subplot(122)
plt.contourf(vec, vec, W1, 100, cmap=plt.get_cmap('bwr'))

plt.show()
