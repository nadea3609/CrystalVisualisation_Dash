import plotly.graph_objects as go


def create_arrows(data, origin, colours):
    """Function for creating arrows for the vectors of the superbase"""
    arrows = []
    for i in range(1, 4):
        arrows.append(
            go.layout.Annotation(dict(
                x=data['x'][i], y=data['y'][i], xref="x", yref="y",
                text="", showarrow=True, axref="x", ayref='y',
                ax=origin['a'], ay=origin['b'], arrowhead=3,
                arrowwidth=2, arrowcolor=colours[i-1]))
        )
    return arrows


def create_lines(data):
    """Function for creating lines to show the shape of the unit cell"""
    lines = [
        go.layout.Annotation(dict(
                x=data['x'][4], y=data['y'][4], xref="x", yref="y",
                text="", showarrow=True, axref="x", ayref='y',
                ax=data['x'][1], ay=data['y'][1], arrowhead=0,
                arrowwidth=2, arrowcolor='grey')),
        go.layout.Annotation(dict(
                x=data['x'][4], y=data['y'][4], xref="x", yref="y",
                text="", showarrow=True, axref="x", ayref='y',
                ax=data['x'][2], ay=data['y'][2], arrowhead=0,
                arrowwidth=2, arrowcolor='grey'))
    ]
    return lines
