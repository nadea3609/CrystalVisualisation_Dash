from dash import Dash, dcc, html, Input, Output, callback
import numpy as np
import plotly.graph_objects as go

from arrows_lines import create_arrows
from lattice_points import create_lattice_points

# constants and configs
size = np.linspace(0, 1, 1001)
config = {'displayModeBar': False}
app = Dash()

# creating figures for the dashboard
fig_l = go.Figure(data=[go.Heatmap(x=size, y=size,
                        z=np.zeros((1000, 1000)),
                        opacity=0,
                        hoverinfo='x+y',
                        showscale=False
                                   )
                        ],
                  layout=go.Layout(
                     width=600,
                     height=600
                  ))

fig_l.add_shape(dict(type="path",
                path="M 0 0 L 0 1 L 1 0 Z",
                fillcolor="yellow",
                line_color="Yellow"
                     )
                )
fig_l.update_xaxes(range=[-0.1, 1.1])
fig_l.update_yaxes(range=[-0.1, 1.1])
fig_l.update_layout()
# app layout
app.layout = html.Div([
    html.Div([
        html.H2('Hover over left plot to generate basis on right plot')
    ], style={'width': '100%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(figure=fig_l,
                  hoverData={'points': [{"x": 0, "y": 0}]},
                  config=config,
                  id='left-fig')
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'}),
    html.Div([
        dcc.Graph(config=config, id='right-fig'),
        html.Code('v1=0, v2=0, ang=90', id='txt-output')
    ], style={'display': 'inline-block', 'width': '49%'}),
])


# callback to generate right side graph
@callback(
    Output('right-fig', 'figure'),
    Output('txt-output', 'children'),
    Input('left-fig', 'hoverData'),
)
def update_graph(hoverData):
    hover = hoverData['points'][0]
    origin = {'x': 0, 'y': 0}
    r12 = 1/3 * hover['y']
    r01 = 1/6 * (3 - 3*hover['x']-hover['y'])
    r02 = 1/6 * (3+3*hover['x']-hover['y'])
    den = -4*hover['y'] ** 2
    num = np.sqrt(((9*(hover['x'] ** 2) + 5*(hover['y'] ** 2) - 6*hover['y'] + 9) ** 2) - 36*(hover['x'] ** 2) * (3-hover['y']) ** 2)
    vals = {
        'v1': np.sqrt(r12 ** 2 + r01 ** 2),
        'v2': np.sqrt(r12 ** 2 + r02 ** 2),
        'ang': np.acos(den/num)
        }
    data = create_lattice_points(vals, origin, 2)
    # dx = vals['v1']
    # dy = vals['v2'] * np.sin(vals['ang'])
    # dy_x = vals['v2'] * np.cos(vals['ang']) # x component of dy
    # data = {
    #     'x': [origin['x'], origin['x'] + dx, origin['x'] + dy_x,
    #           origin['x'] - dx - dy_x, origin['x'] + dx + dy_x,
    #           origin['x'] - dx, origin['x'] - dy_x,
    #           origin['x'] - dx + dy_x, origin['x'] + dx - dy_x
    #           ],
    #     'y': [origin['y'], origin['y'], origin['y'] + dy,
    #           origin['y'] - dy, origin['y'] + dy, origin['y'],
    #           origin['y'] - dy, origin['y'] + dy, origin['y'] - dy
    #           ]
    #     }
    # for i in range(1, len(data['x'])):
    #     extend_x = 2 * data['x'][i]
    #     extend_y = 2 * data['y'][i]
    #     data['x'].append(extend_x)
    #     data['y'].append(extend_y)
    #     if i == 1 or i == 5:
    #         data['x'].append(extend_x + dy_x)
    #         data['x'].append(extend_x - dy_x)
    #         data['y'].append(extend_y + dy)
    #         data['y'].append(extend_y - dy)
    #     elif i == 2 or i == 6:
    #         data['x'].append(extend_x + dx)
    #         data['x'].append(extend_x - dx)
    #         data['y'].append(extend_y)
    #         data['y'].append(extend_y)
    txt = f"v1= {'%.3f' % vals['v1']}, v2={'%.3f' % vals['v2']}, ang={'%.3f' % (vals['ang'] * 180/np.pi)}"
    fig_r = go.Figure(data=[go.Scatter(data, mode='markers',
                                       marker=dict(size=20,
                                                   color='black'),
                                       hoverinfo='none'
                                       )],
                      layout=go.Layout(width=600, height=600)
                      )
    arrow_cols = ["green", "blue", "red"]
    arrows = create_arrows(vals, origin, arrow_cols)
    for arr in arrows:
        fig_r.add_annotation(arr)
    fig_r.update_xaxes(range=[-1.5, 1.5])
    fig_r.update_yaxes(range=[-1.5, 1.5])
    if (hover['x'] + hover['y']) >= 1:
        txt = "cursor is outside triangle"
        return None, txt
    else:
        return fig_r, txt


if __name__ == "__main__":
    app.run(debug=True)
