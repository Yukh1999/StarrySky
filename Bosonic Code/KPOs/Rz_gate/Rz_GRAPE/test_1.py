from KPO_Rz_system import Ham, SinglePhotonDriving, TwoPhotonDriving, Optimize
from qutip import coherent, mesolve
import numpy as np
from numpy import sqrt

if __name__ == '__main__':
    dim = 20
    t0 = 0
    tg = 3
    dt = 0.05
    tls = np.arange(t0, tg+dt, dt)
    detuning = 0
    driving_0 = 4

    phi = np.pi

    alpha = sqrt(driving_0)

    ham = Ham(dim, t0, tg, dt)
    ham.set_drift(detuning, driving_0)

    # 双光子驱动
    two_driving = TwoPhotonDriving(t0, tg, dt, driving_0, 19)

    driving_2 = two_driving.lin_triangle_pulse

    driving_sequence_2 = two_driving.pulse_sequence(driving_2)

    two_driving.plot_pulse(driving_sequence_2, 'Two Photon Driving')

    # Ham 中添加双光子驱动
    # ham.set_driving_2(driving_sequence_2)

    # 单光子驱动
    single_driving = SinglePhotonDriving(t0, tg, dt, phi, driving_0, driving_2=None)

    driving_1 = single_driving.blackman_pulse

    driving_sequence_1 = single_driving.pulse_sequence(driving_1)

    single_driving.plot_pulse(driving_sequence_1, 'Single Photon Driving')

    ham.set_driving_1(driving_sequence_1)

    # 添加噪音
    # ham.add_photon_loss(kappa=0.1, n_th=0.1)

    logical_0 = coherent(dim, alpha)
    logical_1 = coherent(dim, -alpha)

    initial_state = (logical_0 + logical_1).unit()

    phase_factor = 1j * phi / 2
    target_state = (logical_0 * np.exp(-phase_factor) + logical_1 * np.exp(phase_factor)).unit()

    # 优化
    opt = Optimize(ham=ham, initial_state=initial_state, target_state=target_state, ctrl_num=1)

    opt.optimize_grape(step=0.01, thres=1000)
    # print(opt.fidelity())

