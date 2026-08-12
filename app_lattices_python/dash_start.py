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
               including many based on the same chemical compositions but with slight differences in structure [2][3].
               With such large quantities of data, finite classification schemes may be insufficient.
               """),
        html.P("""
                A continuous classification scheme is capable of uniquely identifying lattice structures
                up to rigid motion (superposition) and uniform scaling [4]. This also allows for distinguishing between
                close but distinct structures caused by slight differences in real or simulated crystallisation conditions.
               """),
        html.H2("How does the root invariant classification scheme work?"),
        html.P("""
                This classification scheme operates using 'obtuse superbases'[5].
                 A superbase are a set of vectors {v\u2080, v\u2081...v\u2099} where v\u2080 = -\u2211 v\u2099 with 'conorms'
                 p\u1D62\u2C7C = -v\u1D62 \u00B7 v\u2C7C for all distinct indicies of i,j \u2208 {0, 1...n}.
                 A superbase is considered 'obtuse' if all conorms p\u1D62\u2C7C \u2265 0, if this is true, then all angles
                 between the vectors in the superbase are non-acute. A superbase can be called 'strict' if all p\u1D62\u2C7C \u003E 0 [4].
               """),
        html.P("""
                From the conorms of the obtuse superbases, the 'Root Invariant' of a lattice can be derived from the root products,
                 the square root of the conorms r\u1D62\u2C7C = \u221A p\u1D62\u2C7C and arranged in increasing order 
                 0 \u2264 r\u2081\u2082 \u2264 r\u2080\u2081 \u2264 r\u2080\u2082, forming the root invariant
                 RI = {r\u2081\u2082, r\u2080\u2081, r\u2080\u2082}. Every lattice has a unique root invariant up to isometry,
                 or up to rigid motion for non-rectangular lattices.
              """),
        html.P("For some relevant research papers, see the references page.")
    ], style={'width': '49%', 'display': 'inline-block', 'position': 'absolute', 'padding': '0 10'}),
    html.Div([
        html.Img(src=dash.get_asset_url("QT.png")),
        html.P("Location of Bravais Class lattices in the continuous space of 2D lattices, source: [1]")
    ],style={'width': '49%', 'position': 'absolute', 'top': '250px', 'right': '10px', 'display': 'inline-block'})
])
