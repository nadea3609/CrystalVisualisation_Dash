import dash
from dash import html

dash.register_page(__name__, path="/", name="Landing page")

layout = html.Div([
    html.H1("Select an operation mode from the list above to get started"),
    html.H2("Why is a continuous classification scheme important?"),
    html.Div([
        html.P("""
               Traditional crystallography uses finite classification schemes,
               such as Bravais Classes or space-group types. These are generally
               suitable for manual or visual identification of highly symmetric crystals [1].
               """),
        html.P("""
               However, modern day crystallographic databases contain vast numbers of crystal structures,
               including many based on the same chemical compositions but with slight differences in structure [2].
               With such large quantities of data, finite classification schemes may be insufficient.
               """),
        html.P("""
                A continuous classification scheme is capable of uniquely identifying lattice structures
                up to rigid motion (superposition) and uniform scaling. This also allows for distinguishing between
                close but distinct structures caused by slight differences in real or simulated crystallisation conditions.
               """)
    ], style={'width': '49%', 'display': 'inline-block', 'position': 'absolute', 'padding': '0 10'}),
    html.Div([
        html.Img(src=dash.get_asset_url("QT.png")),
        html.P("Location of Bravais Class lattices in the continuous space of 2D lattices, source: [1]")
    ],style={'width': '49%', 'position': 'absolute', 'top': '250px', 'right': '10px', 'display': 'inline-block'})
])
