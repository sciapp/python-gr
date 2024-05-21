from math import pi

import grm


# TODO Warning GKS: Character height is invalid in routine SET_TEXT_HEIGHT

def polar_histogram_minimal() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    print("Polar histogram with minimal input...")
    grm.plot.polar_histogram(x=theta)
    input("Press enter to continue")


def polar_histogram_phiflip() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    print("Polar histogram with phi_flip...")
    grm.plot.polar_histogram(x=theta, phi_flip=True)
    input("Press enter to continue")


def polar_histogram_nbins() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    print("Polar histogram with num_bins = 3...")
    grm.plot.polar_histogram(x=theta, num_bins=3)
    input("Press enter to continue")


def polar_histogram_bin_counts() -> None:
    bin_counts = [4, 2, 5, 1]
    print("Polar histogram with bin_counts instead of theta values...")
    grm.plot.polar_histogram(x=bin_counts, bin_counts=1)
    input("Press enter to continue")


def polar_histogram_colormap() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    print("Polar histogram with colormaps...")
    grm.plot.polar_histogram(x=theta, x_colormap=44, y_colormap=44, draw_edges=1)
    input("Press enter to continue")


def polar_histogram_bin_edges() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    bin_edges = (0.0, pi / 2, pi * 1.0, pi * 1.33, 2 * pi)
    print("Polar histogram with bin_edges instead of theta values...")
    grm.plot.polar_histogram(x=theta, bin_edges=bin_edges)
    input("Press enter to continue")


def polar_histogram_stairs() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    print("Polar histogram with stairs...")
    grm.plot.polar_histogram(x=theta, stairs=1)
    input("Press enter to continue")


def polar_histogram_rlim() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    rlim = (0.25, 0.5)
    print("Polar histogram with r_lim...")
    grm.plot.polar_histogram(x=theta, r_lim=rlim)
    input("Press enter to continue")


def polar_histogram_philim() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    philim = (pi / 4.0, 1.5 * pi)
    print("Polar histogram with phi_lim...")
    grm.plot.polar_histogram(x=theta, phi_lim=philim)
    input("Press enter to continue")


def polar_histogram_normalization() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    norms = ("count", "probability", "countdensity", "pdf", "cumcount", "cdf")
    print("Polar histogram with different normalizations...")
    for norm in norms:
        print(f"norm = {norm}")
        grm.plot.polar_histogram(x=theta, normalization=norm)
        input("Press enter to continue")


def polar_histogram_bin_width() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    bin_width = pi / 2.0
    print("Polar histogram with bin_width...")
    grm.plot.polar_histogram(x=theta, bin_width=bin_width)
    input("Press enter to continue")


def polar_histogram_title() -> None:
    theta = (0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1)
    title = "testing the polar histogram"
    print("Polar histogram with title...")
    grm.plot.polar_histogram(x=theta, title=title)
    input("Press enter to continue")


def main() -> None:
    polar_histogram_minimal()
    polar_histogram_phiflip()
    polar_histogram_nbins()
    polar_histogram_bin_counts()
    polar_histogram_colormap()
    polar_histogram_bin_edges()
    polar_histogram_stairs()
    polar_histogram_rlim()
    polar_histogram_philim()
    polar_histogram_normalization()
    polar_histogram_bin_width()
    polar_histogram_title()


if __name__ == "__main__":
    main()
