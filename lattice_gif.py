import plotly.graph_objects as go

from lattice_vals import generate_vals
from lattice_points import create_lattice_points
from arrows_lines import create_arrows


def generate_gif_frame(x, y, origin):
    """
    This function generates a gif of the changing lattices
    between two specified points in the 2D map
    """
    fig = go.Figure(layout=go.Layout(width=600, height=600))
    arrow_cols = ["green", "blue", "red"]
    if x + y >= 1:
        vals = generate_vals((1-y), (1-x))
        arrows = create_arrows(vals, origin, arrow_cols, "-")
    else:
        vals = generate_vals(x, y)
        arrows = create_arrows(vals, origin, arrow_cols, "+")
    data = create_lattice_points(vals, origin, 2)
    fig.add_trace(go.Scatter(data, mode='markers',
                             marker=dict(size=20,
                                         color='black'),
                             hoverinfo='none'
                             ))
    for arr in arrows:
        fig.add_annotation(arr)
    fig.update_xaxes(range=[-1.5, 1.5])
    fig.update_yaxes(range=[-1.5, 1.5])
    return fig
