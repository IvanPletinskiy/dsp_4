from random import choice
from math import sin, pi, hypot, atan2, cos
from statistics import mean
from matplotlib import pyplot as plt

N = 512
AVERAGED_WINDOW = 5
MEDIAN_WINDOW = 7
REMOVING_ELEMENTS = 1
B1 = 100
B2 = 2
ERROR_LEVEL = 0.001


def test_signal(hi, N, B1, B2):
    return B1 * sin((2 * pi * hi) / N) + sum(B2 * choice([-1, 1]) * sin((2 * pi * hi * j) / N) for j in range(50, 71))


def moving_averaged_smooting(values, window):
    offset = (window - 1) // 2
    def_range = range(len(values))
    return [mean(values[i] for i in range(j - offset, j + offset) if i in def_range) for j in def_range]


def fourth_degree_parabola_smooting(values):
    N = 1 / 2431
    def_range = range(len(values))
    get_value = lambda i: values[i] if i in def_range else 0

    def point_antialized(i):
        return N * (110 * get_value(i - 6) - 198 * get_value(i - 5) - 135 * get_value(i - 4) + 110 * get_value(i - 3)
                    + 390 * get_value(i - 2) + 600 * get_value(i - 1) + 677 * get_value(i) + 600 * get_value(i + 1)
                    + 390 * get_value(i + 2) + 110 * get_value(i + 3) - 135 * get_value(i + 4) - 198 * get_value(i + 5)
                    + 110 * get_value(i + 6))

    return [point_antialized(i) for i in def_range]


def moving_median_smooting(values, window, remove):
    offset = (window - 1) // 2
    def_range = range(len(values))

    def point_smoothed(i):
        window_values = [values[j] for j in range(i - offset, i + offset) if j in def_range]
        window_values = sorted(window_values[remove:-remove])
        return mean(window_values) if window_values else 0

    return [point_smoothed(i) for i in def_range]


def fourier_path(func, sequence, j, N):
    result = sum(x * func(2 * pi * i * j / N) for i, x in enumerate(sequence))
    return (2 / N) * result


def fourier_spectrum(sequence):
    N = len(sequence)
    spectrum_list = []
    for j in range(N // 2):
        cosine = fourier_path(cos, sequence, j, N)
        sine = fourier_path(sin, sequence, j, N)
        amplitude = hypot(sine, cosine)
        phase = atan2(sine, cosine)
        spectrum_list.append((amplitude, phase if abs(amplitude) > ERROR_LEVEL else 0))

    return spectrum_list


def print_plot(signals, labels, w, h):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    plots = []
    fig = plt.figure(figsize=(15, 7))
    plt.grid(True)

    for i, unit in enumerate(signals):
        plt.subplot(h, w, i + 1)
        tempPlot, = plt.plot(unit, color=colors[i])
        plots.append(tempPlot)

    plt.figlegend(plots, labels, loc='upper left')
    return plots


def main():
    labels = ["???????????????????????? ????????????", "???????????????????? ????????????????????", "???????????????? 4 ??????????????", "?????????????????? ????????????????????"]
    random_signal = [test_signal(i, N, B1, B2) for i in range(N)]

    moving_averaged = moving_averaged_smooting(random_signal, AVERAGED_WINDOW)
    parabola = fourth_degree_parabola_smooting(random_signal)
    moving_median = moving_median_smooting(random_signal, MEDIAN_WINDOW, REMOVING_ELEMENTS)

    print_plot([random_signal, moving_averaged, parabola, moving_median], labels, 2, 2)

    # Signal spectrum
    labels = ["?????????????????? ?????????????????????????? ??????????????", "?????????????????? ???????????????????????? ??????????????",
              "?????????????????? ?????????? ???????????????????? ??????????????????", "?????????????????? ?????????? ???????????????????? ????????????????????"]
    amplitude, phase = zip(*fourier_spectrum(random_signal))
    amplitude_averaged, phase_averaged = zip(*fourier_spectrum(moving_averaged))
    amplitude_parabola, phase_parabola = zip(*fourier_spectrum(parabola))
    amplitude_median, phase_median = zip(*fourier_spectrum(moving_median))

    print_plot([amplitude, amplitude_averaged, amplitude_parabola, amplitude_median], labels, 2, 2)

    plt.show()


if __name__ == '__main__':
    main()
