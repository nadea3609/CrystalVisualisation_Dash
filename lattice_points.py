import numpy as np


def create_lattice_points(vals, origin, nlayers=1):
    """
    function to create the array of lattice points for the
    right side graph of the main function
    """
    if nlayers == 0:
        raise ValueError("Number of layers must be at least 2!")
    size = 2 * nlayers + 1
    dx = vals['v1']
    dy = vals['v2'] * np.sin(vals['ang'])
    dy_x = vals['v2'] * np.cos(vals['ang'])  # x component of dy
    data = {'x': [], 'y': []}
    n = -2
    n_dyx = -2
    for i in range(0, size ** 2):
        if n > 2:
            n = -2
            n_dyx += 1
        data['x'].append(origin['x'] + n * dx + n_dyx * dy_x)
        n += 1
    n = -2
    for i in range(0, size ** 2):
        for j in range(0, 5):
            data['y'].append(origin['y'] + n * dy)
        n += 1
    return data
