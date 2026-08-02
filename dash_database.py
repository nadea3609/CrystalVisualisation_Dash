import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
import sqlite3 as sql

dash.register_page(__name__, path="/database-map", name="Database map")

# left map graph
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
# for i in range(0, 1001):
#     if z[0, i] == 0:
#         z[0, i] += 0.1
bar = dict(
    tick0=0,
    tickvals=[0, 1, 2, 3, 4],
    ticktext=['0', '10\u00b9', '10\u00b2',
              '10\u00b3', '10\u2074'],
    title={'text': "Number of lattices", 'side': "right"}
)

config = {'displayModeBar': False, 'responsive': True}
fig_l = go.Figure(data=[go.Heatmap(x=size, y=size,
                        z=np.log10(z),
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
fig_l.update_xaxes(range=[0, 1])
fig_l.update_yaxes(range=[0, 1])
fig_l.update_layout()

# right map graph

fig_r = go.Figure(data=[go.Surface(x=size, y=size,
                                   z=np.log10(z),
                                   colorscale='Hot',
                                   colorbar=bar,
                                   reversescale=True,
                                   hoverinfo='none'
                                   )],
                  layout=go.Layout(width=600, height=600))
fig_r.update_xaxes(range=[0, 1])
fig_r.update_yaxes(range=[0, 1])
fig_r.update_layout()

layout = html.Div([
        html.H1("Database map"),
        html.P("""This shows how crystals within a modern large database
                   map onto the space of 2D lattices created by the
                   continuous classification scheme"""),
        html.Div([
            dcc.Graph(figure=fig_l, config=config)
                 ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'}),
        html.Div([
            dcc.Graph(figure=fig_r, config=config),
                 ], style={'display': 'inline-block', 'width': '49%'}),
        html.P("""
               The default database map was produced using the Crystallography Open Database,
               downloaded in July 2026.
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
            html.Li("Run the 'database_scan.py' code on the downloaded database, this will take some time."),
            html.Li("Replace the 'cod.db' file in this app's folder with the database file produced")
        ])
])
