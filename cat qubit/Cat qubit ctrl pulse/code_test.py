import numpy as np
from qutip import basis
import krotov
from pi_pulse import hamiltonian

L = 3
psi = [[basis(L, 0), basis(L, 1)]]


H = hamiltonian(_dim=L, _kerr=-2 * np.pi * 297e-3, _omega=6.2815 * 2 * np.pi, _amp=1)

a = krotov.Objective(initial_state=psi[0][0], target=psi[0][1], H=H)

print(a)
