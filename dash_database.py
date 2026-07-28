import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
import os
import sqlite3 as sql

from cif_read import map_crystal

dash.register_page(__name__, path="/database-map", name="Database map")

# left map graph
size = np.linspace(0, 1, 1001)
z = np.zeros((1001, 1001))

# placeholder code for eventual sqlite database connection
# con = sql.connect("test.db")
# cur = con.cursor()
# for row in cur.execute("SELECT * from codheatmap ORDER BY RowNo"):
#     z[row[0], row[1]] = row[2]

path = "CIF_Files"
cifs = []
with os.scandir(path) as it:
    for entry in it:
        if ".cif" in entry.name and entry.is_file():
            cifs.append(entry.name)
for file in cifs:
    filepath = f"CIF_files/{file}"
    coords = map_crystal(filepath)
    for tup in coords:
        z[int(tup[1] * 1000), int(tup[0] * 1000)] += 1
config = {'displayModeBar': False}
fig_l = go.Figure(data=[go.Heatmap(x=size, y=size,
                        z=z,
                        colorscale='Hot',
                        reversescale=True,
                        hoverinfo='x+y+z'
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

fig_r = go.Figure(data=[go.Surface(z=z, x=size, y=size,
                                   colorscale='Hot',
                                   reversescale=True,
                                   )],
                  layout=go.Layout(width=600, height=600))

layout = html.Div([
        html.Div([
            dcc.Graph(figure=fig_l, config=config)
                 ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 10'}),
        html.Div([
            dcc.Graph(figure=fig_r, config=config),
                 ], style={'display': 'inline-block', 'width': '49%'})
])
