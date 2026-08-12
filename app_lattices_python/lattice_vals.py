import numpy as np


def generate_vals(x, y):
    """Generates the vals dictionary for the right figure and other operations"""
    r12 = 1/3 * y
    r01 = 1/6 * (3 - 3 * x - y)
    r02 = 1/6 * (3 + 3 * x - y)
    den = -4*y ** 2
    num = np.sqrt(((9*(x ** 2) + 5*(y ** 2) - 6*y + 9) ** 2) - 36*(x ** 2) * (3 - y) ** 2)
    if y + y >= 1:
        vals = {
            'v1': np.sqrt(r12 ** 2 + r01 ** 2),
            'v2': np.sqrt(r12 ** 2 + r02 ** 2),
            'ang': np.acos(den/num)
        }
    else:
        vals = {
            'v1': np.sqrt(r12 ** 2 + r01 ** 2),
            'v2': np.sqrt(r12 ** 2 + r02 ** 2),
            'ang': np.acos(den/num)
        }
    return vals
