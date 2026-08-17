import dash
from dash import dcc, html, ctx, Input, Output, callback
from plotly_gif import GIF, capture
import numpy as np
import plotly.graph_objects as go

from arrows_lines import create_arrows
from lattice_points import create_lattice_points
from lattice_vals import generate_vals
from lattice_gif import generate_gif_frame

dash.register_page(__name__, path='/lattice-visualiser', name="Lattice visualiser", order=1)
# constants and configs
size = np.linspace(0, 1, 1001)
origin = {'x': 0, 'y': 0}
config = {'displayModeBar': False, 'responsive': True}


# creating figures for the dashboard
fig_l = go.Figure(data=[go.Heatmap(x=size, y=size,
                        z=np.zeros((1001, 1001)),
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
fig_l.add_shape(dict(type="path",
                path="M 1 1 L 0 1 L 1 0 Z",
                fillcolor="white",
                line_color="white"
                     )
                )
fig_l.add_shape(type="line",
                x0=0, y0=0, x1=0, y1=1,
                line=dict(
                    color="orange",
                    width=3
                ))
fig_l.add_shape(type="line",
                x0=1, y0=0, x1=1, y1=1,
                line=dict(
                    color="green",
                    width=3
                ))
fig_l.add_shape(type="line",
                x0=1, y0=0, x1=0, y1=1,
                line=dict(
                    color="RoyalBlue",
                    width=3
                ))
fig_l.add_shape(type="line",
                x0=0, y0=0, x1=1, y1=0,
                line=dict(
                    color="green",
                    width=3
                ))
fig_l.add_shape(type="line",
                x0=0, y0=1, x1=1, y1=1,
                line=dict(
                    color="orange",
                    width=3
                ))
fig_l.update_xaxes(range=[-0.1, 1.1])
fig_l.update_yaxes(range=[-0.1, 1.1])
fig_l.update_layout()
# app layout
layout = html.Div([
    html.Div([
        html.H2('Lattice visualiser'),
        html.P("""
                This visualiser shows how 2D crystal lattices can be represented
                in a continuous fashion. Hovering over the left plot displays a dynamically updating
                obtuse superbase representing a 2D lattice on the right plot.
               """),
        html.P("""
               The input boxes to the right can be used to generate a gif of the lattices between
                two points in the space of 2D continuous lattices.
               """),
        html.P("""
                This demonstrates the basic concept of the continuous, invariant-based classification of
                Kurlin (2022) and shows how the quotient triangle can visualise any 2D lattice under isometry
                 and uniform scaling.
               """)
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10', 'font-size': '18px'}),
    html.Div([
        html.H3('Select start and end values and press generate to create GIF of lattices between those points'),
        html.H5('Note: generating a GIF may take a few minutes'),
        html.H5("X coordinates"),
        dcc.Input(
            id="input_x0", type="number", placeholder="Start",
            min=0, max=1, step=0.001, debounce=True
            ),
        dcc.Input(
            id="input_x1", type="number", placeholder="End",
            min=0, max=1, step=0.001, debounce=True
            ),
        html.H5("Y coordinates"),
        dcc.Input(
            id="input_y0", type="number", placeholder="Start",
            min=0, max=1, step=0.001, debounce=True
            ),
        dcc.Input(
            id="input_y1", type="number", placeholder="End",
            min=0, max=1, step=0.001, debounce=True
            ),
        dcc.Button(id='gif-button', children="Generate", n_clicks=0),
        html.Div(id='confirm')
        ], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(figure=fig_l,
                  hoverData={'points': [{"x": 0, "y": 0}]},
                  config=config,
                  id='left-fig')
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'}),
    html.Div([
        dcc.Graph(config=config, id='right-fig'),
        html.P('v1=0, v2=0, ang=90', id='txt-output')
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
    if hover['x'] + hover['y'] >= 1:
        hover_x = 1 - hover['y']
        hover_y = 1 - hover['x']
    else:
        hover_x = hover['x']
        hover_y = hover['y']
    vals = generate_vals(hover_x, hover_y)
    if (hover['x'] + hover['y']) >= 1:
        txt = f"v1= {'%.3f' % vals['v1']}, v2={'%.3f' % (vals['v2'])}, ang={'%.3f' % ((vals['ang']) * 180/np.pi)}"
    else:
        txt = f"v1= {'%.3f' % vals['v1']}, v2={'%.3f' % vals['v2']}, ang={'%.3f' % (vals['ang'] * 180/np.pi)}"
    data = create_lattice_points(vals, origin, 4)
    fig_r = go.Figure(data=[go.Scatter(data, mode='markers',
                                       marker=dict(size=20,
                                                   color='black'),
                                       hoverinfo='none'
                                       )],
                      layout=go.Layout(width=600, height=600)
                      )
    arrow_cols = ["green", "blue", "red"]
    if (hover['x'] + hover['y']) >= 1:
        arrows = create_arrows(vals, origin, arrow_cols, "-")
    else:
        arrows = create_arrows(vals, origin, arrow_cols, "+")
    for arr in arrows:
        fig_r.add_annotation(arr)
    fig_r.update_xaxes(range=[-1.5, 1.5])
    fig_r.update_yaxes(range=[-1.5, 1.5])
    return fig_r, txt


# Callback for gif generation
@callback(
    Output('confirm', 'children'),
    Input('input_x0', 'value'),
    Input('input_x1', 'value'),
    Input('input_y0', 'value'),
    Input('input_y1', 'value'),
    Input('gif-button', 'n_clicks')
)
def output_gif(x0, x1, y0, y1, n_clicks):
    gif = GIF()
    check_val = [isinstance(x0, (int, float)),
                 isinstance(x1, (int, float)),
                 isinstance(y0, (int, float)),
                 isinstance(y1, (int, float))
                 ]
    if all(check_val) and not all([x0 == x1, y0 == y1]):
        x_range = np.linspace(x0, x1, 100, dtype=float)
        y_range = np.linspace(y0, y1, 100, dtype=float)
    else:
        return ""
    if n_clicks != 0 and ctx.triggered_id == 'gif-button':

        @capture(gif)
        def plot_gif(x_, y_):
            fig = generate_gif_frame(x_, y_, origin)
            return fig
        for x, y in zip(x_range, y_range):
            plot_gif(x, y)
        gif.create_gif(gif_path=f"lattice_gif_{n_clicks}.gif")
        return "gif created successfully!"
    else:
        return ""


# if __name__ == "__main__":
#     app.run(debug=True)
