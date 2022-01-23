import matplotlib.pyplot as plt
import numpy as np
from qutip import basis, Options, expect
import krotov
from pi_pulse import hamiltonian, Hamiltonian

L = 3
psi = [[basis(L, 0), basis(L, 1)]]


def plot_population(occ, tls):
    num = len(occ)
    plt.figure(figsize=(16, 10), dpi=80)

    for i in range(num):
        plt.plot(tls, occ[i], label='$|' + str(i) + r'\rangle$')
    plt.xlabel('Time(ns)')
    plt.ylabel('Occupation')
    plt.legend()

    plt.show()


def occupation(dyn):
    occ_proj = [basis(L, i) * basis(L, i).dag() for i in range(L)]

    occ = expect(occ_proj, dyn.states)

    plot_population(occ, dyn.times)


t_start = 0
t_stop = 18 * 2
sigma = t_stop/6
steps = 4 * int(np.ceil(t_stop - t_start))

tlist = np.linspace(t_start, t_stop, steps)

# 哈密顿量
ham = Hamiltonian(_dim=L)
# 添加漂移项
ham.add_drift(kerr=-2 * np.pi * 297e-3)

# 初始脉冲
ham.add_square_driving(channel='x', t_start=0, t_stop=t_stop, _amp=0)
ham.add_blackman_driving(channel='y', t_start=0, t_stop=t_stop, _sigma=sigma)

print(ham.ham_info())
a = krotov.Objective(initial_state=psi[0][0], target=psi[0][1], H=ham.ham_info())

guess_dynamics = [a.mesolve(tlist=tlist, progress_bar=True, options=Options(nsteps=50000))]

occupation(guess_dynamics[0])

print(a)
