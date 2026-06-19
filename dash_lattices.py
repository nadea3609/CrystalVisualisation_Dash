from dash import Dash, dcc, html, Input, Output, callback
import numpy as np
import plotly.graph_objects as go

# axis values
size = np.linspace(0, 1, 1001)
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
        html.H3('Hover over left plot to generate basis on right plot')
    ], style={'width': '100%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(figure=fig_l,
                  hoverData={'points': [{"x": 0, "y": 0}]},
                  id='left-fig')
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='right-fig'),
        html.Code('v1=0, v2=0, ang=90', id='txt-output')
    ], style={'display': 'inline-block', 'width': '49%'}),
])


@callback(
    Output('right-fig', 'figure'),
    Output('txt-output', 'children'),
    Input('left-fig', 'hoverData')
)
def update_graph(hoverData):
    hover = hoverData['points'][0]
    origin = {'a': 0, 'b': 0}
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
    data = {
        'x': [0,
              origin['a'] + vals['v1'],
              origin['a'] + vals['v2'] * np.cos(vals['ang']),
              origin['a'] - vals['v1'] - vals['v2'] * np.cos(vals['ang'])
              ],
        'y': [0,
              origin['b'],
              origin['b'] + vals['v2'] * np.sin(vals['ang']),
              origin['b'] - vals['v2'] * np.sin(vals['ang'])
              ]
        }
    txt = f"v1= {'%.3f' % vals['v1']}, v2={'%.3f' % vals['v2']}, ang={'%.3f' % (vals['ang'] * 180/np.pi)}"
    fig_r = go.Figure(data=[go.Scatter(data, mode='markers',
                                       marker=dict(size=[20, 20, 20, 1],
                                                   color='black'),
                                       hoverinfo='none'
                                       )],
                      layout=go.Layout(width=600, height=600)
                      )
    arrow_cols = ["green", "blue", "red"]
    arrows = [
            go.layout.Annotation(dict(
                x=data['x'][1], y=data['y'][1], xref="x", yref="y",
                text="", showarrow=True, axref="x", ayref='y',
                ax=origin['a'], ay=origin['b'], arrowhead=3,
                arrowwidth=2, arrowcolor=arrow_cols[0])),
            go.layout.Annotation(dict(
                x=data['x'][2], y=data['y'][2], xref="x", yref="y",
                text="", showarrow=True, axref="x", ayref='y',
                ax=origin['a'], ay=origin['b'], arrowhead=3,
                arrowwidth=2, arrowcolor=arrow_cols[1])),
            go.layout.Annotation(dict(
                x=data['x'][3], y=data['y'][3], xref="x", yref="y",
                text="", showarrow=True, axref="x", ayref='y',
                ax=origin['a'], ay=origin['b'], arrowhead=3,
                arrowwidth=2, arrowcolor=arrow_cols[2])),
    ]
    for arr in arrows:
        fig_r.add_annotation(arr)
    fig_r.update_xaxes(range=[-0.6, 0.6])
    fig_r.update_yaxes(range=[-1, 1])
    if (hover['x'] + hover['y']) >= 1:
        txt = "cursor is outside triangle"
        return None, txt
    else:
        return fig_r, txt


if __name__ == "__main__":
    app.run(debug=True)
