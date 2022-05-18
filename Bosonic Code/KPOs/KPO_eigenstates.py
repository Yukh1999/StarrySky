from qutip import coherent, destroy, qeye, mesolve
import numpy as np

# 定义常数
N = 20  # 维度
delta = 0  # 失谐
K = 1  # 非线性强度
p0 = 4 * K  # 双光子驱动强度

# 定义算符
a = destroy(N)
a_dag = a.dag()
I = qeye(N)

# 哈密顿量
ham = delta * a_dag * a + K / 2 * (a_dag ** 2) * (a ** 2) - p0 / 2 * (a_dag ** 2 + a ** 2)

# 哈密顿量本征态
states = ham.eigenstates()[1]

# 理想猫态
alpha = np.sqrt(p0/K)
logical_0 = coherent(N=N, alpha=alpha)
logical_1 = coherent(N=N, alpha=-alpha)
ideal_state = (logical_0+logical_1).unit()

# 保真度
fidelity = np.abs(np.array(ideal_state.dag() * states[1])[0][0]) ** 2
print(1-fidelity)
print(ideal_state)
print(states[1])

