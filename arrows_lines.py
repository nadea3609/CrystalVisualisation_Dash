import plotly.graph_objects as go
import numpy as np


def create_arrows(vals, origin, colours):
    """Function for creating arrows for the vectors of the superbase"""
    arrows = []
    dx = vals['v1']
    dy = vals['v2'] * np.sin(vals['ang'])
    dy_x = vals['v2'] * np.cos(vals['ang'])  # x component of dy
    x_vals = [origin['x'] + dx, origin['x'] + dy_x, origin['x'] - dx - dy_x]
    y_vals = [origin['y'], origin['y'] + dy, origin['y'] - dy]
    for i in range(0, 3):
        arrows.append(
            go.layout.Annotation(dict(
                x=x_vals[i], y=y_vals[i], xref="x", yref="y",
                text="", showarrow=True, standoff=8, startstandoff=8,
                axref="x", ayref='y', ax=origin['x'], ay=origin['y'],
                arrowhead=3, arrowwidth=3, arrowcolor=colours[i]))
        )
    return arrows


# depricated function for adding unit cell boundary
def create_lines(data):
    """Function for creating lines to show the shape of the unit cell"""
    lines = [
        go.layout.Annotation(dict(
                x=data['x'][4], y=data['y'][4], xref="x", yref="y",
                text="", showarrow=True, standoff=8, startstandoff=8,
                axref="x", ayref='y', ax=data['x'][1], ay=data['y'][1],
                arrowhead=0, arrowwidth=2, arrowcolor='grey')),
        go.layout.Annotation(dict(
                x=data['x'][4], y=data['y'][4], xref="x", yref="y",
                text="", showarrow=True, standoff=8, startstandoff=8,
                axref="x", ayref='y', ax=data['x'][2], ay=data['y'][2],
                arrowhead=0, arrowwidth=2, arrowcolor='grey'))
    ]
    return lines
