from gr.pygr import polar_histogram
import numpy as np

norms = ['count', 'probability', 'countdensity', 'pdf', 'cumcount', 'cdf']
random_theta = np.random.rand(1, 10000) * 2 * np.pi
theta = [0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1]

for param in norms:
    print(param)
    random_theta = np.random.rand(1, 10000) * 2 * np.pi

    polar_histogram(random_theta, num_bins=100, colormap=pixmap, draw_edges=True, edge_color=222, face_alpha=0.9, normalization=param)
    input()
    polar_histogram(bin_counts=[6, 9, 3, 4], bin_edges=[0, 0.2, 0.5, 0.9, 2], normalization=param)
    input()
    polar_histogram(bin_counts=[6, 9, 3, 4], bin_edges=[0, 0.2, 0.5, 0.9, 2], colormap=pixmap, draw_edges=True,
                    normalization=param)
    input()
    polar_histogram(random_theta, num_bins=10, normalization=param)
    input()
    polar_histogram(random_theta, num_bins=10, normalization=param, colormap=pixmap)
    input()
    polar_histogram(random_theta, num_bins=10, normalization=param, colormap=pixmap, draw_edges=True)
    input()
    polar_histogram(bin_counts=[6, 9, 3, 4], bin_edges=[0, 0.2, 0.5, 0.9, 2], stairs=True, normalization=param)
    input()
    polar_histogram([0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1])
    input()
    polar_histogram([0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1], normalization=param,
                    edge_color=500)
    input()
    polar_histogram([0.1, 1.1, 5.4, 3.4, 2.3, 4.5, 3.2, 3.4, 5.6, 2.3, 2.1, 3.5, 0.6, 6.1, 6, 6, 6, 6], num_bins=5,
                    edge_color=222)
    input()