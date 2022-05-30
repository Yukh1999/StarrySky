"""
Optimize the performance of Rz gate

GRAPE(Gradient Ascent Pulse Engineering) algorithm
"""

import numpy as np
import pandas as pd
from qutip import destroy, coherent, Qobj
from matplotlib import pyplot as plt
import krotov
from scipy import integrate


class DrivingPulse(object):
    def __init__(self, t0, tg, dt):
        self.tls = np.arange(t0, tg+dt, dt)
        self.t0 = t0
        self.tg = tg
        self.dt = dt
        self.number = self.tls.shape[0]

    def pulse_sequence(self, pulse_func):
        tls = self.tls

        return [pulse_func(t) for t in tls]

    def plot_pulse(self, pulse_sequence, name=None):
        """
        Plot Pulse
        """
        tls = self.tls
        plt.figure(figsize=(16, 12), dpi=100)

        plt.plot(tls, pulse_sequence, linewidth=5)
        plt.xlabel('Time', fontsize=18)
        plt.ylabel('Amp', fontsize=18)

        if name is not None:
            plt.title(name)
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        plt.show()


class SinglePhotonDriving(DrivingPulse):

    def __init__(self, t0, tg, dt, phi, driving_0, driving_2=None):
        super().__init__(t0, tg, dt)
        self.driving_0 = driving_0
        self.driving_2 = driving_2
        if driving_2 is None:
            self.driving_2 = lambda t: 0
        self.phi = phi

    def ori_pulse(self, t):
        t0 = self.t0
        tg = self.tg
        Tg = tg - t0
        phi = self.phi

        pulse = np.pi * phi * np.sin(np.pi * (t - t0) / Tg) \
                / (8 * Tg * np.sqrt(self.driving_0 + self.driving_2(t)))

        return pulse

    def integ_func(self, t):
        t0 = self.t0
        tg = self.tg
        Tg = tg - t0

        return np.sqrt(self.driving_0 + self.driving_2(t)) * krotov.shapes.blackman(t, t0, Tg)

    def blackman_pulse(self, t):
        t0 = self.t0
        tg = self.tg
        Tg = tg - t0

        phi = self.phi

        integ = integrate.quad(self.integ_func, t0, Tg)[0]

        amp = phi / (integ * 4)

        return amp * krotov.shapes.blackman(t, t_start=t0, t_stop=Tg)


class TwoPhotonDriving(DrivingPulse):

    def __init__(self, t0, tg, dt, driving_0, rate_param):
        super().__init__(t0, tg, dt)
        self.driving_0 = driving_0
        self.rate_param = rate_param

    def lin_triangle_pulse(self, t):
        t0 = self.t0
        tg = self.tg
        Tg = tg - t0

        rate_param = self.rate_param

        energy_gap = 4 * self.driving_0
        rate = 1 / (rate_param * energy_gap)

        t_mid = Tg / 2

        if t < t_mid:
            return -rate * t
        else:
            return -rate * (Tg - t)


class Ham(object):
    """
    The Hamiltonian
    """

    def __init__(self, dim, t0, tg, dt):
        self.ham_photon_loss = None
        self.sequence_2 = []
        self.sequence_1 = []
        self.isSet1 = False
        self.isSet2 = False
        self.ham_driving_2 = []
        self.ham_driving_1 = []
        self.ham_drift = None

        self.tls = np.arange(t0, tg+dt, dt)
        self.t0 = t0
        self.tg = tg
        self.dt = dt
        self.number = self.tls.shape[0]

        self.a = destroy(dim)
        self.a_dag = self.a.dag()

    def set_drift(self, detuning, driving_0):
        """
        The drift term of Hamiltonian
        """
        a = self.a
        a_dag = self.a_dag

        self.ham_drift = detuning * a_dag * a + 1 / 2 * (a_dag ** 2) * (a ** 2) - driving_0 / 2 * (
                a_dag ** 2 + a ** 2)

    def set_driving_1(self, pulse_sequence):
        """
        Single photon driving
        """
        a = self.a
        a_dag = self.a_dag

        self.sequence_1 = pulse_sequence

        self.ham_driving_1 = [amp * (a + a_dag) for amp in pulse_sequence]
        self.isSet1 = True

    def set_driving_2(self, pulse_sequence):
        """
        Two photon driving
        """
        a = self.a
        a_dag = self.a_dag

        self.sequence_2 = pulse_sequence

        self.ham_driving_2 = [amp * (a ** 2 + a_dag ** 2) for amp in pulse_sequence]
        self.isSet2 = True

    def add_photon_loss(self, kappa, n_th):
        """
        Add photon loss to the system
        """
        a = self.a
        a_dag = self.a_dag

        self.ham_photon_loss = -1j * kappa * (1 + n_th) * a_dag * a / 2

    def ham_ctrl(self, idx):
        """
        Hamiltonian of control term
        """
        ctrl = [self.ham_driving_1[idx]]
        if self.isSet2:
            ctrl.append(self.ham_driving_2[idx])

        return ctrl

    def ctrl_sequence(self, idx):
        """
        The sequence of control term
        """
        ctrl_seq = [self.sequence_1[idx]]
        if self.isSet2:
            ctrl_seq.append(self.sequence_2)
        return ctrl_seq

    def ham_full(self, idx):
        """
        The full Hamiltonian of idx
        """
        ham = 0
        if self.isSet1:
            ham = self.ham_drift + self.ham_driving_1[idx]
        if self.isSet2:
            ham += self.ham_driving_2[idx]
        if self.ham_photon_loss is not None:
            ham += self.ham_photon_loss

        return ham

    def unitary(self, idx):
        """
        The ith unitary operator
        """
        dt = self.dt
        ham = self.ham_full(idx)
        uni = (-1j * dt * ham).expm()

        return uni

    def evolution(self, initial_state, target_state):
        """
        Time evolution
        """
        number = self.number

        uni_ls = [self.unitary(i) for i in range(number)]

        # 前向传播的态
        states_forward = []

        # 后向传播的态
        states_back = []

        temp_state_forward = initial_state
        #
        # states_forward.append(initial_state)

        # temp_state_back = target_state
        # for i in range(number):
        #     temp_state_back = (uni_ls[i] * temp_state_back).unit()

        # states_back.append(temp_state_back)

        for i in range(number):
            temp_state_forward = (uni_ls[i] * temp_state_forward).unit()
            states_forward.append(temp_state_forward)

            if i < number - 1:
                temp_state_back = target_state
                for j in range(number)[i + 1:]:
                    temp_state_back = (uni_ls[j] * temp_state_back).unit()

                states_back.append(temp_state_back)

        states_back.append(target_state)

        return states_forward, states_back


class Optimize(object):
    def __init__(self, ham: Ham, initial_state, target_state, ctrl_num):
        self.grads = None
        self.states_back = None
        self.states_forward = None
        self.ham = ham
        self.initial_state = initial_state
        self.target_state = target_state

        self.ctrl_num = ctrl_num

    def solve_states(self):
        self.states_forward, self.states_back = self.ham.evolution(initial_state=self.initial_state,
                                                                   target_state=self.target_state)

    def solve_gradient(self):
        dt = self.ham.dt
        ctrl_num = self.ctrl_num

        grad = lambda idx, nth: -1j * dt * np.array(self.states_back[idx].dag() * self.ham.ham_ctrl(idx)[nth] \
                                                    * self.states_forward[idx])[0][0]

        self.grads = [[grad(idx, nth) for idx in range(self.ham.number)] for nth in range(ctrl_num)]

    def fidelity(self):
        return np.abs(np.array(self.states_forward[-1].dag() * self.target_state)[0][0]) ** 2

    def optimize_grape(self, step, thres):
        self.solve_states()
        self.solve_gradient()
        print("Fidelity: ", self.fidelity())

        print(self.grads[0][:5])

        sequence_1 = np.zeros(self.ham.number, dtype=complex)
        sequence_2 = np.zeros(self.ham.number, dtype=complex)
        sequence = [sequence_1, sequence_2]

        for i in range(thres):
            for nth in range(self.ctrl_num):
                for idx in range(self.ham.number):
                    sequence[nth][idx] = np.complex(self.ham.ctrl_sequence(idx)[nth]) - step * self.grads[nth][idx]

                sequence[nth][self.ham.number - 1] = 0

            self.ham.set_driving_1(pulse_sequence=sequence[0])

            if self.ctrl_num == 2:
                self.ham.set_driving_2(pulse_sequence=sequence[1])

            self.solve_states()
            self.solve_gradient()
            print(self.grads[0][:5])
            print("Fidelity: ", self.fidelity())
