import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np
import sqlite3 as sql

dash.register_page(__name__, path="/database-map", name="Database map")

# constants and configs
np.seterr(divide="ignore")
size = np.linspace(0, 1, 1001)
z = np.zeros((1001, 1001))
# sqlite database connection
con = sql.connect("cod_complete.db")
cur = con.cursor()
res = cur.execute("SELECT * from codcoords")
for tup in res.fetchall():
    if tup[0] is None:
        continue
    elif tup[0] > 1 or tup[1] > 1:
        continue
    elif tup[1] == -0.0:
        z[0, int(tup[0] * 1000)] += 1
    else:
        z[int(tup[1] * 1000), int(tup[0] * 1000)] += 1
z_trim = z.copy()
z_trim[0, 0:] = 0
z_trim[1000, 0] = 0
bar = dict(
    tick0=0,
    tickvals=[0, 1, 2, 3, 4],
    ticktext=['0', '10\u00b9', '10\u00b2',
              '10\u00b3', '10\u2074'],
    title={'text': "Number of lattices", 'side': "right"}
)
bar_lin = dict(
    tick0=0,
    tickvals=[0, 10000, 20000, 50000, 70000],
    ticktext=['0', '10k', '20k',
              '50k', '70k'],
    title={'text': "Number of lattices", 'side': "right"}
)
bar_lin_tr = dict(
    tick0=0,
    title={'text': "Number of lattices", 'side': "right"}
)
config = {'displayModeBar': False, 'responsive': True}
layout = html.Div([
        html.H1("Database map"),
        html.P("""
                   This shows how crystals within a modern large database
                   map onto the space of 2D lattices created by the
                   continuous classification scheme. 
                   Here the distribution can be viewed as a 2D heatmap and a 3D histogram.
                   The graphs here use a logarithmic scale by default to account for the high numbers 
                   of square lattices along y = 0, and hexagonal lattices at [0, 1].
                   To view the map on a linear scale, select the "Linear" option from the buttons,
                   to view a linear scale with the extreme values removed, select "Linear Trimmed".
                   """, style={'font-size': '18px'}),
        html.P("""
                 This demonstrates the applicability of a continuous classification scheme
                  to real-life data, showing the distribution of lattice structures of an
                  entire database onto the space of 2D lattice structures.
                  This can allow for visualisation of structural trends within sets of crystals.
                 """, style={'font-size': '18px'}),
        dcc.RadioItems(options=("Log", "Linear", "Linear Trimmed"), value="Log", id='scale-select'),
        html.Div([
            dcc.Graph(config=config, id='left-dbmap')
                 ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'}),
        html.Div([
            dcc.Graph(config=config, id='right-dbmap'),
                 ], style={'display': 'inline-block', 'width': '49%'}),
        html.P("""
               The default database map was produced using the Crystallography Open Database,
               downloaded in July 2026. This version contains approximately 534,824 individual
                crystal structures.
               """),
        html.H5("Updating the database"),
        html.P("To update or change the database used for this map:"),
        html.Ul([
            html.Li("""
                    Download the 'cif_read.py' and 'database_scan.py' files from
                    https://github.com/nadea3609/CrystalVisualisation_Dash
                    """
                    ),
            html.Li("Download the database you wish to use (warning, these tend to be very large, make sure you have enough space!)"),
            html.Li("Run the 'database_scan.py' code on the downloaded database (you will need to modify the code to target the database path on your computer), this will take some time."),
            html.Li("Replace the 'cod_complete.db' file in this app's folder with the database file produced (you may need to rename the file or modify the code so it recognises the new database)")
        ])
])


# callback for figure generation and scale updating
@callback(
    Output('left-dbmap', 'figure'),
    Output('right-dbmap', 'figure'),
    Input('scale-select', 'value')
)
def update_maps(value):
    np.seterr(divide="ignore")
    if value == "Log":
        fig_l = go.Figure(data=[go.Heatmap(x=size, y=size,
                        z=np.log10(z),
                        colorscale='Hot',
                        showscale=False,
                        reversescale=True,
                        hoverinfo='none'
                                   )],
                          layout=go.Layout(
                     width=600,
                     height=600,
                     autosize=False
                  ))
        fig_r = go.Figure(data=[go.Surface(x=size, y=size,
                                           z=np.log10(z),
                                           colorscale='Hot',
                                           colorbar=bar,
                                           reversescale=True,
                                           hoverinfo='none'
                                            )],
                                layout=go.Layout(width=600, height=600))
    elif value == "Linear":
        fig_l = go.Figure(data=[go.Heatmap(x=size, y=size,
                        z=z,
                        colorscale='Hot',
                        showscale=False,
                        reversescale=True,
                        hoverinfo='none'
                                   )
                        ],
                  layout=go.Layout(
                     width=600,
                     height=600,
                     autosize=False
                  ))
        fig_r = go.Figure(data=[go.Surface(x=size, y=size,
                                        z=z,
                                        colorscale='Hot',
                                        colorbar=bar_lin,
                                        reversescale=True,
                                        hoverinfo='none'
                                        )],
                        layout=go.Layout(width=600, height=600))
    elif value == "Linear Trimmed":
        fig_l = go.Figure(data=[go.Heatmap(x=size, y=size,
                                           z=z_trim,
                                           colorscale='Hot',
                                           showscale=False,
                                           reversescale=True,
                                           hoverinfo='none'
                                           )],
                          layout=go.Layout(
                     width=600,
                     height=600,
                     autosize=False
                  ))
        fig_r = go.Figure(data=[go.Surface(x=size, y=size,
                                           z=z_trim,
                                           colorscale='Hot',
                                           colorbar=bar_lin_tr,
                                           reversescale=True,
                                           hoverinfo='none'
                                           )],
                          layout=go.Layout(width=600, height=600))
    fig_l.update_xaxes(range=[0, 1])
    fig_l.update_yaxes(range=[0, 1])
    fig_l.update_layout()
    fig_r.update_xaxes(range=[0, 1])
    fig_r.update_yaxes(range=[0, 1])
    fig_r.update_layout()
    return fig_l, fig_r
